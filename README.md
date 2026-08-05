# PassCyber — passcyber.co.uk

Static site. No build step. `index.html` (landing) + `check.html` (CE Readiness Check, served at `/check` via cleanUrls).

The free Readiness Check is the lead magnet — scores a business against the five CE controls and the two 2026 auto-fail traps (cloud MFA, 14-day patching), then captures the lead by email.

## Deploy (Vercel)
1. vercel.com → Add New → Project → Import `Chadhauser/passcyber-site` → Deploy (Other, no build command, output dir root).
2. Settings → Domains → add `passcyber.co.uk` and `www.passcyber.co.uk`.

## DNS (Namecheap → passcyber.co.uk → Advanced DNS)
| Type | Host | Value |
|------|------|-------|
| A | @ | 76.76.21.21 |
| CNAME | www | cname.vercel-dns.com |

## Mailbox
`hello@passcyber.co.uk` is hard-coded (CONTACT_EMAIL in check.html, mailto in index.html). Set up the mailbox like Granton when ready.

## CE facts baked in (verified Aug 2026)
Five controls: firewalls, secure configuration, user access control, malware protection, security update management. Danzell question set + Requirements v3.3. Two auto-fails from 26 Apr 2026: cloud MFA missing, and high-risk updates not applied within 14 days — either fails outright. IASME fee £320–600+VAT; PassCyber pitch £500–800 done-for-you.
