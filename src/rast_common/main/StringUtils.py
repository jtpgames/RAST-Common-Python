import argparse
import os
from datetime import datetime
from re import search


def get_date_from_string(line):
    return search(r"\d*-\d*-\d*", line).group().strip()


def contains_timestamp_with_ms(line: str):
    return search(r"(?<=\])\s*\d*-\d*-\d*\s\d*:\d*:\d*\.\d*", line) is not None


def get_timestamp_from_string(line: str):
    return search(r"(?<=\])\s*\d*-\d*-\d*\s\d*:\d*:\d*\.?\d*", line).group().strip()


def get_timestamp_from_line(line: str) -> datetime:
    if contains_timestamp_with_ms(line):
        format_string = '%Y-%m-%d %H:%M:%S.%f'
    else:
        format_string = '%Y-%m-%d %H:%M:%S'

    return datetime.strptime(
        get_timestamp_from_string(line),
        format_string
    )


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
