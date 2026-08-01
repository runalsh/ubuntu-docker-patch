# Ubuntu Docker Patch Images

Automated build of Docker images for exact Ubuntu point releases (**22.04** .. **22.04.5**, **24.04** .. **24.04.4**, **26.04**).

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
- Automatically publishing ready-to-use Docker images to Docker Hub: **`runalsh/ubuntu-patch`**.

---

## 📦 Available Images and Tags

### Ubuntu 22.04 LTS (Jammy Jellyfish)

| Tag | Version in `/etc/os-release` | Canonical Base Release |
|---|---|---|
| `runalsh/ubuntu-patch:22.04` | `22.04 LTS` | `release-20220420` |
| `runalsh/ubuntu-patch:22.04.1` | `22.04.1 LTS` | `release-20220810` |
| `runalsh/ubuntu-patch:22.04.2` | `22.04.2 LTS` | `release-20230302` |
| `runalsh/ubuntu-patch:22.04.3` | `22.04.3 LTS` | `release-20230814` |
| `runalsh/ubuntu-patch:22.04.4` | `22.04.4 LTS` | `release-20240223` |
| `runalsh/ubuntu-patch:22.04.5` | `22.04.5 LTS` | `release-20240912` |

### Ubuntu 24.04 LTS (Noble Numbat)

| Tag | Version in `/etc/os-release` | Canonical Base Release |
|---|---|---|
| `runalsh/ubuntu-patch:24.04` | `24.04 LTS` | `release-20240423` |
| `runalsh/ubuntu-patch:24.04.1` | `24.04.1 LTS` | `release-20240911` |
| `runalsh/ubuntu-patch:24.04.2` | `24.04.2 LTS` | `release-20250221` |
| `runalsh/ubuntu-patch:24.04.3` | `24.04.3 LTS` | `release-20250805` |
| `runalsh/ubuntu-patch:24.04.4` | `24.04.4 LTS` | `release-20260225` |

### Ubuntu 26.04 LTS (Resilient Reptile)

| Tag | Version in `/etc/os-release` | Canonical Base Release |
|---|---|---|
| `runalsh/ubuntu-patch:26.04` | `26.04 LTS` | `release-20260421` |

---

## 🛠 Quick Start

### Using pre-built images from Docker Hub

```bash
docker run --rm -it runalsh/ubuntu-patch:22.04.1 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-patch:24.04.2 cat /etc/os-release
docker run --rm -it runalsh/ubuntu-patch:26.04 cat /etc/os-release
```

### Local Build

The `releases.txt` file contains a list of tags and direct download URLs for rootfs archives.

To import all versions locally:

```bash
chmod +x build.sh
TEST_VERSION=true PUSH_TO_DOCKERHUB=false ./build.sh
```

---

## 🔧 Environment Variables

The `build.sh` script supports the following configuration environment variables:

| Variable | Default | Description |
|---|---|---|
| `TEST_VERSION` | `true` | When set to `true`, verifies container functionality and validates `/etc/os-release` after import. |
| `PUSH_TO_DOCKERHUB` | `false` | When set to `true`, automatically pushes built images to Docker Hub (`runalsh/ubuntu-patch:<tag>`). |
| `CLEANUP_DOCKER_IMAGES` | `false` | When set to `true`, deletes the local Docker image (`docker rmi`) after build and push to conserve disk space. |
| `SKIP_EXISTS_CHECK` | `false` | When set to `false`, checks if the image tag already exists on Docker Hub and skips download/build if present. Set to `true` to force building all tags regardless of Docker Hub status. |

---

## ⚙️ Repository Structure

```text
.
├── .github/workflows/
│   └── build-and-push.yml  # Automated CI pipeline for building, testing, and pushing to Docker Hub
├── build.sh                 # Script for automatic import and version verification
├── releases.txt             # Registry of URLs with rootfs versions
└── README.md                # Project documentation
```

---

## 🔐 GitHub Actions Secrets

The CI workflow requires the following secrets in GitHub Secrets:
- `DOCKERHUB_USERNAME`: Your Docker Hub username (`runalsh`)
- `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token
