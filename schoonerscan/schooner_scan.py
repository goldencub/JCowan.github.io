"""
Script name: schooner_scan.py
Author:      Josiah Cowan
Version:     2.0
Purpose:     Scan a range of TCP ports on a target IP address or hostname
             and report which ports are open. Results are logged to a file.
Date started: 25.11.25
Date updated: 01.08.26

Usage:
    Interactive:  python schooner_scan.py
    One-shot:     python schooner_scan.py 10.0.1.1 -p 1-1024
                  python schooner_scan.py scanme.nmap.org --ports 20-443 --timeout 0.5

Note: IPv4 only. gethostbyname() and AF_INET resolve to IPv4 addresses by
      design; IPv6 targets are intentionally out of scope for this tool.
"""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


LOG_FILE = "scan_log.txt"
MAX_WORKERS = 100  # how many ports we probe at once


BANNER = r"""
                       |    |    |
                      )_)  )_)  )_)
                     )___))___))___)\
                    )____)____)_____)\\
                  _____|____|____|____\\\__
         ---------\                      /---------
           ^^^^^^^^\  S C H O O N E R   /^^^^^^^^^^
             ^^^^^^^^\    S C A N      /^^^^^^^^
               ^^^^^^^^\______________/^^^^^^
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^
   ============ TCP Port Scanner - all ports on deck ============
"""


def log_message(message: str, log_handle) -> None:
    """
    Append a timestamped message to an already-open log file.

    Passing the open file handle in (instead of reopening the file every
    call) avoids hammering the disk during large scans.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_handle.write(f"[{timestamp}] {message}\n")


def get_service_name(port: int) -> str:
    """
    Return the well-known service name for a TCP port (e.g. 'ssh', 'http'),
    or an empty string if the port has no registered name.
    """
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return ""


def resolve_target(target_input: str) -> str | None:
    """
    Resolve a hostname or IP string to an IPv4 address.

    Returns the IP as a string, or None if it can't be resolved.
    """
    try:
        return socket.gethostbyname(target_input)
    except socket.gaierror:
        return None


def get_target() -> str:
    """
    Prompt the user for an IP address or hostname and validate it.

    Returns:
        The resolved IP address as a string.
    """
    while True:
        target_input = input("Enter target IP address or hostname: ").strip()
        target_ip = resolve_target(target_input)

        if target_ip is None:
            print("Error: invalid or unreachable IP/hostname. Please try again.\n")
            continue

        print(f"Target resolved to IP: {target_ip}")
        return target_ip


def validate_port_range(start_port: int, end_port: int) -> str | None:
    """
    Check that a port range is sane.

    Returns an error message string if invalid, or None if the range is fine.
    These three checks together cover all four bounds: if start >= 1 and
    end <= 65535 and start <= end, then end is also >= 1 and start also <= 65535.
    """
    if start_port < 1 or end_port > 65535:
        return "Ports must be between 1 and 65535."
    if start_port > end_port:
        return "Start port cannot be greater than end port."
    return None


def get_port_range() -> tuple[int, int]:
    """
    Prompt the user for a start and end port and validate them.

    Returns:
        A tuple containing (start_port, end_port).
    """
    while True:
        start_input = input("Enter start port (1-65535): ").strip()
        end_input = input("Enter end port (1-65535): ").strip()

        try:
            start_port = int(start_input)
            end_port = int(end_input)
        except ValueError:
            print("Error: ports must be whole numbers. Please try again.\n")
            continue

        error = validate_port_range(start_port, end_port)
        if error:
            print(f"Error: {error} Please try again.\n")
            continue

        return start_port, end_port


def check_port(target_ip: str, port: int, timeout: float) -> int | None:
    """
    Probe a single TCP port.

    Returns the port number if it's open, otherwise None.
    Designed to be run in a thread pool, so it does no printing itself.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            # connect_ex returns 0 on a successful connection (open port)
            if sock.connect_ex((target_ip, port)) == 0:
                return port
        except socket.error:
            pass
    return None


