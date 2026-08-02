#!/bin/bash
set -euo pipefail

IMAGE_NAME="runalsh/ubuntu-patch"
RELEASES_FILE="releases.txt"

if [ ! -f "$RELEASES_FILE" ]; then
    echo "Error: $RELEASES_FILE not found!"
    exit 1
fi

mkdir -p trivy-reports

echo "Starting process for image repository: ${IMAGE_NAME}"

while read -r tag url || [ -n "$tag" ]; do
    # Skip empty lines or comments
    [[ -z "$tag" || "$tag" =~ ^# ]] && continue

    echo "=========================================="
    echo "Processing tag: ${tag}"
    echo "URL: ${url}"
    echo "=========================================="

    FULL_IMAGE_TAG="${IMAGE_NAME}:${tag}"
    GHCR_IMAGE_NAME="ghcr.io/$(echo "${IMAGE_NAME}" | tr '[:upper:]' '[:lower:]')"
    FULL_GHCR_TAG="${GHCR_IMAGE_NAME}:${tag}"

    NEEDS_DOCKERHUB_PUSH=false
    NEEDS_GHCR_PUSH=false

    if [ "${SKIP_EXISTS_CHECK:-false}" = "true" ]; then
        echo "SKIP_EXISTS_CHECK is true. Forcing build and push for ${tag}..."
        [ "${PUSH_TO_DOCKERHUB:-false}" = "true" ] && NEEDS_DOCKERHUB_PUSH=true
        [ "${PUSH_TO_GHCR:-false}" = "true" ] && NEEDS_GHCR_PUSH=true
    else
        if [ "${PUSH_TO_DOCKERHUB:-false}" = "true" ]; then
            if ! docker manifest inspect "${FULL_IMAGE_TAG}" &>/dev/null && ! curl -sfSL "https://hub.docker.com/v2/repositories/${IMAGE_NAME}/tags/${tag}/" &>/dev/null; then
                echo "Tag ${FULL_IMAGE_TAG} missing on Docker Hub."
                NEEDS_DOCKERHUB_PUSH=true
            fi
        fi

        if [ "${PUSH_TO_GHCR:-false}" = "true" ]; then
            if ! docker manifest inspect "${FULL_GHCR_TAG}" &>/dev/null; then
                echo "Tag ${FULL_GHCR_TAG} missing on GHCR."
                NEEDS_GHCR_PUSH=true
            fi
        fi

        if [ "${NEEDS_DOCKERHUB_PUSH}" = "false" ] && [ "${NEEDS_GHCR_PUSH}" = "false" ]; then
            if [ "${PUSH_TO_DOCKERHUB:-false}" = "true" ] || [ "${PUSH_TO_GHCR:-false}" = "true" ]; then
                echo "Tag ${tag} already exists on all enabled remote registries. Skipping download and build!"
                echo
                continue
            fi
        fi
    fi

    TAR_FILE="temp_rootfs_${tag}.tar.xz"

    echo "1. Downloading rootfs..."
    curl -fSL -o "${TAR_FILE}" "${url}"

    echo "2. Importing rootfs into Docker as ${FULL_IMAGE_TAG}..."
    docker import "${TAR_FILE}" "${FULL_IMAGE_TAG}"

    if [ "${TEST_VERSION:-true}" = "true" ]; then
        echo "3. Verifying container functionality and /etc/os-release version..."
        OS_RELEASE=$(docker run --rm "${FULL_IMAGE_TAG}" cat /etc/os-release)
        echo "$OS_RELEASE"

        # Normalize tag if ending in .0 (e.g. 22.04.0 -> 22.04)
        EXPECTED_VER="${tag%.0}"

        if echo "$OS_RELEASE" | grep -q "${EXPECTED_VER}"; then
            echo "SUCCESS: Version match found for ${EXPECTED_VER} in /etc/os-release!"
        else
            echo "ERROR: Version mismatch! Expected ${EXPECTED_VER} in /etc/os-release"
            exit 1
        fi
    else
        echo "3. Skipping version verification (TEST_VERSION is false)."
    fi

    if command -v trivy &>/dev/null || [ "${ENABLE_TRIVY_SCAN:-false}" = "true" ]; then
        echo "4. Generating SBOM and scanning vulnerabilities with Trivy..."
        trivy image --format spdx-json --output "trivy-reports/sbom-${tag}.json" "${FULL_IMAGE_TAG}" 2>/dev/null || true
        echo "--- Trivy Vulnerability Report for ${FULL_IMAGE_TAG} ---"
        trivy image --exit-code 0 --severity UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL "${FULL_IMAGE_TAG}" || true
        echo "--------------------------------------------------------"
    fi

    if [ "${NEEDS_DOCKERHUB_PUSH}" = "true" ] || [ "${PUSH_TO_DOCKERHUB:-false}" = "true" ]; then
        echo "5. Pushing image to Docker Hub (${FULL_IMAGE_TAG})..."
        docker push "${FULL_IMAGE_TAG}" || true
    else
        echo "5. Skipping Docker Hub push."
    fi

    if [ "${NEEDS_GHCR_PUSH}" = "true" ] || [ "${PUSH_TO_GHCR:-false}" = "true" ]; then
        echo "6. Pushing image to GitHub Packages / GHCR (${FULL_GHCR_TAG})..."
        docker tag "${FULL_IMAGE_TAG}" "${FULL_GHCR_TAG}"
        docker push "${FULL_GHCR_TAG}" || true
        if [ "${CLEANUP_DOCKER_IMAGES:-false}" = "true" ]; then
            docker rmi -f "${FULL_GHCR_TAG}" 2>/dev/null || true
        fi
    else
        echo "6. Skipping GHCR push."
    fi

    echo "7. Cleaning up local tarball..."
    rm -f "${TAR_FILE}"

    if [ "${CLEANUP_DOCKER_IMAGES:-false}" = "true" ]; then
        echo "Removing local Docker image ${FULL_IMAGE_TAG} to save disk space..."
        docker rmi -f "${FULL_IMAGE_TAG}" 2>/dev/null || true
    fi

    echo "Successfully completed processing for tag ${tag}!"
    echo
done < "$RELEASES_FILE"

echo "All images processed successfully!"
