import csv
import logging
from typing import List, Union, Callable

from .import_statement import ImportStatement
from .utils import guess_delimiter

logger = logging.getLogger(__name__)


class Importer(object):
    """Base class for importers"""

    def __init__(
        self,
        header_converter: Union[dict, Callable[[str], str | None]],
        date_fmt: str,
        delimiter: str | None = None,
        encoding: str | None = None,
    ):
        """Initializes Importer object

        Args:
            date_fmt (str): date format used inside the csv
            header_converter (Union[dict, function]): converts csv file headers to standard headers.
            If converter is a function, it should return None if the csv header should be skipped
            delimiter (str|None, optional): The delimiter used in the csv. Defaults to None.
        """
        self.fmt = date_fmt
        self.header_converter = header_converter
        self.delimiter = delimiter
        self.encoding = encoding

    def convert_header(self, csv_header):
        if callable(self.header_converter):
            return self.header_converter(csv_header)
        else:
            return self.header_converter.get(csv_header)

    def import_transactions(self, csv_path: str) -> List[ImportStatement]:
        """imports transactions from a csv file

        Args:
            csv_path (List[ImportStatement]): path to the csv file
        """
        delimiter = self.delimiter or guess_delimiter(csv_path)

        data = []
        with open(csv_path, encoding=self.encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=delimiter)
            csv_headers = reader.fieldnames or []
            for r, row in enumerate(reader):
                try:
                    translated_row = {
                        self.convert_header(k): v
                        for k, v in row.items()
                        if self.convert_header(k)
                    }
                    data.append(translated_row)
                except Exception:
                    logger.warning(f"Error in importing line {r} from {csv_path!r}")
        return data
