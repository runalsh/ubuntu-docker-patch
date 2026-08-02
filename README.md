# Ubuntu Docker Patch Images

Automated build of Docker images for exact Ubuntu point releases (**22.04.0** .. **22.04.5**, **24.04.0** .. **24.04.4**, **26.04.0**).

---

## ❓ Problem Statement

The official Docker Hub registry (`library/ubuntu`) publishes **only major tags** (e.g., `ubuntu:22.04`, `ubuntu:24.04`, `ubuntu:26.04`, `jammy`, `noble`, `resilient`).

Official tags like `ubuntu:22.04.1`, `ubuntu:22.04.5`, or `ubuntu:24.04.2` **do not exist**, as maintainers continuously update major tags with the latest packages.

### Key Issues:
1. **Testing on specific distribution patch versions**: Impossibility of running tests or simulating environments locked to a specific point release (e.g., `22.04.1` or `24.04.2`).
2. **Build Reproducibility**: The base `ubuntu:22.04` image changes over time as packages are updated, which can mask or alter software behavior.
3. **Security Audits & Forensics**: Difficulty in reproducing system environments as they existed at a specific point release date.

---

## 🚀 Solution

This repository addresses the problem by:
- Using official root filesystem archives (**rootfs tar.xz**) directly from Canonical (`cloud-images.ubuntu.com`).
- Building and validating clean Docker images for each exact Ubuntu LTS point release.
- Automatically validating `/etc/os-release` against the expected version tag before publishing.
- Generating SPDX SBOM files and scanning for vulnerabilities using **Trivy** without blocking the pipeline.
- Automatically publishing ready-to-use Docker images to **Docker Hub** (`runalsh/ubuntu-patch`) and **GitHub Container Registry** (`ghcr.io/runalsh/ubuntu-patch`).

---

## 📦 Available Images and Registries

### Ubuntu 22.04 LTS (Jammy Jellyfish)

