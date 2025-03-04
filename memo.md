ずんだもんID：3

// (def read_yaml) Read yaml to get all lines
```
- 読み上げテキスト1
- 読み上げテキスト2
```

// Loop each lines
  // (def get_audio_query) get audio query
  curl -s \
      -X POST \
      "127.0.0.1:50021/audio_query?speaker=3" \
      --get --data-urlencode 'text=読み上げテキスト1' \
      > 01_query.json

// (def edit_audio_query) edit audio query json
sed -i -r 's/"speedScale":[0-9.]+/"speedScale":1.5/' *query.json && \
sed -i -r 's/"postPhonemeLength":[0-9.]+/"postPhonemeLength":2.0/' *query.json

// Join all *_query.json into 1 array and save it as 'query.json'

// (def get_audio) get audio
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=3" \
    > audio.wav
