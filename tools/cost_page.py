import re

f = 'guides/cyber-essentials-cost.html'
s = open(f, encoding='utf-8').read()

if 'The short answer' not in s:
    s = s.replace('<title>How much does Cyber Essentials cost? The fee, and the bit nobody mentions',
                  '<title>How much does Cyber Essentials cost in 2026? Fees by size, Plus, and the real total', 1)
    s = s.replace('<meta property="og:title" content="How much does Cyber Essentials cost?">',
                  '<meta property="og:title" content="How much does Cyber Essentials cost in 2026? Fees by size, Plus, and the real total">', 1)
    s = s.replace('"headline":"How much does Cyber Essentials cost?"',
                  '"headline":"How much does Cyber Essentials cost in 2026? Fees by size, Plus, and the real total"', 1)
    s = s.replace('"dateModified":"2026-08-23"', '"dateModified":"2026-09-13"', 1)
    s = s.replace('<h1>How much does Cyber Essentials cost?</h1>',
                  '<h1>How much does Cyber Essentials cost in 2026?</h1>', 1)

    short = '''<h2>The short answer</h2>
<p>The Cyber Essentials certification fee is <strong>£320 to £600 plus VAT</strong>, set by IASME and banded by organisation size: from £320 for a micro business (under 10 people), around £400 for a small one (10\u201349), £450 for medium (50\u2013249) and £500\u2013600 for large. That buys the assessment. A typical small business all-in \u2014 fee, a provider that reviews your answers before submission and covers a resubmission, and a few hours of configuration \u2014 lands between <strong>£600 and £1,500</strong>. Cyber Essentials Plus adds <strong>£1,500 to £3,000</strong> on top. Everything below explains where each of those numbers comes from.</p>

'''
    s = s.replace('<h2>The certification fee</h2>', short + '<h2>The certification fee</h2>', 1)

    total = '''<h2>Adding it up</h2>

<p>Three worked cases, all excluding VAT:</p>
<ul>
  <li><strong>Ready already</strong> \u2014 MFA on everywhere, supported devices, individual accounts. The fee (£320\u2013£400) plus a provider\u2019s service charge if you use one. <strong>Around £400\u2013£800 total.</strong></li>
  <li><strong>Nearly ready</strong> \u2014 a few hours of configuration: MFA switched on across services, admin accounts separated, an old browser retired. Fee plus £200\u2013£600 of work. <strong>Around £600\u2013£1,500 total.</strong></li>
  <li><strong>Starting from behind</strong> \u2014 unsupported machines to replace, no MFA, shared logins. Fee plus a hardware and configuration project that is worth doing regardless of certification: £1,500\u2013£5,000 depending on how many machines. This is where the government\u2019s ~£5,000 mean figure comes from.</li>
</ul>
<p>Add £1,500\u2013£3,000 for Cyber Essentials Plus if a customer, framework or insurer specifically requires it \u2014 most that say \u201cCyber Essentials\u201d mean the base certificate. And remember the £25,000 of <a href="/guides/cyber-essentials-insurance.html">cyber liability insurance</a> included with a pass, which offsets a good part of the fee for any business that would otherwise buy cover.</p>
'''
    s = re.sub(r'<h2>Adding it up</h2>\s*<p>For a typical small organisation.*?</p>\n', total, s, 1, flags=re.S)
    open(f, 'w', encoding='utf-8').write(s)

sm = open('sitemap.xml').read()
sm2 = re.sub(r'(<loc>https://passcyber.co.uk/guides/cyber-essentials-cost</loc><lastmod>)[^<]+', r'\g<1>2026-09-13', sm, 1)
if sm2 != sm:
    open('sitemap.xml', 'w').write(sm2)
