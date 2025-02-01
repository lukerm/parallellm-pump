#!/bin/bash
#  Copyright (C) 2025 lukerm of www.zl-labs.tech
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

PROVIDERS="chatgpt claude"
PROVIDERS_VS=$(echo $PROVIDERS | sed -e 's/ /_vs_/g')
mkdir -p data/responses/$PROVIDERS_VS
for i in {0..9}; do
    i_pad=$(printf "%02d" $i)
    prompt_file="data/prompts/prompt$i_pad.txt"
    if [ ! -f $prompt_file ]; then
        echo "Skipping prompt $i_pad"; continue
    fi
    echo "Pumping prompt $i_pad"
    python -m src.prefer --prompt "`cat $prompt_file`" \
                         --providers $PROVIDERS > data/responses/$PROVIDERS_VS/prompt$i_pad.log 2>&1
done
