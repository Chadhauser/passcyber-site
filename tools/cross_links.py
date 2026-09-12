import re

G = '/guides/'
T = {
 'how-to-get-cyber-essentials': 'How to get Cyber Essentials, start to finish',
 'cyber-essentials-cost': 'How much does Cyber Essentials cost?',
 'cyber-essentials-checklist': 'The Cyber Essentials checklist',
 'cyber-essentials-questionnaire-answers': 'How to answer the questionnaire',
 'cyber-essentials-application-details': 'The details that bounce an application',
 'cyber-essentials-plus-cost': 'What Cyber Essentials Plus costs',
 'cyber-essentials-vs-plus': 'Cyber Essentials or Cyber Essentials Plus?',
 'failed-cyber-essentials': 'Failed Cyber Essentials? What happens next',
 'why-cyber-essentials-applications-fail': 'Why applications fail',
 'cyber-essentials-mfa-requirements': 'The MFA rule that fails whole applications',
 'windows-10-cyber-essentials': 'Still on Windows 10? That\u2019s a fail now',
 'cyber-essentials-scope-personal-devices': 'Are personal phones and home laptops in scope?',
 'cyber-essentials-serviced-office': 'Serviced offices and hot desks: whose firewall?',
 'cyber-essentials-renewal': 'Renewal: fresh rules, no lock-in',
 'cyber-essentials-logo': 'The Cyber Essentials logo: getting and using it',
 'cyber-essentials-insurance': 'The free \u00a325,000 insurance that comes with a pass',
 'verify-cyber-essentials-certificate': 'How to check a company holds Cyber Essentials',
 'iso-27001-vs-cyber-essentials': 'ISO 27001 vs Cyber Essentials',
 'iasme-cyber-assurance': 'IASME Cyber Assurance, explained',
 'how-to-choose-cyber-essentials-certification-body': 'How to choose a certification body',
 'cyber-essentials-schools': 'Cyber Essentials for schools and trusts',
 'cyber-security-services-small-business': 'Buying cyber security services as a small business',
 'cyber-security-policy-template': 'A cyber security policy template you can use',
}

BASICS = ['how-to-get-cyber-essentials', 'cyber-essentials-cost', 'cyber-essentials-checklist', 'cyber-essentials-questionnaire-answers', 'cyber-essentials-application-details']
PLUS = ['cyber-essentials-vs-plus', 'cyber-essentials-plus-cost']
FIX = ['why-cyber-essentials-applications-fail', 'failed-cyber-essentials', 'cyber-essentials-mfa-requirements', 'windows-10-cyber-essentials', 'cyber-essentials-scope-personal-devices', 'cyber-essentials-serviced-office']
AFTER = ['cyber-essentials-renewal', 'cyber-essentials-logo', 'cyber-essentials-insurance', 'verify-cyber-essentials-certificate']
STANDARDS = ['iso-27001-vs-cyber-essentials', 'iasme-cyber-assurance', 'how-to-choose-cyber-essentials-certification-body', 'cyber-essentials-schools', 'cyber-security-services-small-business', 'cyber-security-policy-template']

def pick(cluster, me, n, extras):
    i = cluster.index(me) if me in cluster else 0
    ring = cluster[i+1:] + cluster[:i]
    out = [x for x in ring if x != me][:n]
    for e in extras:
        if e != me and e not in out and len(out) < 6:
            out.append(e)
    return out

REL = {}
for p in BASICS:
    REL[p] = pick(BASICS, p, 3, ['why-cyber-essentials-applications-fail', 'cyber-essentials-vs-plus', 'cyber-essentials-renewal'])
for p in PLUS:
    REL[p] = pick(PLUS, p, 1, ['cyber-essentials-cost', 'how-to-get-cyber-essentials', 'iso-27001-vs-cyber-essentials', 'cyber-essentials-insurance', 'cyber-essentials-checklist'])
for p in FIX:
    REL[p] = pick(FIX, p, 3, ['cyber-essentials-checklist', 'how-to-get-cyber-essentials', 'cyber-essentials-cost'])
for p in AFTER:
    REL[p] = pick(AFTER, p, 3, ['cyber-essentials-cost', 'how-to-get-cyber-essentials', 'cyber-essentials-checklist'])
for p in STANDARDS:
    REL[p] = pick(STANDARDS, p, 3, ['cyber-essentials-cost', 'how-to-get-cyber-essentials', 'cyber-essentials-vs-plus'])

CHANNEL = {
 'msp': ['cyber-essentials-checklist', 'cyber-essentials-mfa-requirements', 'windows-10-cyber-essentials', 'cyber-essentials-renewal', 'cyber-essentials-cost', 'how-to-choose-cyber-essentials-certification-body'],
 'insurance-brokers': ['cyber-essentials-insurance', 'cyber-essentials-cost', 'cyber-essentials-vs-plus', 'verify-cyber-essentials-certificate', 'how-to-get-cyber-essentials', 'cyber-essentials-renewal'],
}

STYLE = '.related{margin:40px 0 8px;padding:22px 24px;border:1px solid rgba(0,0,0,.1);border-radius:8px;background:rgba(0,0,0,.02)}.related .rt{font-family:inherit;font-size:12px;letter-spacing:.14em;text-transform:uppercase;opacity:.7;margin:0 0 10px}.related ul{list-style:none;margin:0;padding:0;columns:2;column-gap:28px}.related li{break-inside:avoid;margin:0 0 8px;font-size:16px}.related a{text-decoration:none;border-bottom:1px solid rgba(0,0,0,.25)}@media(max-width:600px){.related ul{columns:1}}'

def apply(path, rel):
    s = open(path, encoding='utf-8').read()
    if 'class="related"' in s or '<div class="cta">' not in s:
        return
    block = '<div class="related">\n  <p class="rt">Related guides</p>\n  <ul>\n' + ''.join('    <li><a href="%s%s.html">%s</a></li>\n' % (G, r, T[r]) for r in rel) + '  </ul>\n</div>\n\n'
    s = s.replace('<div class="cta">', block + '<div class="cta">', 1)
    s = s.replace('</style>', STYLE + '\n</style>', 1)
    open(path, 'w', encoding='utf-8').write(s)

for slug, rel in REL.items():
    apply('guides/' + slug + '.html', rel)
for slug, rel in CHANNEL.items():
    apply(slug + '.html', rel)
