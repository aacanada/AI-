#!/usr/bin/env bash
# Re-transcribe each narration clip with ElevenLabs STT to check for skipped / misread words.
cd "$(dirname "$0")/.."
for f in audio/vo/s*.mp3; do id=$(basename $f .mp3)
  curl -sS https://api.elevenlabs.io/v1/speech-to-text -H "xi-api-key: $ELEVENLABS_API_KEY" -F model_id=scribe_v1 -F language_code=kor -F file=@$f \
   | python3 -c "import sys,json;print(json.load(sys.stdin).get('text',''))" > audio/vo/stt/$id.txt
done
