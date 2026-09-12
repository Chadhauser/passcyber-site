import re, json, html

TPL = 'guides/cyber-essentials-renewal.html'

def make(slug, title, desc, h1, stand, reading, prose, cta_h2, cta_p, rel):
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
    s = s[:a] + '\n\n' + prose + '\n' + s[b:]
    s = re.sub(r'<script>\s*document\.getElementById\(\'rnform\'\).*?</script>', '', s, 1, flags=re.S)
    s = re.sub(r'(<div class="cta">\s*<div class="t">PassCyber</div>\s*)<h2>.*?</h2>\s*<p>.*?</p>',
               r'\g<1>' + '<h2>%s</h2>\n  <p>%s</p>' % (cta_h2, cta_p), s, 1, flags=re.S)
    s = re.sub(r'(<div class="related">\s*<p class="rt">Related guides</p>\s*<ul>).*?(</ul>)',
               lambda m: m.group(1) + '\n' + ''.join('    <li><a href="/guides/%s.html">%s</a></li>\n' % r for r in rel) + '  ' + m.group(2), s, 1, flags=re.S)
    open('guides/' + slug + '.html', 'w', encoding='utf-8').write(s)

SCOPE = """<h2>The short answer</h2>
<p>Cyber Essentials scope is every device and account that can reach your business data or your business network: laptops, desktops, servers, phones and tablets \u2014 company-owned or personal \u2014 plus your firewalls, routers and cloud services. The default is "whole organisation", and that is what buyers, insurers and the free insurance all expect. You can certify a smaller scope, but it must be a separately networked sub-set, it must be declared on the certificate, and it usually causes more trouble than it saves.</p>

<h2>What is always in scope</h2>
<ul>
  <li><strong>Every user device</strong> that accesses organisational data or services \u2014 including home-working laptops and any personal phone with work email on it. <a href="/guides/cyber-essentials-scope-personal-devices.html">Personal devices are the usual surprise.</a></li>
  <li><strong>Every server</strong> \u2014 on premises or hosted \u2014 that you administer.</li>
  <li><strong>Boundary devices</strong> \u2014 the firewalls and routers between your network and the internet. In a home or serviced office that includes kit you don\u2019t own; <a href="/guides/cyber-essentials-serviced-office.html">here\u2019s how that\u2019s handled</a>.</li>
  <li><strong>Cloud services</strong> \u2014 Microsoft 365, Google Workspace, Xero, your CRM, anything with a login that holds business data. You don\u2019t patch the provider\u2019s servers, but the MFA and account controls are yours to answer for.</li>
  <li><strong>Accounts</strong> \u2014 every user and admin account on the above.</li>
</ul>

<h2>What is out of scope</h2>
<ul>
  <li>Devices that cannot reach business data or the business network at all \u2014 a till on its own isolated network, a machine-tool controller with no internet access.</li>
  <li>Services where you are purely a consumer with no admin rights and no business data \u2014 but be honest: a shared spreadsheet in a personal Dropbox is business data.</li>
  <li>Anything you have deliberately walled off into a separate network with its own boundary, <em>and</em> excluded on the application. Rare in a small business, and it must be real segmentation, not a line on a form.</li>
</ul>

<h2>The home-working question</h2>
<p>A home router is not in scope if the laptop uses its own software firewall and the business runs no services on the home network. The laptop, however, is fully in scope \u2014 supported operating system, patched within 14 days, MFA on the cloud services it reaches. The same goes for the director\u2019s personal machine used "just for email" at weekends. This is where most scope arguments end: if it touches the data, it\u2019s in.</p>

<h2>Whole organisation or a sub-set?</h2>
<p>Certify the whole organisation unless you have a specific, defensible reason not to. Three things push you that way:</p>
<ul>
  <li><strong>Buyers assume it.</strong> A certificate scoped to "head office only" invites the question "what about the rest?" on every tender.</li>
  <li><strong>The free insurance requires it.</strong> The <a href="/guides/cyber-essentials-insurance.html">£25,000 cyber liability cover</a> is only available for whole-organisation certification.</li>
  <li><strong>Sub-sets are hard to prove.</strong> You must show the excluded part is on a separately controlled network with its own firewall. If a laptop can wander between the two, it isn\u2019t separate.</li>
</ul>
<p>The legitimate case for a sub-set is a large organisation with a genuinely separate division, or an old estate you\u2019re decommissioning that you can isolate until it\u2019s gone. For a business under fifty people it almost never applies \u2014 and the certification fee is banded by the size of the organisation, not the scope, so a narrow scope doesn\u2019t make it cheaper.</p>

<h2>How to write the scope on the application</h2>
<p>Name the organisation, state "whole organisation", and list the counts the questionnaire asks for: user devices by operating system and version, servers and what they run, mobile devices, cloud services, and the location(s) they operate from. If you have excluded anything, say exactly what and describe the network boundary that separates it. Vague scopes get sent back with questions, which costs you days; a scope that reads like an inventory sails through. The <a href="/guides/cyber-essentials-checklist.html">checklist</a> lists everything you need to have counted before you start.</p>

<h2>Scope drift is what fails renewals</h2>
<p>New starter, new laptop, new cloud tool, tablet bought for the workshop: all in scope from the day they arrive, all invisible to last year\u2019s answers. Keep a one-page asset list and update it as things change, and <a href="/guides/cyber-essentials-renewal.html">renewal</a> becomes a re-check rather than a rediscovery.</p>
"""