def scan_ports(target_ip: str, start_port: int, end_port: int,
               timeout: float, log_handle) -> None:
    """
    Scan a range of TCP ports on the target using a thread pool.

    Args:
        target_ip:  Target IP address as a string.
        start_port: First port in the range.
        end_port:   Last port in the range.
        timeout:    Per-port connection timeout in seconds.
        log_handle: Open file handle for logging.
    """
    total = end_port - start_port + 1
    print(f"\nStarting scan on {target_ip} from port {start_port} to {end_port} "
          f"({total} ports, {timeout}s timeout)...")
    log_message(f"Scan started on {target_ip}, ports {start_port}-{end_port}", log_handle)

    open_ports = []
    start_time = datetime.now()

    try:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit every port to the pool, then handle results as they finish.
            futures = {
                executor.submit(check_port, target_ip, port, timeout): port
                for port in range(start_port, end_port + 1)
            }

            for future in as_completed(futures):
                port = future.result()
                if port is not None:
                    service = get_service_name(port)
                    label = f"{port} ({service})" if service else f"{port}"
                    print(f"Port {label} OPEN")
                    log_message(f"[OPEN] Port {label} on {target_ip}", log_handle)
                    open_ports.append(port)
    except KeyboardInterrupt:
        # Ctrl+C during a scan: bail out cleanly and still report what we found.
        print("\n\nScan interrupted by user. Reporting partial results...")
        log_message(f"Scan interrupted by user on {target_ip}", log_handle)

    open_ports.sort()  # results arrive out of order with threading
    elapsed = (datetime.now() - start_time).total_seconds()

    # Summary
    print("\nScan complete.")
    print(f"Total ports scanned: {total}")
    print(f"Open ports found:    {len(open_ports)}")
    if open_ports:
        print("Open ports:", ", ".join(str(p) for p in open_ports))
    print(f"Time taken:          {elapsed:.2f} seconds")

    log_message(
        f"Scan finished on {target_ip} in {elapsed:.2f}s. "
        f"Open ports: {open_ports if open_ports else 'None'}",
        log_handle,
    )


def parse_args() -> argparse.Namespace:
    """
    Parse optional command-line arguments for non-interactive use.
    """
    parser = argparse.ArgumentParser(
        description="SchoonerScan - a simple threaded TCP port scanner."
    )
    parser.add_argument(
        "target", nargs="?",
        help="Target IP address or hostname. Omit to run interactively."
    )
    parser.add_argument(
        "-p", "--ports", default=None,
        help="Port range as START-END, e.g. 1-1024."
    )
    parser.add_argument(
        "-t", "--timeout", type=float, default=0.5,
        help="Per-port connection timeout in seconds (default: 0.5)."
    )
    return parser.parse_args()


def run_from_args(args: argparse.Namespace, log_handle) -> bool:
    """
    Run a single scan from command-line arguments.

    Returns True if a scan ran, False if arguments were missing/invalid
    (in which case the caller should fall back to interactive mode).
    """
    if not args.target:
        return False

    target_ip = resolve_target(args.target)
    if target_ip is None:
        print(f"Error: could not resolve '{args.target}'.")
        return True  # we handled it (with an error); don't drop into prompts

    print(f"Target resolved to IP: {target_ip}")

    # Default to a common range if no ports were supplied.
    port_range = args.ports if args.ports else "1-1024"
    try:
        start_str, end_str = port_range.split("-")
        start_port, end_port = int(start_str), int(end_str)
    except ValueError:
        print("Error: ports must look like START-END, e.g. 1-1024.")
        return True

    error = validate_port_range(start_port, end_port)
    if error:
        print(f"Error: {error}")
        return True

    scan_ports(target_ip, start_port, end_port, args.timeout, log_handle)
    return True


def interactive_loop(log_handle) -> None:
    """
    Repeated-scan loop for interactive use.
    """
    while True:
        target_ip = get_target()
        start_port, end_port = get_port_range()
        scan_ports(target_ip, start_port, end_port, 0.5, log_handle)

        choice = input("\nRun another scan? (y/n): ").strip().lower()
        if choice != "y":
            print("Weighing anchor. Goodbye.")
            break


def main() -> None:
    print(BANNER)

    args = parse_args()

    # Open the log file once for the whole session.
    with open(LOG_FILE, "a", encoding="utf-8") as log_handle:
        try:
            # If a target was passed on the command line, do one scan and exit.
            # Otherwise fall through to the interactive prompts.
            if not run_from_args(args, log_handle):
                interactive_loop(log_handle)
        except KeyboardInterrupt:
            # Ctrl+C at a prompt (rather than mid-scan).
            print("\nInterrupted. Weighing anchor. Goodbye.")


if __name__ == "__main__":
    main()
