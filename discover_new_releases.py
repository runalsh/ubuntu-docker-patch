#!/usr/bin/env python3
import os
import re
import sys
import io
import tarfile
import urllib.request

MAJOR_TRACKS = ["22.04", "24.04", "26.04"]
RELEASES_FILE = "releases.txt"
README_FILE = "README.md"

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
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            tf = tarfile.open(fileobj=resp, mode="r|xz")
            for member in tf:
                if member.isfile() and member.name.endswith("usr/lib/os-release"):
                    f = tf.extractfile(member)
                    if f:
                        content = f.read().decode("utf-8")
                        v_id = None
                        v_str = None
                        for line in content.splitlines():
                            if line.startswith("VERSION_ID="):
                                v_id = line.split("=", 1)[1].strip('"\'')
                            elif line.startswith("VERSION="):
                                v_str = line.split("=", 1)[1].strip('"\'')
                        if v_id:
                            return v_id
                        if v_str:
                            m = re.search(r"(\d+\.\d+(?:\.\d+)?)", v_str)
                            if m:
                                return m.group(1)
                    break
    except Exception:
        pass
    return None

def update_readme_table(tag, track):
    if not os.path.exists(README_FILE):
        return
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_row = f"| `{tag}` | `{tag} LTS` | [`runalsh/ubuntu-patch:{tag}`](https://hub.docker.com/r/runalsh/ubuntu-patch/tags) | [`ghcr.io/runalsh/ubuntu-patch:{tag}`](https://github.com/users/runalsh/packages/container/package/ubuntu-patch) |\n"

    # Find where to insert the new row in README.md table
    inserted = False
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Match previous version row in the same track e.g. | `24.04` or | `24.04.4`
        if f"| `{track}" in line and "| [`runalsh/ubuntu-patch" in line and not inserted:
            # Check if next line is not another tag in the same series
            if i + 1 >= len(lines) or not lines[i + 1].startswith(f"| `{track}"):
                new_lines.append(new_row)
                inserted = True

    if inserted:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Updated {README_FILE} table with tag {tag}.")

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

    # Update releases.txt and README.md
    with open(RELEASES_FILE, "a", encoding="utf-8") as f:
        for item in new_discoveries:
            f.write(f"{item['tag']} {item['url']}\n")
            update_readme_table(item['tag'], item['track'])

    print(f"Updated {RELEASES_FILE} and {README_FILE}.")

    # Set GitHub Actions output environment variables
    first_new = new_discoveries[0]
    if "GITHUB_ENV" in os.environ:
        with open(os.environ["GITHUB_ENV"], "a", encoding="utf-8") as f:
            f.write("NEW_RELEASE_FOUND=true\n")
            f.write(f"NEW_TAG={first_new['tag']}\n")
            f.write(f"NEW_URL={first_new['url']}\n")

if __name__ == "__main__":
    main()
