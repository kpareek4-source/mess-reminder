# mess-reminder

Sends mess meal reminders (Breakfast, Lunch, Snacks, Dinner) on a schedule via GitHub Actions.

## Notifications

Notifications are sent to:

- **ntfy.sh** — set the `NTFY_TOPIC` repo secret to your ntfy topic.
- **WhatsApp** (via [Twilio](https://www.twilio.com/whatsapp)) — optional, skipped automatically if not configured.

### WhatsApp setup (Twilio)

1. Create a free [Twilio](https://www.twilio.com/try-twilio) account.
2. In the Twilio Console, open **Messaging → Try it out → Send a WhatsApp message** to reach the WhatsApp sandbox. Note the sandbox number and the `join <your-code>` phrase shown there.
3. From the WhatsApp account you want reminders sent to, send that `join <your-code>` message to the sandbox number.
4. Copy your **Account SID** and **Auth Token** from the Console dashboard.
5. Add four repo secrets (Settings → Secrets and variables → Actions):
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM` — the sandbox number in international format, no `whatsapp:` prefix (e.g. `14155238886`).
   - `TWILIO_WHATSAPP_TO` — your WhatsApp number in international format (e.g. `919876543210`).

If any of these secrets are missing, the workflows still run and simply skip the WhatsApp step.

The free sandbox session expires after a few days of inactivity — if messages stop arriving, resend the `join <your-code>` message to reactivate it.
