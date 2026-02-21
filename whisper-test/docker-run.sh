#!/usr/bin/env sh

docker run --rm -it \
  --device /dev/snd \
  whisper-listener