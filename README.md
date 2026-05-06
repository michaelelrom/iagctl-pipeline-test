# iagctl-pipeline-test

A GitHub Actions pipeline that automatically imports IAG5 services into [Itential Automation Gateway](https://itential.com) via `iagctl db import` whenever the script or decorator changes.

## How it works

```
Push change to import.yaml or scripts/**
        │
        ▼
GitHub Actions (self-hosted runner on your Mac)
        │
        ├── iagctl db import --check   (validate)
        ├── iagctl db import --force   (import into IAG5)
        └── iagctl run pipeline-test-script  (smoke test)
        │
        ▼
Service appears in Gateway Manager
```

## Repo structure

```
.github/workflows/
  iagctl-import.yml                 ← pipeline definition
import.yaml                         ← service + decorator definition
scripts/
  pipeline-test.py                  ← IAG5 Python service
```

## Prerequisites

- IAG5 (gateway5) running locally via `itential-dev-stack`
- `iagctl` installed on your Mac at `/usr/local/bin/iagctl`
- A GitHub Actions self-hosted runner registered on this repo

## One-time setup

### 1. Get an iagctl API key

Login and capture the API key in one step:

```bash
iagctl login admin --raw 2>/dev/null | grep -i "api-key\|apiKey\|key" | awk '{print $NF}'
```

Or login interactively and copy the key manually:

```bash
iagctl login admin --raw
```

Enter your password when prompted. The output will contain your API key — copy the value and store it as the `IAG5_API_KEY` secret.

> **Note:** The API key does not expire. It is only invalidated if you run `iagctl login admin --change-password`. If you rotate your password, regenerate the key and update the secret.

### 2. Register a self-hosted runner

Go to **Settings → Actions → Runners → New self-hosted runner** in this repo and follow the macOS instructions. The runner must be running on the same machine as your `itential-dev-stack` so it can reach `gateway5` on `localhost:50051`.

### 3. Add GitHub secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|---|---|
| `IAG5_SERVER` | `localhost:50051` |
| `IAG5_API_KEY` | API key from step 1 |
| `IAG5_CA_CERT` | Contents of `volumes/gateway5/certificates/gw-manager.pem` |

## Testing

### Option A — trigger manually (no code change needed)

Go to **Actions → iagctl-import → Run workflow** in the GitHub UI.

### Option B — push a change

Edit either the script or the decorator and push to `main`:

```bash
# edit the service script
vi scripts/pipeline-test.py

git add import.yaml scripts/
git commit -m "chore: trigger pipeline test"
git push origin main
```

The pipeline triggers automatically on any change to `import.yaml` or `scripts/`.

### Verify in Gateway Manager

After the pipeline succeeds, open **Gateway Manager** in your Itential Platform and look for:

- **Repository:** `iagctl-pipeline-test`
- **Service:** `pipeline-test-script`
- **Decorator:** `pipeline-test-decorator`

Run the service from the UI and pass `message` and `target` as inputs.

## Modifying the service

| What to change | File |
|---|---|
| Script logic | `scripts/pipeline-test.py` |
| Input variables / schema | `decorators` section of `import.yaml` |
| Service metadata (name, tags) | `services` section of `import.yaml` |
| Pipeline triggers / steps | `.github/workflows/iagctl-import.yml` |
