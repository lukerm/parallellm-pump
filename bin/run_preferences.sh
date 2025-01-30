#!/bin/bash
PROVIDERS="chatgpt claude"
PROVIDERS_VS=$(echo $PROVIDERS | sed -e 's/ /_vs_/g')
mkdir -p data/responses/$PROVIDERS_VS
for i in {0..9}; do
    i_pad=$(printf "%02d" $i)
    prompt_file="data/prompts/prompt$i_pad.txt"
    if [ ! -f $prompt_file ]; then
        echo "Skipping prompt $i_pad"; continue
    fi
    echo "Running prompt $i_pad"
    python -m src.prefer --prompt "`cat $prompt_file`" \
                         --providers $PROVIDERS > data/responses/$PROVIDERS_VS/prompt$i_pad.log 2>&1
done
