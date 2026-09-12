import re,os,json,html,sys
def attr(s,pat):
    m=re.search(pat,s,re.I|re.S); return html.unescape(m.group(1)).strip() if m else ''
def process(path,site,base,org_ld,page_ld):
    s=open(path,encoding='utf-8').read(); orig=s
    title=attr(s,r'<title>(.*?)</title>'); desc=attr(s,r'<meta name="description" content="(.*?)"')
    canon=attr(s,r'<link rel="canonical" href="(.*?)"')
    rel=os.path.relpath(path,site)
    if not canon:
        url=base+'/' if rel=='index.html' else base+'/'+rel[:-5]
        canon=url
        s=s.replace('<link rel="icon"','<link rel="canonical" href="%s">\n<link rel="icon"'%url,1)
    ins=[]
    if 'og:title' not in s:
        typ='website' if rel=='index.html' else 'article'
        ins.append('<meta property="og:type" content="%s">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n<meta property="og:site_name" content="%s">\n<meta name="twitter:card" content="summary">'%(typ,html.escape(title,quote=True),html.escape(desc,quote=True),canon,org_ld['name']))
    if 'ld+json' not in s and rel!='privacy.html':
        ld = org_ld if rel=='index.html' else page_ld(title,desc,canon)
        ins.append('<script type="application/ld+json">%s</script>'%json.dumps(ld,ensure_ascii=False))
    if ins:
        s=s.replace('</head>','\n'.join(ins)+'\n</head>',1)
    if s!=orig: open(path,'w',encoding='utf-8').write(s); return rel
granton_org={"@context":"https://schema.org","@type":"FinancialService","name":"Granton Finance","url":"https://granton.finance/","email":"hello@granton.finance","description":"Commercial finance broker arranging business acquisition, management buyout, succession, bridging and invoice finance for UK owner-managed businesses. FIBA member FIB42279.","areaServed":"GB","parentOrganization":{"@type":"Organization","name":"Edwards Bros (Spaldwick) Ltd","url":"https://www.edwardsbros.co.uk/"},"founder":{"@type":"Person","name":"Peter Edwards","honorificSuffix":"ACMA CGMA","url":"https://www.edwardsbros.co.uk/peter-edwards.html"},"memberOf":{"@type":"Organization","name":"FIBA - Financial Intermediary and Broker Association"},"knowsAbout":["Business acquisition finance","Management buyout funding","Bridging loans","Invoice finance","Succession finance"]}
pass_org={"@context":"https://schema.org","@type":"ProfessionalService","name":"PassCyber","url":"https://passcyber.co.uk/","description":"Cyber Essentials certification done for you at one all-in price including the IASME certification fee. If it does not pass, we fix it and resubmit free.","areaServed":"GB","parentOrganization":{"@type":"Organization","name":"Edwards Bros (Spaldwick) Ltd","url":"https://www.edwardsbros.co.uk/"},"makesOffer":{"@type":"Offer","itemOffered":{"@type":"Service","name":"Cyber Essentials certification, done for you","serviceType":"Cyber Essentials certification"}},"knowsAbout":["Cyber Essentials","Cyber Essentials Plus","IASME Cyber Assurance"]}
def mk(pubname,puburl):
    return lambda t,d,u:{"@context":"https://schema.org","@type":"WebPage","name":t,"description":d,"url":u,"isPartOf":{"@type":"WebSite","name":pubname,"url":puburl},"publisher":{"@type":"Organization","name":"Edwards Bros (Spaldwick) Ltd","url":"https://www.edwardsbros.co.uk/"}}
site,base=sys.argv[1],sys.argv[2]
if 'granton' in base:
    p=os.path.join(site,'index.html'); t=open(p,encoding='utf-8').read()
    old='Granton Finance arranges business acquisition, management buyout and succession finance. We think like the credit committee: your deal arrives at\u2026'
    new='Granton Finance arranges business acquisition, management buyout, succession, bridging and invoice finance for UK owner-managed businesses. Chartered accountant led: we pre-underwrite your deal so it arrives at the lender already answering the credit committee\'s questions.'
    if old in t: open(p,'w',encoding='utf-8').write(t.replace(old,new))
org,pl=(granton_org,mk("Granton Finance","https://granton.finance/")) if 'granton' in base else (pass_org,mk("PassCyber","https://passcyber.co.uk/"))
changed=[]
for root,_,files in os.walk(site):
    if '.git' in root or 'tools' in root: continue
    for f in files:
        if f.endswith('.html') and not f.startswith('google'):
            r=process(os.path.join(root,f),site,base,org,pl)
            if r: changed.append(r)
print('\n'.join(sorted(changed)))
