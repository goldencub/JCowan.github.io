---
layout: default
---

Text can be **bold**, _italic_, ~~strikethrough~~ or `keyword`.

[Link to another page](./another-page.html).

There should be whitespace between paragraphs.

There should be whitespace between paragraphs. We recommend including a README, or a file with information about your project.

[#Active Directory & Microsoft Sentinal Home Lab](./another-page.html)

[#Phishing Email Analysis Project](./another-page.html)

[#ServiceNow ITSM Practice](./another-page.html)

[#Malware Reverse Engineering](./another-page.html)


 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 I built a virtualised enterprise environment in Hyper-V consisting of a Windows Server 2016 Domain Controller, a Windows 10 workstation, and a Kali Linux attacker machine, to simulate a realistic small business network end to end. I administered Active Directory — structuring Organisational Units, managing the full user lifecycle, and applying group-based access control through security groups. I hardened the domain using Group Policy, enforcing password complexity, account lockout thresholds, USB storage restrictions, and screen lock timeouts, scoped per department to reflect real organisational policy design. To bring in a security monitoring layer, I registered the Domain Controller with Azure Arc and deployed the Azure Monitor Agent to forward Windows Security events into Microsoft Sentinel. From there I used KQL to query live authentication telemetry, identifying failed logon events and account lockouts across the domain — the same investigative workflow a SOC analyst uses to detect brute-force activity.

# Phishing Email Analysis Project

I investigated suspected phishing emails using PhishTool and VirusTotal to practise the analyst workflow for email-based threats. This involved analysing email headers and SMTP routing to identify spoofing attempts, decoding Base64-encoded content to inspect hidden payloads, and examining malicious URLs and domains using threat intelligence tools. I documented each investigation and classified the phishing indicators I found, building a repeatable process for identifying and triaging this type of alert — one of the most common categories of incident a Tier 1 SOC analyst handles.


# ServiceNow ITSM Practice

I deployed and configured a ServiceNow Personal Developer Instance to practise structured incident lifecycle management — logging, investigation, escalation, and resolution — in a real ITSM platform. I completed full Tier 1 and Tier 2 escalation workflows with detailed work notes documenting each step, and applied ITIL concepts including the Impact/Urgency priority matrix and resolution code classification. This gave me practical experience with the ticketing and escalation discipline that underpins how real SOC teams track and hand off incidents. 

```js
// Javascript code with syntax highlighting.
var fun = function lang(l) {
  dateformat.i18n = require('./lang/' + l)
  return true;
}
```

```ruby
# Ruby code with syntax highlighting
GitHubPages::Dependencies.gems.each do |gem, version|
  s.add_dependency(gem, "= #{version}")
end
```

#### Header 4

*   This is an unordered list following a header.
*   This is an unordered list following a header.
*   This is an unordered list following a header.

##### Header 5

1.  This is an ordered list following a header.
2.  This is an ordered list following a header.
3.  This is an ordered list following a header.

###### Header 6

| head1        | head two          | three |
|:-------------|:------------------|:------|
| ok           | good swedish fish | nice  |
| out of stock | good and plenty   | nice  |
| ok           | good `oreos`      | hmm   |
| ok           | good `zoute` drop | yumm  |

### There's a horizontal rule below this.

* * *

### Here is an unordered list:

*   Item foo
*   Item bar
*   Item baz
*   Item zip

### And an ordered list:

1.  Item one
1.  Item two
1.  Item three
1.  Item four

### And a nested list:

- level 1 item
  - level 2 item
  - level 2 item
    - level 3 item
    - level 3 item
- level 1 item
  - level 2 item
  - level 2 item
  - level 2 item
- level 1 item
  - level 2 item
  - level 2 item
- level 1 item

### Small image

![Octocat](https://github.githubassets.com/images/icons/emoji/octocat.png)

### Large image

![Branching](Screenshot 2025-09-15 114336.png)


### Definition lists can be used with HTML syntax.

<dl>
<dt>Name</dt>
<dd>Godzilla</dd>
<dt>Born</dt>
<dd>1952</dd>
<dt>Birthplace</dt>
<dd>Japan</dd>
<dt>Color</dt>
<dd>Green</dd>
</dl>

```
Long, single-line code blocks should not wrap. They should horizontally scroll if they are too long. This line should be long enough to demonstrate this.
```

```
The final element.
```
