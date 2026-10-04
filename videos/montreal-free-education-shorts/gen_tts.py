import json, os, ssl, urllib.request, base64, subprocess
VOICE="9qtE9eIaqHMUAfRp4QTW"
ctx=ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
scenes=json.load(open("scenes.json"))
os.makedirs("assets/voice",exist_ok=True)
out=[]
for i,s in enumerate(scenes):
    body={"text":s["tts"],"model_id":"eleven_multilingual_v2",
          "voice_settings":{"stability":0.5,"similarity_boost":0.8,"style":0.15,"use_speaker_boost":True,"speed":1.12},
          "previous_text": scenes[i-1]["tts"] if i>0 else None,
          "next_text": scenes[i+1]["tts"] if i+1<len(scenes) else None}
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps?output_format=mp3_44100_128",
        data=json.dumps(body).encode(),headers={"xi-api-key":os.environ["ELEVENLABS_API_KEY"],"Content-Type":"application/json"})
    r=json.load(urllib.request.urlopen(req,context=ctx))
    mp3=f"assets/voice/{s['id']}.mp3"
    open(mp3,"wb").write(base64.b64decode(r["audio_base64"]))
    al=r["alignment"]
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",mp3]))
    out.append({"id":s["id"],"path":mp3,"duration":dur,"chars":al["characters"],"starts":al["character_start_times_seconds"],"ends":al["character_end_times_seconds"]})
    print(s["id"],round(dur,2))
json.dump(out,open("voice_alignment.json","w"),ensure_ascii=False)
