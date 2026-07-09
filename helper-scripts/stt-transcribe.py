import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error

BASE_URL = "http://stt.internal.shld-systems.com:8000"


def submit_audio(filepath: str) -> str:
    result = subprocess.run(
        ["curl.exe", "-s", "-X", "POST", f"{BASE_URL}/convert", "-F", f"file=@{filepath}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Upload failed (exit {result.returncode}): {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Unexpected response: {result.stdout}", file=sys.stderr)
        sys.exit(1)

    if "job_id" not in data:
        print(f"Unexpected response: {data}", file=sys.stderr)
        sys.exit(1)

    return data["job_id"]


def poll_job(job_id: str) -> dict:
    url = f"{BASE_URL}/results/{job_id}"
    while True:
        try:
            with urllib.request.urlopen(url) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.URLError as e:
            print(f"Poll error: {e}", file=sys.stderr)
            time.sleep(60)
            continue

        status = data.get("status")
        if status == "completed":
            return data
        if status == "error":
            print(f"Job failed: {data.get('error', 'unknown error')}", file=sys.stderr)
            sys.exit(1)
        if status in ("pending", "running"):
            print(f"  Status: {status} — waiting 60s...")
            time.sleep(60)
            continue

        print(f"Unknown status: {data}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio via internal STT service")
    parser.add_argument("filepath", help="Path to audio file")
    args = parser.parse_args()

    filepath = os.path.abspath(args.filepath)
    if not os.path.isfile(filepath):
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    print(f"Submitting {filepath}...")
    job_id = submit_audio(filepath)
    print(f"Job ID: {job_id}")

    print("Waiting 1 minute before first poll...")
    result = poll_job(job_id)

    segments = result.get("result", {}).get("segments")
    if isinstance(segments, list) and segments:
        if isinstance(segments[0], dict):
            text = "\n".join(s.get("text", "") for s in segments if "text" in s)
        else:
            text = "\n".join(str(s) for s in segments)
    elif isinstance(segments, dict):
        text = segments.get("text", json.dumps(segments, ensure_ascii=False))
    else:
        text = str(segments) if segments else ""

    out_dir = os.path.dirname(filepath)
    base = os.path.splitext(os.path.basename(filepath))[0]
    out_path = os.path.join(out_dir, f"{base}.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"\nTranscription saved to {out_path}")
    print(f"Transcript:\n{text}")


if __name__ == "__main__":
    main()
