"""
File contains function to compare strings and decide their acceptability.
"""
import re


def min_char_diff_criteria(s1: str, s2: str, config) -> bool:
    diff = sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))
    return diff > config['n_diff']


def regex_criteria(s1: str, s2: str, config) -> bool:
    return bool(re.search(config['str_to_find'], s2))
