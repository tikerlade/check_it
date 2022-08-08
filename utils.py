"""
File with utils of different kind.
"""
import yaml

from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.console import Console

import stop_criterias
from argparse_settings import argparse_obj


def load_config_file(filename):
    with open(filename, 'r') as fin:
        return yaml.safe_load(fin)


def get_config(yaml_config_filename='config.yaml'):
    args = argparse_obj.parse_args()

    if args.urls:
        return vars(args)
    return load_config_file(yaml_config_filename)


def get_stop_criteria(config):
    str_to_criteria = {'symbols_diff': stop_criterias.min_char_diff_criteria,
                       'str_to_find': stop_criterias.regex_criteria}
    console = Console()

    if config['symbols_diff'] == 0 and config['str_to_find'] == "":
        console.print("[red] You must specify any stop criteria.")
        return None
    elif config['symbols_diff'] > 0 and config['str_to_find'] != "":
        console.print("[red]You enabled >1 stop criterias. Pls select one option:")
        console.print("\t1. Minimum char difference between old and new version")
        console.print("\t2. Regex pattern found on page")
        stop_criteria_num = Prompt.ask("Your option:", choices=["1", "2"])
        stop_criteria_option = 'symbols_diff' if stop_criteria_num == '1' else 'str_to_find'
    else:
        stop_criteria_option = 'symbols_diff' if config['symbols_diff'] else 'str_to_find'

    return str_to_criteria[stop_criteria_option]


def get_table(result):
    table = Table()

    table.add_column("ID")
    table.add_column("Link")
    table.add_column("Updated")

    for idx, url in enumerate(result):
        table.add_row(
            f"{idx}", Markdown(f"[{url}]({url})"), "[green]:heavy_check_mark:" if result[url] else "[red]:cross_mark:",
            end_section=True
        )

    return table
