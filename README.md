# mess-reminder

Sends an [ntfy.sh](https://ntfy.sh) push notification 30 minutes before each mess
meal (Breakfast, Lunch, Snacks, Dinner) with the day's menu.

Each meal is a separate GitHub Actions workflow that runs `scripts/reminder.py`.

## Why an external scheduler?

GitHub Actions' built-in `schedule:` (cron) trigger is **not** reliable for
time-sensitive notifications — on low-activity/public repos it is regularly
delayed by hours. To get reminders on time, the workflows are triggered via
`workflow_dispatch` (the GitHub API) by an external cron service that fires at
the exact minute needed. API-triggered runs start almost immediately instead of
waiting in GitHub's cron queue.

## Reminder times (IST)

Notifications should fire **30 minutes before** serving time:

| Meal      | Serving time        | Reminder fires (IST) | Reminder fires (UTC) | Workflow file  |
|-----------|---------------------|----------------------|----------------------|----------------|
| Breakfast | 7:45 AM – 10:15 AM  | 7:15 AM              | 1:45 (01:45)         | `breakfast.yml`|
| Lunch     | 1:00 PM – 3:00 PM   | 12:30 PM             | 7:00 (07:00)         | `lunch.yml`    |
| Snacks    | 5:15 PM – 6:45 PM   | 4:45 PM              | 11:15 (11:15)        | `snacks.yml`   |
| Dinner    | 8:00 PM – 10:15 PM  | 7:30 PM              | 14:00 (14:00)        | `dinner.yml`   |

> Most external cron services (including cron-job.org) schedule in **UTC**. Use
> the UTC column, or set the service's timezone to Asia/Kolkata and use the IST
> column.

## Setup

### 1. Create a GitHub Personal Access Token (PAT)

The external service needs a token to trigger workflows via the API.

1. Go to **GitHub → Settings → Developer settings → Personal access tokens →
   Fine-grained tokens → Generate new token**.
2. **Repository access:** Only select repositories → `mess-reminder`.
3. **Permissions:** Repository permissions → **Actions: Read and write**
   (this is what allows dispatching workflows).
4. Set an expiry and generate. **Copy the token** — you can't see it again.

### 2. Make sure the `NTFY_TOPIC` secret exists

The workflows send to `https://ntfy.sh/<NTFY_TOPIC>`. In the repo:
**Settings → Secrets and variables → Actions → New repository secret**,
name `NTFY_TOPIC`, value = your ntfy topic name.

### 3. Create one scheduled job per meal on an external cron service

Using a free service like [cron-job.org](https://cron-job.org) (or EasyCron,
etc.), create **four** cron jobs — one per meal — each configured as an HTTP
request:

- **Method:** `POST`
- **URL:** `https://api.github.com/repos/kpareek4-source/mess-reminder/actions/workflows/<WORKFLOW_FILE>/dispatches`
  (e.g. `.../workflows/breakfast.yml/dispatches`)
- **Headers:**
  - `Accept: application/vnd.github+json`
  - `Authorization: Bearer <YOUR_PAT>`
  - `X-GitHub-Api-Version: 2022-11-28`
  - `Content-Type: application/json`
- **Body:** `{"ref": "main"}`
- **Schedule:** the time from the table above (see UTC note).

Repeat for `lunch.yml`, `snacks.yml`, and `dinner.yml` at their respective times.

A successful dispatch returns HTTP **204 No Content** and a run appears under the
repo's **Actions** tab within seconds.

### Quick test with curl

```bash
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR_PAT>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/kpareek4-source/mess-reminder/actions/workflows/breakfast.yml/dispatches \
  -d '{"ref":"main"}'
```

You can also trigger any workflow manually from the **Actions** tab
(**Run workflow** button), since each one still supports `workflow_dispatch`.
