# Revitalization Checklist

Tracks all identified issues and improvements for the `s3-sunriver-upload` Raspberry Pi photo uploader.

**State values:** `todo` · `in-progress` · `done` · `stalled` · `blocked` · `wont-fix`

---

## Phase 1 — Security & Credentials

| # | Task | State | Notes |
|---|------|-------|-------|
| 1.1 | Remove `keys.sh` from repo and git history | `done` | Credentials were passed as CLI args, visible in process list and bash history |
| 1.2 | Rotate the AWS credentials that were committed | `todo` | Treat as compromised; generate new key pair in IAM |
| 1.3 | Switch to `~/.aws/credentials` file or IAM role auth | `todo` | Never pass secrets as arguments or env vars set in scripts |
| 1.4 | Scope IAM policy to minimum required permissions | `todo` | Only `s3:PutObject` + `s3:DeleteObject` on `sunriver-display-s3-prod/public/*` |

---

## Phase 2 — Modernize the Runtime

| # | Task | State | Notes |
|---|------|-------|-------|
| 2.1 | Upgrade to Python 3.11 or 3.12 | `todo` | Currently pinned to Python 3.5.3 (EOL Oct 2020) |
| 2.2 | Migrate from `astral` 1.x to 3.x | `todo` | Breaking API change — location and sun() interfaces changed significantly |
| 2.3 | Replace `picamera` with `picamera2` | `in-progress` | `picamera` is deprecated on modern Pi OS (Bookworm+) |
| 2.4 | Regenerate `requirements.txt` with current pinned versions | `todo` | boto3, botocore, pytz, python-dateutil all need updates |
| 2.5 | Add `pyvenv.cfg` to `.gitignore` | `done` | Virtual environment config should not be in source control |

---

## Phase 3 — Fix Core Logic

| # | Task | State | Notes |
|---|------|-------|-------|
| 3.1 | Replace bucket-wipe-on-upload with fixed key overwrite | `done` | `bucket.objects.all().delete()` on every photo is destructive; upload to `public/current.jpg` instead |
| 3.2 | Fix `time_utils.getDayLight()` return value | `in-progress` | Function returns the location object instead of the sun timing dict — broken/dead code |
| 3.3 | Wire `time_utils` into main script or delete it | `todo` | Currently unused; duplicated inline in `pic-script.py` |
| 3.4 | Delete `s3_utils.py` or use it | `todo` | `clearBucket()` was extracted but never imported; orphaned dead code |
| 3.5 | Delete `test2.py` and `test.txt` | `done` | Leftover development scaffolding committed to repo |
| 3.6 | Remove or fix `datetime_astral_test.py` | `todo` | Decide if this becomes a proper test or gets deleted |

---

## Phase 4 — Reliability & Observability

| # | Task | State | Notes |
|---|------|-------|-------|
| 4.1 | Replace `print()` with `logging` module | `todo` | Logs go nowhere once terminal is closed; use rotating file handler at `/var/log/sunriver-upload.log` |
| 4.2 | Add try/except around camera capture with retry | `todo` | Camera failures silently crash the script |
| 4.3 | Add try/except around S3 upload with exponential backoff | `todo` | Network dropouts and S3 throttling cause silent crashes; 3 retries recommended |
| 4.4 | Add SIGTERM / SIGINT signal handling for graceful shutdown | `todo` | Mid-upload interruption can leave bucket in partial state |
| 4.5 | Add error handling around astral dawn/dusk calculation | `todo` | `astral` can throw on edge-case dates/coordinates |

---

## Phase 5 — Configurability

| # | Task | State | Notes |
|---|------|-------|-------|
| 5.1 | Extract all hardcoded values to a config file | `todo` | Bucket name, prefix, lat/lon, timezone, resolution, interval, filename template are all buried in script body |
| 5.2 | Choose config mechanism (`.env`, `config.ini`, or `config.py`) | `todo` | `.env` + `python-dotenv` is common; `configparser` + `.ini` is zero-dependency |
| 5.3 | Add `.env.example` or `config.example.ini` to repo | `todo` | Document required config keys so setup is self-explanatory |

---

## Phase 6 — Run as a systemd Service

| # | Task | State | Notes |
|---|------|-------|-------|
| 6.1 | Write `sunriver-upload.service` systemd unit file | `todo` | Enables start-on-boot and automatic restart on crash |
| 6.2 | Set `Restart=on-failure` with a restart delay | `todo` | Prevents rapid crash loops |
| 6.3 | Write installation / deployment instructions in README | `todo` | Document `systemctl enable`, credential setup, and config steps |

---

## Phase 7 — Optional Enhancements

| # | Task | State | Notes |
|---|------|-------|-------|
| 7.1 | Add photo archive alongside current.jpg | `todo` | Upload to `archive/YYYY/MM/DD/HH-MM.jpg` in addition to overwriting `current.jpg`; enables time-lapse later |
| 7.2 | Upload a heartbeat/health file to S3 each cycle | `todo` | Allows external uptime monitoring without SSH access to the Pi |
| 7.3 | Improve image quality settings for picamera2 | `todo` | HDR, white balance, and exposure controls available in picamera2 |
| 7.4 | Add GitHub Actions CI (lint + test) | `todo` | `ruff` for linting, `pytest` for unit tests, run on push to catch regressions before deploy |
| 7.5 | Write unit tests for time/sun logic | `todo` | `time_utils` logic is testable without hardware; mock astral calls |