make('cyber-essentials-scope', 'Cyber Essentials scope: what\u2019s in, what\u2019s out, and why "whole organisation" is almost always right',
     'Cyber Essentials scope covers every device and account that can reach business data or the business network \u2014 home laptops and personal phones included. What is in, what is out, whole organisation versus a sub-set, and how to write the scope so the application isn\u2019t bounced.',
     'Cyber Essentials scope \u2014 what\u2019s in, what\u2019s out',
     'Every device and account that can reach your data or your network is in. Here is the full picture: the home-working laptop, the personal phone, the serviced-office router, the cloud services, and why certifying a sub-set is rarely the shortcut it looks like.',
     '5', SCOPE,
     'Not sure what\u2019s in scope? Ask before you apply.',
     'Fixed price, current-rules review before submission, fixes included, resubmission covered. We\u2019ll agree the scope with you first, so the application doesn\u2019t come back with questions.',
     [('cyber-essentials-scope-personal-devices', 'Are personal phones and home laptops in scope?'),
      ('cyber-essentials-serviced-office', 'Serviced offices and hot desks: whose firewall?'),
      ('cyber-essentials-checklist', 'The Cyber Essentials checklist'),
      ('cyber-essentials-application-details', 'The details that bounce an application'),
      ('cyber-essentials-cost', 'How much does Cyber Essentials cost?'),
      ('cyber-essentials-insurance', 'The free \u00a325,000 insurance that comes with a pass')])

f = 'guides/verify-cyber-essentials-certificate.html'
s = open(f, encoding='utf-8').read()
if 'Cyber Essentials certificate check' not in s:
    s = re.sub(r'<title>.*?</title>', '<title>Cyber Essentials certificate check: how to look up any company on the register (free) | PassCyber</title>', s, 1, flags=re.S)
    s = re.sub(r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="Cyber Essentials certificate check: how to look up any company on the register (free)">', s, 1)
    s = re.sub(r'"headline":"[^"]*"', '"headline":"Cyber Essentials certificate check: how to look up any company on the register (free)"', s, 1)
    s = re.sub(r'"dateModified":"[^"]+"', '"dateModified":"2026-09-13"', s, 1)
    s = re.sub(r'<h1>.*?</h1>', '<h1>Cyber Essentials certificate check \u2014 how to look up any company on the register</h1>', s, 1, flags=re.S)
    short = """<h2>The short answer</h2>
<p>Search the company\u2019s name on the official IASME Cyber Essentials register \u2014 it\u2019s free, public and needs no login. If the company appears with a certificate that hasn\u2019t expired, they hold it; if they don\u2019t appear, they don\u2019t, whatever their website says. A certificate is valid for twelve months from the date shown. Everything else on this page is how to read the result and what to do about a supplier who has lapsed.</p>

"""
    s = s.replace('<h2>The one place that counts</h2>', short + '<h2>The one place that counts</h2>', 1)
    open(f, 'w', encoding='utf-8').write(s)

sm = open('sitemap.xml').read()
anchor = '  <url><loc>https://passcyber.co.uk/guides/cyber-essentials-renewal</loc>'
if 'guides/cyber-essentials-scope<' not in sm:
    sm = sm.replace(anchor, '  <url><loc>https://passcyber.co.uk/guides/cyber-essentials-scope</loc><lastmod>2026-09-13</lastmod><priority>0.9</priority></url>\n' + anchor, 1)
sm = re.sub(r'(<loc>https://passcyber.co.uk/guides/verify-cyber-essentials-certificate</loc><lastmod>)[^<]+', r'\g<1>2026-09-13', sm, 1)
open('sitemap.xml', 'w').write(sm)

g = open('guides/index.html', encoding='utf-8').read()
card = '''    <a class="card" href="/guides/cyber-essentials-scope.html">
      <span class="k">Before you apply</span>
      <h3>Scope: what\u2019s in, what\u2019s out</h3>
      <p>Every device and account that can reach your data is in \u2014 home laptops and personal phones included. Whole organisation versus a sub-set, and how to write the scope so it isn\u2019t bounced.</p>
      <span class="go">Read &rsaquo;</span>
    </a>

'''
anchor2 = '    <a class="card" href="/guides/cyber-essentials-checklist.html">'
if 'cyber-essentials-scope.html' not in g:
    open('guides/index.html', 'w', encoding='utf-8').write(g.replace(anchor2, card + anchor2, 1))
