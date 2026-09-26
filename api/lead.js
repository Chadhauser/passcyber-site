// api/lead.js — receives Cyber Essentials readiness check results
// Set these environment variables in the Vercel project:
//   RESEND_API_KEY       from resend.com
//   NOTIFY_EMAIL         where leads land, e.g. hello@passcyber.co.uk
//   FROM_EMAIL           a verified sender on passcyber.co.uk
//   ALLOWED_ORIGIN       https://passcyber.co.uk
//   SUPABASE_URL         optional, to keep storing in funnel_signups
//   SUPABASE_SERVICE_KEY optional, service role key — server side only

const RATE = new Map();
const WINDOW_MS = 60 * 60 * 1000;
const MAX_PER_IP = 8;

function clean(v, max) {
  return String(v == null ? '' : v).replace(/[\u0000-\u001F\u007F]/g, '').trim().slice(0, max);
}
function validEmail(e) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e) && e.length <= 254;
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', process.env.ALLOWED_ORIGIN || 'https://passcyber.co.uk');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const now = Date.now();
  const hits = (RATE.get(ip) || []).filter(t => now - t < WINDOW_MS);
  if (hits.length >= MAX_PER_IP) return res.status(429).json({ error: 'Too many submissions' });
  hits.push(now);
  RATE.set(ip, hits);

  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); } catch { return res.status(400).json({ error: 'Bad request' }); }
  }
  if (!body || typeof body !== 'object') return res.status(400).json({ error: 'Bad request' });

  const email = clean(body.email, 254).toLowerCase();
  if (!validEmail(email)) return res.status(400).json({ error: 'A valid email is required' });

  const source = clean(body.source, 180);
  const score = Number.isFinite(Number(body.score)) ? Number(body.score) : null;
  const band = clean(body.band, 40);
  const flags = (body.flags && typeof body.flags === 'object') ? body.flags : {};

  const problems = [];
  if (flags.mfa) problems.push('multi-factor authentication');
  if (flags.patch) problems.push('patching within 14 days');
  if (flags.eol) problems.push('unsupported software still in use');
  if (flags.byod) problems.push('personal devices in scope');

  const results = { emailed: false, stored: false };

  if (process.env.RESEND_API_KEY && process.env.NOTIFY_EMAIL && process.env.FROM_EMAIL) {
    const text = [
      `New Cyber Essentials readiness check completed.`,
      ``,
      `Email:    ${email}`,
      `Score:    ${score === null ? 'n/a' : score}`,
      `Band:     ${band || 'n/a'}`,
      `Problems: ${problems.length ? problems.join(', ') : 'none flagged'}`,
      ``,
      `Source:   ${source}`,
      `Time:     ${new Date().toISOString()}`,
      ``,
      `Reply to this email to reach them directly.`
    ].join('\n');

    try {
      const r = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          from: process.env.FROM_EMAIL,
          to: process.env.NOTIFY_EMAIL,
          reply_to: email,
          subject: `CE readiness check - ${band || 'result'}${score === null ? '' : ' (' + score + ')'} - ${email}`,
          text
        })
      });
      results.emailed = r.ok;
    } catch (e) {
      results.emailed = false;
    }
  }

  if (process.env.SUPABASE_URL && process.env.SUPABASE_SERVICE_KEY) {
    try {
      const r = await fetch(`${process.env.SUPABASE_URL}/rest/v1/funnel_signups`, {
        method: 'POST',
        headers: {
          'apikey': process.env.SUPABASE_SERVICE_KEY,
          'Authorization': `Bearer ${process.env.SUPABASE_SERVICE_KEY}`,
          'Content-Type': 'application/json',
          'Content-Profile': 'sheetmtd',
          'Prefer': 'return=minimal'
        },
        body: JSON.stringify({ email, source })
      });
      results.stored = r.ok;
    } catch (e) {
      results.stored = false;
    }
  }

  if (!results.emailed && !results.stored) {
    console.error('LEAD NOT CAPTURED', { email, source, score, band });
    return res.status(502).json({ error: 'Could not record that' });
  }

  return res.status(200).json({ ok: true });
}
