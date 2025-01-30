import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Dict

import pandas as pd


PROVIDERS = ["chatgpt", "claude"]  # Must be in correct order (as originally supplied to pump/prefer.py)


def format_output(counters: Dict, rmap: Dict[int, str]) -> str:
    jdump = json.dumps(counters, indent=4)
    for k, v in rmap.items():
        jdump = jdump.replace(f'"{k}"', f'"{v}"')

    return jdump


if __name__ == "__main__":

    response_path = Path(__file__).resolve().parents[1] / "data" / "responses" / "chatgpt_vs_claude"
    response_files = os.listdir(response_path)

    providers = PROVIDERS
    rmap = {str(i + 1): provider for i, provider in enumerate(providers)}
    counters = {provider: Counter() for provider in providers}

    rows = []
    for response_file in sorted(response_files):

        prompt_no = response_file.split(".")[0].replace("prompt", "")
        row = {'prompt_no': prompt_no}

        with open(Path(response_path) / response_file, 'r') as f:
            log = f.read()

        # Search for patterns of the form:
        # chatgpt
        # _______
        #
        # 1. Response 1
        for provider in providers:
            search_pattern = f"{provider}\n{'_'*len(provider)}\n\n"
            search_pattern += "1. Response ([0-9])"
            grep = re.search(search_pattern, log)
            counters[provider].update([grep.group(1)])
            row[provider] = rmap[grep.group(1)]

        row['disagree'] = '*' if row[providers[0]] != row[providers[1]] else ''
        rows.append(row)

    print("Results (raw):")
    print(pd.DataFrame(rows).to_markdown(index=False))
    print("\nResults (tallied):")
    print(format_output(counters=counters, rmap={i+1: provider for i, provider in enumerate(providers)}))
