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

import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


def format_output(counters: Dict, rmap: Dict[int, str]) -> str:
    jdump = json.dumps(counters, indent=4)
    for k, v in rmap.items():
        jdump = jdump.replace(f'"{k}"', f'"{v}"')

    return jdump


def detect_providers_in_order(path_to_logs: Path, provider_part_idx: int = None) -> List[str]:
    """
    Infer from the path provided which providers were used to create the log files.

    Assumes paths of format similar to:
    .../data/responses/chatgpt_vs_gemini_vs_claude/v1/

    This would return (noting the order is important):
    ["chatgpt", "gemini", "claude"]
    """
    provider_part = [part for part in path_to_logs.parts if '_vs_' in part]
    if len(provider_part) == 0:
        provider_part = [path_to_logs.parts[provider_part_idx or -1]]  # assume last part unless overridden by argument
    provider_part = provider_part[0]

    return provider_part.split('_vs_')


def extract_final_preferences_from_log_files(path_to_logs: Path) -> pd.DataFrame:
    providers = detect_providers_in_order(path_to_logs=path_to_logs)
    min_provider_len = min([len(p) for p in providers])
    log_files = sorted(os.listdir(path_to_logs))

    data_rows = []

    for i, log_file in enumerate(log_files):
        prompt_no = log_file.split(".")[0].replace("prompt", "")

        with open(Path(path_to_logs) / log_file, 'r') as f:
            log = f.read()

        log = log.split("Final preference results:")[1]  # Discard everything but final ratings
        for k, provider_rater in enumerate(providers):
            # Content between provider titles, e.g.
            # chatgpt
            # _______
            # 1. ...
            # claude
            # ______
            provider_result = log.split('_'*min_provider_len)[k+1]
            # print(f'{provider_result[:10]=}')

            pattern = "(\d)\.[ ]*\**[a-zA-Z0-9 ]+\(([a-z]+)\)"
            matches = list(set(re.findall(pattern, provider_result)))
            if len(matches) != len(providers):
                print('----')
                print(log_file)
                print(provider_rater)
                print(matches)
                print('----')

            for rank, provider in matches:
                data_rows.append({
                    'prompt_no': prompt_no,
                    'provider_rater': provider_rater,
                    'provider_responder': provider,
                    'rank': rank,
                })

    return pd.DataFrame(data_rows)


if __name__ == "__main__":

    args = argparse.ArgumentParser(description="Extract preference data from log files generated from using prefer.py")
    args.add_argument('--path', required=True, type=str, help="root directory where output log files are stored")
    args.add_argument(
        '--subfolder', type=str, default=None,
        help="""
        specify a 1-level directory structure below root path
          (None implies there is no structure, i.e. logs stored directly in root path)
          e.g. "round" means that there are multiple subfolders storing log files, e.g.: 
          path/
            round0/
              prompt00.log
              prompt01.log
              ...
            round1/
              ...
            ...  
        """
    )
    args = args.parse_args()

    root_path = Path(args.path)
    if args.subfolder is None:
        # This case means there is a flat structure => log files stored directly under args.path
        df_rank = extract_final_preferences_from_log_files(path_to_logs=root_path)
    else:
        # This case means there are multiple log file directories to iterate through
        df_rank = pd.DataFrame(None)
        for logs_subfolder in sorted(root_path.glob(f'{args.subfolder}*')):
            print(f'Processing subfolder: {logs_subfolder.parts[-1]}')
            my_df_rank = extract_final_preferences_from_log_files(path_to_logs=logs_subfolder)
            my_df_rank['subfolder'] = logs_subfolder.parts[-1]
            df_rank = pd.concat([df_rank, my_df_rank])
        df_rank.reset_index(drop=True, inplace=True)

    df_rank['rank'] = df_rank['rank'].astype(int)
    df_rank['top-1'] = df_rank['rank'].apply(lambda rank: rank == 1)
    df_rank['top-2'] = df_rank['rank'].apply(lambda rank: rank <= 2)
