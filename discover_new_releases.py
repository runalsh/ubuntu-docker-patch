#!/usr/bin/env python3
import os
import re
import sys
import io
import tarfile
import urllib.request

MAJOR_TRACKS = ["22.04", "24.04", "26.04"]
RELEASES_FILE = "releases.txt"

def load_existing_releases(releases_path):
    existing = set()
    if not os.path.exists(releases_path):
        return existing
    with open(releases_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split()
                if parts:
                    existing.add(parts[0])
    return existing

def inspect_os_release(tar_url):
    req = urllib.request.Request(tar_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        tf = tarfile.open(fileobj=resp, mode="r|xz")
        for member in tf:
            # Check for regular os-release file (usr/lib/os-release or etc/os-release)
            if (member.name.endswith("usr/lib/os-release") or member.name.endswith("etc/os-release")) and member.isfile():
                f = tf.extractfile(member)
                if f:
                    content = f.read().decode("utf-8")
                    for line in content.splitlines():
                        if line.startswith("VERSION="):
                            v_str = line.split("=", 1)[1].strip('"\'')
                            m = re.search(r"(\d+\.\d+(?:\.\d+)?)", v_str)
                            if m:
                                return m.group(1)
                    for line in content.splitlines():
                        if line.startswith("VERSION_ID="):
                            return line.split("=", 1)[1].strip('"\'')
                break
    return None

def main():
    existing_tags = load_existing_releases(RELEASES_FILE)
    print(f"Loaded existing tags from {RELEASES_FILE}: {sorted(list(existing_tags))}")

    new_discoveries = []

    for track in MAJOR_TRACKS:
        print(f"\nScanning Canonical release track {track}...")
        url = f"https://cloud-images.ubuntu.com/releases/{track}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            html = urllib.request.urlopen(req).read().decode("utf-8")
            folders = sorted(list(set(re.findall(r"release-\d{8}", html))))
        except Exception as e:
            print(f"Failed to fetch directory listing for {track}: {e}")
            continue

        print(f"Found {len(folders)} dated release folders for {track}.")

        for folder in reversed(folders):
            tar_url = f"https://cloud-images.ubuntu.com/releases/{track}/{folder}/ubuntu-{track}-server-cloudimg-amd64-root.tar.xz"
            try:
                print(f"Checking {folder}...")
                tag = inspect_os_release(tar_url)
                if not tag:
                    continue

                if tag in existing_tags:
                    print(f"Tag {tag} already present in releases.txt. Track {track} up to date!")
                    break

                print(f"✨ NEW RELEASE DISCOVERED! Tag: {tag} -> {tar_url}")
                new_discoveries.append({
                    "tag": tag,
                    "url": tar_url,
                    "track": track,
                    "folder": folder
                })
                existing_tags.add(tag)
            except Exception as e:
                print(f"Error checking {tar_url}: {e}")

    if not new_discoveries:
        print("\nNo new Ubuntu point releases found. Everything up to date!")
        if "GITHUB_ENV" in os.environ:
            with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
                f.write("NEW_RELEASE_FOUND=false\n")
        return

    print(f"\nDiscovered {len(new_discoveries)} new release(s):")
    for item in new_discoveries:
        print(f" - {item['tag']}: {item['url']}")

    # Update releases.txt
    with open(RELEASES_FILE, "a", encoding="utf-8") as f:
        for item in new_discoveries:
            f.write(f"{item['tag']} {item['url']}\n")
    print(f"Updated {RELEASES_FILE}.")

    # Set GitHub Actions output environment variables
    first_new = new_discoveries[0]
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
            f.write("NEW_RELEASE_FOUND=true\n")
            f.write(f"NEW_TAG={first_new['tag']}\n")
            f.write(f"NEW_URL={first_new['url']}\n")

if __name__ == "__main__":
    main()
