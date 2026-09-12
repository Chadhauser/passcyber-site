import re, json, html

TPL = 'guides/cyber-essentials-renewal.html'

def make(slug, title, desc, h1, stand, reading, prose, cta_h2, cta_p, keep_capture=False, capture_title=None, capture_p=None):
    s = open(TPL, encoding='utf-8').read()
    url = 'https://passcyber.co.uk/guides/' + slug
    s = re.sub(r'<title>.*?</title>', '<title>%s | PassCyber</title>' % html.escape(title), s, 1)
    s = re.sub(r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % html.escape(desc, quote=True), s, 1)
    s = re.sub(r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % url, s, 1)
    s = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="%s">' % html.escape(title, quote=True), s, 1)
    s = re.sub(r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="%s">' % html.escape(desc, quote=True), s, 1)
    s = re.sub(r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="%s">' % url, s, 1)
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "url": url,
          "datePublished": "2026-09-13",
          "author": {"@type": "Organization", "name": "PassCyber"},
          "publisher": {"@type": "Organization", "name": "Edwards Bros (Spaldwick) Ltd", "url": "https://www.edwardsbros.co.uk/"},
          "isPartOf": {"@type": "WebSite", "name": "PassCyber", "url": "https://passcyber.co.uk/"}}
    s = re.sub(r'<script type="application/ld\+json">.*?</script>',
               '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), s, 1, flags=re.S)
    s = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % h1, s, 1, flags=re.S)
    s = re.sub(r'<p class="stand">.*?</p>', '<p class="stand">%s</p>' % stand, s, 1, flags=re.S)
    s = re.sub(r'<div class="meta">.*?</div>', '<div class="meta"><span>Updated for the current question set</span><span>Reading time %s minutes</span></div>' % reading, s, 1, flags=re.S)
    a = s.index('<div class="prose">') + len('<div class="prose">')
    b = s.index('<div class="ok">')
    block = '\n\n' + prose + '\n'
    if keep_capture:
        block += '''
<div class="capture">
  <h3>%s</h3>
  <p class="small">%s</p>
  <form id="rnform" novalidate>
    <input type="email" id="rnemail" placeholder="you@business.co.uk" required aria-label="Email address">
    <button type="submit">Email me the checklist</button>
  </form>
  <div class="ok-msg" id="rnok">Done — the checklist's on its way to your inbox.</div>
</div>

''' % (capture_title, capture_p)
    else:
        s = re.sub(r'<script>\s*document\.getElementById\(\'rnform\'\).*?</script>', '', s, 1, flags=re.S)
    s = s[:a] + block + s[b:]
    s = re.sub(r'(<div class="cta">\s*<div class="t">PassCyber</div>\s*)<h2>.*?</h2>\s*<p>.*?</p>',
               r'\g<1>' + '<h2>%s</h2>\n  <p>%s</p>' % (cta_h2, cta_p), s, 1, flags=re.S)
    if '<table' in prose:
        s = s.replace('</style>', '.prose table{width:100%;border-collapse:collapse;font-size:.93em;margin:1.2em 0}.prose th,.prose td{border:1px solid #d9d9d4;padding:8px 10px;text-align:left;vertical-align:top}.prose th{background:#f3f3ef}\n</style>', 1)
    open('guides/' + slug + '.html', 'w', encoding='utf-8').write(s)

LOGO = """<h2>The short answer</h2>
<p>Once you pass, IASME sends you the official Cyber Essentials logo files with your certificate number and expiry date. You may use it on your website, email signatures, tenders and stationery for exactly twelve months from the certification date, and you must stop using it the day the certificate expires. There is no fee for the logo and no separate application — it comes with the pass.</p>

<h2>Where the logo comes from</h2>
<p>The logo is issued by IASME, which runs the scheme for the National Cyber Security Centre, not by the certification body that assessed you. After a pass you receive an email containing the certificate as a PDF and a link to the logo pack — the standard Cyber Essentials badge, and the Cyber Essentials Plus badge if you certified at that level. Downloading a copy from an image search is not the same thing: the scheme's rules require the version issued to you, and a logo without a valid certificate behind it is a misrepresentation.</p>

<h2>What you're allowed to do with it</h2>
<ul>
  <li><strong>Website</strong> — footer, an "accreditations" panel, a security page. Linking the badge to the public certificate register is good practice and helps anyone checking you.</li>
  <li><strong>Email signatures</strong> — the most-seen placement, and the one that quietly reassures customers and suppliers.</li>
  <li><strong>Tenders and pre-qualification questionnaires</strong> — attach the certificate; the badge goes on the cover.</li>
  <li><strong>Stationery, brochures, vehicles, premises</strong> — permitted while the certificate is valid.</li>
  <li><strong>Social media</strong> — fine, with the same twelve-month limit.</li>
</ul>

<h2>What you must not do</h2>
<ul>
  <li>Use the logo after expiry. Certificates last twelve months; the day after, the badge comes down until you've <a href="/guides/cyber-essentials-renewal.html">recertified</a>.</li>
  <li>Alter the logo — recolour it, crop it, put it on a busy background, or stretch it.</li>
  <li>Use the Plus badge if you only hold the basic certificate.</li>
  <li>Imply the certificate covers a company, site or subsidiary that was outside the assessed scope.</li>
  <li>Use it while an application is pending. "Working towards Cyber Essentials" is a sentence, not a badge.</li>
</ul>

<h2>Getting the sizing right</h2>
<p>The pack contains PNG and vector versions. Use the vector (SVG or EPS) for print, and the PNG at a sensible size for web — the badge should be legible but not the largest thing on the page. Keep clear space around it roughly equal to the height of the shield, and don't put it on a background that fights the colours. The current logo was simplified specifically to stay readable at small sizes in email signatures, so there is no need to enlarge it.</p>

<h2>How to prove the badge is real</h2>
<p>Anyone can check a certificate on the public register by company name; add a line under the badge — "Certificate number XXXXX, valid to Month 2027" — and you've answered the question before it's asked. If you're the one checking a supplier, our <a href="/guides/verify-cyber-essentials-certificate.html">verification guide</a> walks through it.</p>

<h2>If you've lost the logo pack</h2>
<p>Ask the certification body that processed your assessment; they can re-issue the link. If you certified through PassCyber, one email does it. Keep the files somewhere shared rather than in one person's inbox — the commonest reason a business is caught using an expired badge is that nobody knew where the current one lived.</p>
"""

CHECKLIST = """<h2>The checklist in one screen</h2>
<p>Cyber Essentials tests five technical controls. If every line below is true for every device and account in scope, you will pass. If any line is false, that is the work to do before you submit — and the two marked <strong>auto-fail</strong> will fail the whole assessment on their own.</p>

<h3>1. Firewalls and internet gateways</h3>
<ul>
  <li>Every internet connection sits behind a firewall — the router's built-in one counts, as does the software firewall on a laptop used on public Wi-Fi.</li>
  <li>Default admin passwords on routers and firewalls have been changed.</li>
  <li>No inbound services are open to the internet unless there is a documented business need.</li>
  <li>Remote administration of the firewall is disabled or protected by MFA.</li>
</ul>

<h3>2. Secure configuration</h3>
<ul>
  <li>Unused software, accounts and services have been removed or disabled on every device.</li>
  <li>Default passwords on every device and application have been changed.</li>
  <li>Auto-run of removable media is off.</li>
  <li>Devices lock after inactivity, and unlocking needs a password, PIN or biometric.</li>
</ul>

<h3>3. Security update management</h3>
<ul>
  <li><strong>Auto-fail:</strong> nothing in scope runs an operating system or application that is out of vendor support. <a href="/guides/windows-10-cyber-essentials.html">Windows 10 is the one that catches people.</a></li>
  <li>High-risk and critical updates are applied within 14 days of release.</li>
  <li>Automatic updates are switched on wherever the software allows.</li>
  <li>Software is licensed and supported — no abandoned browsers or old office suites.</li>
</ul>

<h3>4. User access control</h3>
<ul>
  <li>Every user has their own account; no shared logins.</li>
  <li>Admin accounts are separate from day-to-day accounts and used only for admin tasks.</li>
  <li>Accounts are created through a documented process and removed when people leave.</li>
  <li><strong>Auto-fail:</strong> multi-factor authentication is on for every cloud service that offers it. <a href="/guides/cyber-essentials-mfa-requirements.html">The MFA rules in full.</a></li>
  <li>Passwords meet the scheme's minimum — a password manager and a 12-character minimum is the simplest compliant setup.</li>
</ul>

<h3>5. Malware protection</h3>
<ul>
  <li>Every in-scope device has anti-malware software that updates automatically and scans files on access, <em>or</em> only runs approved applications (allow-listing), <em>or</em> runs apps only in a sandbox.</li>
  <li>Phones and tablets only install apps from the official store, and the device is not jailbroken or rooted.</li>
</ul>

<h2>Before the five controls: get the scope right</h2>
<p>Most failures aren't a control — they're a device nobody counted. Home-working laptops, the director's personal phone with work email on it, the tablet on the shop floor, the server in the cupboard: if it touches business data or the business network, it is in scope and every line above applies to it. <a href="/guides/cyber-essentials-scope-personal-devices.html">Personal devices are the usual surprise.</a></p>

<h2>What the questionnaire will ask you for</h2>
<p>The self-assessment is around 70 questions, answered by someone who can sign on behalf of the business. You'll need: a count of devices by operating system and version, a count of servers and what they run, a list of your cloud services and whether MFA is on for each, the name of your anti-malware product, and confirmation of who holds admin rights. Gather those before you open the portal and the questionnaire takes an afternoon rather than a fortnight. There's a fuller walk-through in <a href="/guides/cyber-essentials-questionnaire-answers.html">how to answer the questionnaire</a>.</p>

<h2>How long the whole thing takes</h2>
<p>If the checklist is already true: a week. If you have an unsupported machine to replace or MFA to roll out: four to six weeks, most of it waiting for the fixes. Certification bodies typically return a result within a few working days of submission, and you get one free resubmission if something is marked as needing more information.</p>
"""

INSURANCE = """<h2>The short answer</h2>
<p>Every UK organisation with turnover under £20 million that passes Cyber Essentials gets cyber liability insurance included free for the twelve months of the certificate — £25,000 of cover, with no excess, arranged through the scheme rather than bought by you. It's automatic on a pass, provided you opt in on the application form and give a domain registered in the UK. It is not a substitute for a proper cyber policy, but for a small business it is real cover for nothing.</p>

<h2>What the free cover actually includes</h2>
<ul>
  <li><strong>Limit:</strong> £25,000 aggregate for the certificate year.</li>
  <li><strong>Excess:</strong> none.</li>
  <li><strong>Covers:</strong> breach response costs — forensic investigation, legal and regulatory help, notifying affected people, crisis PR — and third-party liability arising from a data breach or cyber event.</li>
  <li><strong>Includes:</strong> access to a 24-hour incident helpline, which for a small business without an IT department is worth more than the limit.</li>
  <li><strong>Eligibility:</strong> UK-domiciled organisation, turnover under £20 million, whole organisation certified (not a partial scope), and the opt-in box ticked on the self-assessment.</li>
</ul>
<p>You'll receive the policy documents from the insurer shortly after your certificate — separately, and often overlooked in the inbox. File them with the certificate.</p>

<h2>Why insurers care about the certificate</h2>
<p>Cyber Essentials is the baseline most cyber and professional indemnity underwriters now ask about, because the five controls it tests are the ones that stop the majority of everyday attacks. Holding it can lower a cyber premium, unlock cover that would otherwise be declined for a small firm, and — increasingly — is written into policy conditions: if the wording says you'll keep supported software and MFA on cloud accounts and you don't, a claim can be reduced or refused. The certificate is your evidence that you did.</p>

<h2>What the free cover doesn't do</h2>
<p>It won't cover business interruption, ransomware payments, funds transfer fraud or the cost of rebuilding systems — the losses that actually close small businesses. £25,000 disappears quickly in a real incident. Treat the included policy as a floor and, if you handle customer data, hold client money or depend on your systems to trade, talk to a broker about a standalone cyber policy. Many will ask for the certificate first; a few will insist on Cyber Essentials Plus.</p>

<h2>Certificate first, then the broker conversation</h2>
<p>The sensible order is: certify, collect the free cover, then take the certificate to your insurance broker and ask what it does to your premiums and cover options. Brokers we work with report the conversation goes very differently when the certificate is already on the table. If you're a broker yourself, <a href="/insurance-brokers">here's how we work with you</a>.</p>

<h2>Keep it continuous</h2>
<p>The insurance runs with the certificate, so a gap in certification is a gap in cover. Start <a href="/guides/cyber-essentials-renewal.html">renewal</a> six weeks before expiry and the badge, the register entry and the policy all stay unbroken. What the certificate itself costs is in <a href="/guides/cyber-essentials-cost.html">our cost guide</a>.</p>
"""

ISO = """<h2>The short answer</h2>
<p>Cyber Essentials is a fixed set of five technical controls, self-assessed, certified in days for a few hundred pounds, and aimed at stopping common attacks. ISO 27001 is a management system for information security, independently audited over months, costing from the low tens of thousands, and aimed at proving you govern security as a business discipline. They are not rivals: most organisations that hold ISO 27001 hold Cyber Essentials too, and nearly everyone should start with Cyber Essentials.</p>

<h2>Side by side</h2>
<table>
  <tr><th></th><th>Cyber Essentials</th><th>ISO 27001</th></tr>
  <tr><td>What it is</td><td>Five technical controls, pass/fail</td><td>An information security management system (ISMS) with 93 controls to consider</td></tr>
  <tr><td>Who checks</td><td>Self-assessment reviewed by a certification body (Plus adds a hands-on audit)</td><td>External audit by an accredited certification body, then annual surveillance audits</td></tr>
  <tr><td>Time to certify</td><td>Days to a few weeks</td><td>Six to twelve months typically</td></tr>
  <tr><td>Typical cost, small business</td><td>A few hundred pounds; low thousands for Plus</td><td>£10,000–£40,000 in year one including consultancy, plus ongoing audit fees</td></tr>
  <tr><td>Scope</td><td>Devices, networks and accounts</td><td>People, processes, suppliers, physical security and technology</td></tr>
  <tr><td>Validity</td><td>12 months</td><td>3 years, with annual audits</td></tr>
  <tr><td>Who asks for it</td><td>UK public sector, insurers, most supply chains</td><td>Large corporates, regulated sectors, international clients</td></tr>
  <tr><td>Recognised</td><td>UK</td><td>Worldwide</td></tr>
</table>

<h2>When Cyber Essentials is the right answer</h2>
<p>You're a UK small or medium business, you've been asked for it by a customer, a tender, a framework or an insurer, and you want the common attacks stopped without a governance programme. It's also the sensible first step even if ISO 27001 is the destination: the five controls are a subset of what an ISO auditor will expect, and a pass gets the free insurance and the badge while the longer project runs.</p>

<h2>When ISO 27001 is the right answer</h2>
<p>You sell to large organisations that ask for it in their supplier questionnaires, you operate internationally, you're in a regulated sector, or a contract is conditional on it. ISO 27001 is what a buyer wants when they need to know you'll <em>keep</em> being secure — that there's a process, an owner, risk assessments and an audit trail — not just that your laptops were patched on the day you certified.</p>

<h2>What sits in between</h2>
<p>If Cyber Essentials feels thin and ISO 27001 feels like too much, there is a middle step: <a href="/guides/iasme-cyber-assurance.html">IASME Cyber Assurance</a>, which adds governance, policies, risk assessment and GDPR to the Cyber Essentials controls at a fraction of ISO's cost and is recognised by an increasing number of UK buyers. And Cyber Essentials Plus — the same controls, verified hands-on by an assessor — is often what a buyer actually wants when they say "something more than basic Cyber Essentials". <a href="/guides/cyber-essentials-vs-plus.html">The Plus comparison is here.</a></p>

<h2>The practical order</h2>
<p>Cyber Essentials now, Plus if a buyer or insurer asks for it, IASME Cyber Assurance if you want governance without the ISO price tag, ISO 27001 when a contract or market genuinely requires it. Each builds on the last; none is wasted. What Cyber Essentials involves and costs is in <a href="/guides/how-to-get-cyber-essentials.html">how to get certified</a>.</p>
"""

make('cyber-essentials-logo', 'Cyber Essentials logo: where it comes from, where you can use it, and when it must come down',
     'The Cyber Essentials logo is issued by IASME with your certificate, is free, and may be used for exactly twelve months. Where to put it, what not to do with it, and how to prove it is real.',
     'The Cyber Essentials logo — how to get it and use it properly',
     'It arrives with your certificate, it costs nothing, and it has a twelve-month clock on it. Here is where the logo comes from, where you are allowed to use it, the rules that catch people out, and how to make the badge prove itself.',
     '4', LOGO,
     'Want the badge on your website by next month?',
     'Fixed price, current-rules review before submission, fixes included, resubmission covered. Pass, and the logo pack lands with the certificate.')

make('cyber-essentials-checklist', 'Cyber Essentials checklist: the five controls, line by line, with the two auto-fails marked',
     'A one-screen Cyber Essentials checklist covering all five controls — firewalls, secure configuration, updates, access control and malware — plus scope, what the questionnaire asks for, and how long it takes.',
     'The Cyber Essentials checklist',
     'Five controls, every line either true or false for every device in scope. Work through this before you open the portal and the questionnaire becomes an afternoon\u2019s work. The two auto-fail rules are marked.',
     '5', CHECKLIST,
     'Checklist done? We\u2019ll turn it into a pass.',
     'Fixed price, current-rules review before submission, fixes included, resubmission covered. Send us your ticked checklist and we\u2019ll tell you honestly whether you\u2019re ready.',
     keep_capture=True,
     capture_title='Get the checklist as a PDF \u2014 free',
     capture_p='The five controls and the scope check on one page, formatted to tick through and file with your submission. We\u2019ll also tell you honestly whether anything on it looks like a trap for your setup.')

make('cyber-essentials-insurance', 'Cyber Essentials insurance: the free £25,000 cover, who qualifies, and what it doesn\u2019t do',
     'Pass Cyber Essentials with turnover under £20m and you get £25,000 of cyber liability insurance free for the certificate year. What it covers, how to claim it, why insurers ask for the certificate, and its limits.',
     'Cyber Essentials and insurance — the free cover, and what it means for your premiums',
     'A pass comes with £25,000 of cyber liability insurance at no cost for the twelve months of the certificate. Here is what the cover includes, who qualifies, why underwriters care about the certificate, and where it stops.',
     '4', INSURANCE,
     'Certify, collect the cover, then talk to your broker.',
     'Fixed price, current-rules review before submission, fixes included, resubmission covered. We\u2019ll make sure the insurance opt-in is ticked so the cover actually arrives.')

make('iso-27001-vs-cyber-essentials', 'ISO 27001 vs Cyber Essentials: the difference, the cost, and which one you actually need',
     'Cyber Essentials is five technical controls certified in days for a few hundred pounds; ISO 27001 is an audited management system taking months and tens of thousands. Side-by-side comparison and the practical order to do them in.',
     'ISO 27001 vs Cyber Essentials',
     'One is a fixed set of technical controls you can certify this month; the other is a security management system audited over the better part of a year. They answer different questions from different buyers. Here is the comparison and the sensible order.',
     '5', ISO,
     'Start with the one you can finish this month.',
     'Fixed price, current-rules review before submission, fixes included, resubmission covered. If ISO 27001 is where you\u2019re heading, Cyber Essentials first is the right foundation.')

# register in sitemap and guides index
s = open('sitemap.xml').read()
anchor = '  <url><loc>https://passcyber.co.uk/guides/cyber-essentials-renewal</loc>'
add = ''.join('  <url><loc>https://passcyber.co.uk/guides/%s</loc><lastmod>2026-09-13</lastmod><priority>0.9</priority></url>\n' % x
              for x in ['cyber-essentials-checklist', 'cyber-essentials-logo', 'cyber-essentials-insurance', 'iso-27001-vs-cyber-essentials'])
if 'cyber-essentials-checklist' not in s:
    open('sitemap.xml', 'w').write(s.replace(anchor, add + anchor, 1))

g = open('guides/index.html', encoding='utf-8').read()
cards = '''    <a class="card" href="/guides/cyber-essentials-checklist.html">
      <span class="k">Before you apply</span>
      <h3>The Cyber Essentials checklist</h3>
      <p>All five controls on one screen, line by line, with the two auto-fail rules marked and the scope check that catches most failures before the questionnaire does.</p>
      <span class="go">Read &rsaquo;</span>
    </a>

    <a class="card" href="/guides/cyber-essentials-logo.html">
      <span class="k">After you pass</span>
      <h3>The Cyber Essentials logo: getting it and using it properly</h3>
      <p>Where the badge comes from, where you can use it, the twelve-month rule, what not to do with it, and how to make it prove itself to anyone checking.</p>
      <span class="go">Read &rsaquo;</span>
    </a>

    <a class="card" href="/guides/cyber-essentials-insurance.html">
      <span class="k">Included with a pass</span>
      <h3>The free £25,000 insurance, and what it means for your premiums</h3>
      <p>Who qualifies for the included cyber liability cover, what it does and doesn't cover, and why underwriters now ask for the certificate.</p>
      <span class="go">Read &rsaquo;</span>
    </a>

    <a class="card" href="/guides/iso-27001-vs-cyber-essentials.html">
      <span class="k">Which standard</span>
      <h3>ISO 27001 vs Cyber Essentials</h3>
      <p>Days versus months, hundreds versus tens of thousands, technical controls versus a management system — and the sensible order to do them in.</p>
      <span class="go">Read &rsaquo;</span>
    </a>

'''
anchor2 = '    <a class="card" href="/guides/cyber-essentials-renewal.html">'
if 'cyber-essentials-checklist' not in g:
    open('guides/index.html', 'w', encoding='utf-8').write(g.replace(anchor2, cards + anchor2, 1))
