# mess-reminder

Sends mess meal reminders (Breakfast, Lunch, Snacks, Dinner) on a schedule via GitHub Actions.

## Notifications

Notifications are sent to:

- **ntfy.sh** — set the `NTFY_TOPIC` repo secret to your ntfy topic.
- **WhatsApp** (via [CallMeBot](https://www.callmebot.com/blog/free-api-whatsapp-messages/)) — optional, skipped automatically if not configured.

### WhatsApp setup (CallMeBot)

1. Save `+34 621 71 08 61` as a contact on the phone you want reminders sent to.
2. Send it the WhatsApp message: `I allow callmebot to send me messages`.
3. Wait for the reply containing your API key.
4. Add two repo secrets (Settings → Secrets and variables → Actions):
   - `CALLMEBOT_PHONE` — your WhatsApp number in international format (e.g. `919876543210`).
   - `CALLMEBOT_APIKEY` — the API key from the activation reply.

If either secret is missing, the workflows still run and simply skip the WhatsApp step.