| Tag | OS Version | Docker Hub Image Link | GHCR Package Link |
|---|---|---|---|
| `22.04` | `Latest 22.04 LTS` | [`runalsh/ubuntu-patch:22.04`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.0` | `22.04.0 LTS` | [`runalsh/ubuntu-patch:22.04.0`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.0`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.1` | `22.04.1 LTS` | [`runalsh/ubuntu-patch:22.04.1`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.1`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.2` | `22.04.2 LTS` | [`runalsh/ubuntu-patch:22.04.2`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.2`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.3` | `22.04.3 LTS` | [`runalsh/ubuntu-patch:22.04.3`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.3`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.4` | `22.04.4 LTS` | [`runalsh/ubuntu-patch:22.04.4`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.4`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `22.04.5` | `22.04.5 LTS` | [`runalsh/ubuntu-patch:22.04.5`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:22.04.5`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |

### Ubuntu 24.04 LTS (Noble Numbat)

| Tag | OS Version | Docker Hub Image Link | GHCR Package Link |
|---|---|---|---|
| `24.04` | `Latest 24.04 LTS` | [`runalsh/ubuntu-patch:24.04`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `24.04.0` | `24.04.0 LTS` | [`runalsh/ubuntu-patch:24.04.0`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04.0`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `24.04.1` | `24.04.1 LTS` | [`runalsh/ubuntu-patch:24.04.1`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04.1`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `24.04.2` | `24.04.2 LTS` | [`runalsh/ubuntu-patch:24.04.2`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04.2`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `24.04.3` | `24.04.3 LTS` | [`runalsh/ubuntu-patch:24.04.3`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04.3`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `24.04.4` | `24.04.4 LTS` | [`runalsh/ubuntu-patch:24.04.4`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:24.04.4`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |

### Ubuntu 26.04 LTS (Resilient Reptile)

| Tag | OS Version | Docker Hub Image Link | GHCR Package Link |
|---|---|---|---|
| `26.04` | `Latest 26.04 LTS` | [`runalsh/ubuntu-patch:26.04`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:26.04`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |
| `26.04.0` | `26.04.0 LTS` | [`runalsh/ubuntu-patch:26.04.0`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:26.04.0`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |

---

## 🛠 Quick Start

### Docker Hub

```bash
docker run --rm -it runalsh/ubuntu-patch:22.04.0 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-patch:22.04.5 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-patch:24.04.0 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-patch:26.04.0 cat /etc/os-release
```

### GitHub Container Registry (GHCR)

```bash
docker run --rm -it ghcr.io/runalsh/ubuntu-patch:22.04.0 cat /etc/os-release
docker run --rm -it ghcr.io/runalsh/ubuntu-patch:22.04.5 cat /etc/os-release
docker run --rm -it ghcr.io/runalsh/ubuntu-patch:24.04.0 cat /etc/os-release
docker run --rm -it ghcr.io/runalsh/ubuntu-patch:26.04.0 cat /etc/os-release
```

### Local Build

The `releases.txt` file contains a list of tags and direct download URLs for rootfs archives.

To import all versions locally:

```bash
chmod +x build.sh
TEST_VERSION=true PUSH_TO_DOCKERHUB=false PUSH_TO_GHCR=false ./build.sh
```

---

## 🔧 Environment Variables

The `build.sh` script supports the following configuration environment variables:

| Variable | Default | Description |
|---|---|---|
| `TEST_VERSION` | `true` | When set to `true`, verifies container functionality and validates `/etc/os-release` after import. |
| `PUSH_TO_DOCKERHUB` | `false` | When set to `true`, automatically pushes built images to Docker Hub (`runalsh/ubuntu-patch:<tag>`). |
| `PUSH_TO_GHCR` | `false` | When set to `true`, automatically pushes built images to GitHub Packages / GHCR (`ghcr.io/runalsh/ubuntu-patch:<tag>`). |
| `CLEANUP_DOCKER_IMAGES` | `false` | When set to `true`, deletes local Docker images (`docker rmi`) after build and push to conserve disk space. |
| `SKIP_EXISTS_CHECK` | `false` | When set to `false`, checks if the image tag already exists and skips download/build if present. Set to `true` to force building all tags regardless of remote registry status. |
| `ENABLE_TRIVY_SCAN` | `false` | When set to `true` (or when `trivy` binary is present), generates SPDX SBOM reports (`trivy-reports/sbom-<tag>.json`) and logs vulnerabilities to stdout without failing the build pipeline (`--exit-code 0`). |

---

## 🛡 Security & Trivy Scanning

During build execution, images are scanned using [Trivy](https://github.com/aquasecurity/trivy):
- **SBOM Generation**: Exported in SPDX-JSON format (`trivy-reports/sbom-<tag>.json`) and saved to GitHub Actions Job Artifacts (`ubuntu-sbom-reports`).
- **Vulnerability Logging**: Vulnerabilities (UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL) are logged to build stdout. Scans execute with `--exit-code 0`, ensuring pipeline continuity regardless of identified CVEs.

---

## ⚙️ Repository Structure

```text
.
├── .github/workflows/
│   ├── build-and-push.yml        # Automated CI pipeline for building, testing, scanning, and pushing to Docker Hub & GHCR
│   └── auto-discover-ubuntu.yml  # Weekly cron workflow for discovering new Ubuntu point releases and opening PRs
├── build.sh                       # Script for automatic import, Trivy scanning, and version verification
├── discover_new_releases.py       # Python scanner for checking Canonical for new point releases
├── releases.txt                   # Registry of URLs with rootfs versions
└── README.md                      # Project documentation
```

---

## 🔐 GitHub Actions Secrets

The CI workflow requires the following secrets in GitHub Secrets:
- `DOCKERHUB_USERNAME`: Your Docker Hub username (`runalsh`)
- `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token
- `${{ secrets.GITHUB_TOKEN }}`: Automatically provided by GitHub for GHCR publishing
