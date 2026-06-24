\# Release Checklist



Use this checklist before creating a production release.



\## 1. Local Verification



\* \[ ] Backend tests pass with `pytest`

\* \[ ] Frontend build passes with `npm run build`

\* \[ ] Playwright tests pass with `npm run test:e2e`

\* \[ ] Backend production smoke test passes with `python scripts/production\_smoke.py`

\* \[ ] No `.env` files are tracked

\* \[ ] No database dumps are tracked

\* \[ ] No screenshots contain credentials

\* \[ ] No logs contain secrets



\## 2. Production Backend Verification



\* \[ ] `/api/v1/health` returns healthy

\* \[ ] `/api/v1/ready` returns database connected

\* \[ ] `/api/v1/profile` returns the public profile

\* \[ ] Render service status is live

\* \[ ] Render logs show no repeated errors

\* \[ ] Production API custom domain works: `https://api.bajiraosalunke.com`

\* \[ ] Production API docs are disabled



\## 3. Production Frontend Verification



\* \[ ] Home page loads

\* \[ ] `/ai-tools` loads

\* \[ ] `/admin/login` loads

\* \[ ] Project detail page loads

\* \[ ] Research detail page loads

\* \[ ] Direct refresh works on all routes

\* \[ ] No CORS errors appear in browser console

\* \[ ] Metadata, favicon, sitemap and robots.txt load

\* \[ ] Frontend custom domain works: `https://bajiraosalunke.com`

\* \[ ] `www.bajiraosalunke.com` redirects to `bajiraosalunke.com`



\## 4. Functional Verification



\* \[ ] Contact form works

\* \[ ] Contact form saves record in database

\* \[ ] Contact form sends admin notification email

\* \[ ] Contact form sends user confirmation email

\* \[ ] Interview request form works

\* \[ ] Interview request saves record in database

\* \[ ] Interview request sends admin notification email

\* \[ ] Interview request sends user confirmation email

\* \[ ] JD matcher works

\* \[ ] Chatbot works

\* \[ ] Admin login works

\* \[ ] Admin dashboard loads

\* \[ ] Content manager loads

\* \[ ] Resume download works

\* \[ ] Project images load



\## 5. Email Verification



\* \[ ] Resend domain is verified

\* \[ ] Sender email works: `notifications@mail.bajiraosalunke.com`

\* \[ ] Admin email is correct: `bajisalunke001@gmail.com`

\* \[ ] Resend API key is configured only in Render

\* \[ ] Email notifications are enabled in production

\* \[ ] Test emails appear in Resend logs

\* \[ ] Emails are not landing in spam



\## 6. Security Verification



\* \[ ] Production `.env` values are only in Render or Vercel

\* \[ ] Admin password is not exposed

\* \[ ] Database credentials are not exposed

\* \[ ] JWT secret is not exposed

\* \[ ] Resend key is not exposed

\* \[ ] API keys are not committed to GitHub

\* \[ ] Admin pages return `X-Robots-Tag: noindex`

\* \[ ] Production API docs are disabled

\* \[ ] CORS origins contain only approved frontend domains

\* \[ ] Trusted hosts contain only approved backend hosts



\## 7. Production Environment Variables



\### Render Backend



\* \[ ] `DATABASE\_URL` is configured

\* \[ ] `JWT\_SECRET\_KEY` is configured

\* \[ ] `RESEND\_API\_KEY` is configured

\* \[ ] `EMAIL\_NOTIFICATIONS\_ENABLED=True`

\* \[ ] `EMAIL\_FROM\_ADDRESS=notifications@mail.bajiraosalunke.com`

\* \[ ] `ADMIN\_NOTIFICATION\_EMAIL=bajisalunke001@gmail.com`

\* \[ ] `PUBLIC\_FRONTEND\_URL=https://bajiraosalunke.com`

\* \[ ] `CORS\_ORIGINS` includes `https://bajiraosalunke.com`

\* \[ ] `TRUSTED\_HOSTS` includes `api.bajiraosalunke.com`



\### Vercel Frontend



\* \[ ] `VITE\_API\_BASE\_URL=https://api.bajiraosalunke.com`

\* \[ ] `VITE\_SITE\_URL=https://bajiraosalunke.com`



\## 8. Release



\* \[ ] GitHub Actions CI passes

\* \[ ] Production smoke workflow passes

\* \[ ] Version tag created

\* \[ ] GitHub release created

\* \[ ] Final production frontend checked

\* \[ ] Final production backend checked



