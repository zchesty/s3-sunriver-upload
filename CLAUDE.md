# Claude Agent Instructions

This repository is a Raspberry Pi photo uploader that captures images at dawn/dusk intervals and uploads them to an Amazon S3 bucket. The codebase dates from 2020 and is undergoing a phased revitalization tracked in `REVITALIZATION.md`.

## Working on this project

All planned work is tracked in `REVITALIZATION.md`. Before starting any task:

1. Find the relevant item(s) in the checklist
2. Update the `State` column to `in-progress`
3. Do the work on the `claude/raspi-s3-uploader-review-R1kBl` branch (or a branch per phase)
4. Update the `State` column to `done` when the work is merged

### State values

| Value | Meaning |
|-------|---------|
| `todo` | Not started |
| `in-progress` | Actively being worked |
| `done` | Completed and merged |
| `stalled` | Started but stuck — leave a note in the Notes column |
| `blocked` | Waiting on something external — describe what in the Notes column |
| `wont-fix` | Decided not to address — explain why in the Notes column |

## Project structure

```
pi-pic-script/
  pic-script.py       # main entry point — runs on the Pi
  test2.py            # dev scaffolding (to be deleted, Phase 3.5)
  utils/
    s3_utils.py       # clearBucket() helper — currently unused (Phase 3.4)
    time_utils.py     # getDayLight() — broken return value (Phase 3.2)
datetime_astral_test.py  # standalone astral smoke test (Phase 3.6)
keys.sh                  # SECURITY ISSUE — to be deleted (Phase 1.1)
requirements.txt         # outdated deps, needs full regeneration (Phase 2.4)
REVITALIZATION.md        # phased checklist
```

## Priority order

Work phases in this order — later phases depend on earlier ones being stable:

1. **Phase 1 (Security)** — must be done before anything is deployed
2. **Phase 2 (Runtime)** — Python + library upgrades unblock everything else
3. **Phase 3 (Core logic)** — fix the dangerous bucket-wipe and dead code
4. **Phase 4 (Reliability)** — logging and error handling
5. **Phase 5 (Config)** — extract hardcoded values
6. **Phase 6 (systemd)** — deployment wiring
7. **Phase 7 (Enhancements)** — optional, do last

## Critical context

- **`bucket.objects.all().delete()` runs on every photo upload** (`pic-script.py` ~line 39). The entire S3 bucket is wiped every 30 minutes. Fix: upload to a fixed key (`public/current.jpg`) and overwrite in place — no deletion needed.
- **`keys.sh` contains AWS credential handling that exposes secrets in the process list.** Treat the key pair as compromised and rotate it before any other work.
- **`astral` 1.x → 3.x is a breaking API change.** The `Location` class and `sun()` call signatures changed. Read the astral 3.x docs before touching `time_utils.py` or the main script.
- **`picamera` is deprecated** on Raspberry Pi OS Bookworm and later. Use `picamera2`.

## Running the code

The main script requires Pi hardware (camera module) and valid AWS credentials. For development and testing without hardware:

- Comment out the `PiCamera` block (as done in `test2.py`) to test S3 logic
- Use `datetime_astral_test.py` to validate sun-timing logic without S3 or camera
- Set `AWS_PROFILE` or populate `~/.aws/credentials` before running any S3 code
