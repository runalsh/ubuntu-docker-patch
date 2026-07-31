#!/bin/bash
set -euo pipefail

IMAGE_NAME="runalsh/ubuntu-docker-patch"
RELEASES_FILE="releases.txt"

if [ ! -f "$RELEASES_FILE" ]; then
    echo "Error: $RELEASES_FILE not found!"
    exit 1
fi

echo "Starting process for image repository: ${IMAGE_NAME}"

while read -r tag url || [ -n "$tag" ]; do
    # Skip empty lines or comments
    [[ -z "$tag" || "$tag" =~ ^# ]] && continue

    echo "=========================================="
    echo "Processing tag: ${tag}"
    echo "URL: ${url}"
    echo "=========================================="

    TAR_FILE="temp_rootfs_${tag}.tar.xz"

    echo "1. Downloading rootfs..."
    curl -fSL -o "${TAR_FILE}" "${url}"

    FULL_IMAGE_TAG="${IMAGE_NAME}:${tag}"

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

    if [ "${PUSH_TO_DOCKERHUB:-false}" = "true" ]; then
        echo "4. Pushing image to Docker Hub..."
        docker push "${FULL_IMAGE_TAG}"
    else
        echo "4. Skipping Docker Hub push (PUSH_TO_DOCKERHUB is not set to 'true')."
    fi

    echo "5. Cleaning up local tarball..."
    rm -f "${TAR_FILE}"

    echo "Successfully completed processing for tag ${tag}!"
    echo
done < "$RELEASES_FILE"

echo "All images processed successfully!"
