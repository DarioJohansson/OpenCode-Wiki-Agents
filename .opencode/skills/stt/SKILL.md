---
name: stt
description: >-
  Use ONLY when the user wants to transcribe an audio file using the internal
  Speech-to-Text service. The user will specify a file path to an audio file.
  This skill handles uploading the file, polling for completion, and returning
  the transcription result. Do NOT use for text-to-speech, voice synthesis,
  or any other audio-related task that is not transcription.
---

# Speech-to-Text (STT) — Internal Service

Transcribes audio files via the internal STT service at `http://stt.internal.shld-systems.com:8000`.

## Usage

Run the CLI script with the path to the audio file:

```powershell
python helper-scripts/stt-transcribe.py <filepath>
```

The script will:
1. Upload the file via `curl.exe` multipart POST to `http://stt.internal.shld-systems.com:8000/convert`
2. Extract the `job_id` from the response
3. Poll `http://stt.internal.shld-systems.com:8000/results/{job_id}` every **1 minute** until complete
4. Save the transcription as a `.txt` file alongside the original audio
5. Print the transcription to stdout

## Status lifecycle

| Status | Meaning |
|--------|---------|
| `pending` | Job is queued, not yet started |
| `running` | Job is actively processing |
| `completed` | Transcription done — result is returned |
| `error` | Job failed — error description is reported |

## Notes

- The file path must point to an existing audio file on this machine
- The script saves output as `<original_filename>.txt` in the same directory
- No external Python packages required — uses only stdlib + `curl.exe`