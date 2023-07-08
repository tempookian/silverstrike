import csv
import logging

logger = logging.getLogger(__name__)


def guess_delimiter(csv_file: str):
    """receives a csv file and tries to guess the delimiter

    Args:
        csv_file (str): path to csv file
    """
    with open(csv_file, "r") as f:
        dialect = csv.Sniffer().sniff(f.readline())
        return dialect.delimiter
    
