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

## Workflow

### 1. Submit the audio file

```powershell
curl -X POST "http://stt.internal.shld-systems.com:8000/convert" -F "file=@<filepath>"
```

Replace `<filepath>` with the absolute path to the audio file provided by the user.

**Response (success):**
```json
{"job_id":"<id string>"}
```

Extract the `job_id` from the response.

### 2. Poll for results

Poll `http://stt.internal.shld-systems.com:8000/results/{job_id}` periodically until the job completes.

```powershell
curl -X GET "http://stt.internal.shld-systems.com:8000/results/{job_id}"
```

**Possible status responses:**

| Status | Meaning | Response |
|--------|---------|----------|
| `pending` | Job is queued, not yet started | `{"status":"pending","job_id":"<id>"}` |
| `running` | Job is actively processing | `{"status":"running","job_id":"<id>"}` |
| `completed` | Transcription done | `{"status":"completed","job_id":"<id>","result":"<transcription>"}` |
| `error` | Job failed | `{"status":"error","job_id":"<id>","error":"<error description>"}` |

### Polling strategy

- Wait **1 minute** between polls
- Stop polling when status is `completed` or `error`
- Return the transcription result to the user

## Notes

- Use `Invoke-RestMethod` in PowerShell or `curl` for the HTTP calls
- The file path must point to an existing audio file on this machine
- The service returns `job_id` on successful upload — do not proceed to polling without it
