import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Dict


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
    counters = {provider: Counter() for provider in providers}

    for response_file in sorted(response_files):

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

    print("Results:")
    print(format_output(counters=counters, rmap={i+1: provider for i, provider in enumerate(providers)}))
