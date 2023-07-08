import logging
from typing import List

from silverstrike.importers.import_statement import ImportStatement

from .importer import Importer

log = logging.getLogger(__name__)

DATE_FORMAT = "%d.%m.%y"


HEADER_CONVERTER = {
    "Auftragskonto": "account",
    "Buchungstag": "book_date",
    "Valutadatum": "transaction_date",
    "Betrag": "amount",
    "Verwendungszweck": "notes",
    "Kontonummer/IBAN": "iban",
}


def import_transactions(file_path: str) -> List[ImportStatement]:
    sparkasse = Importer(
        date_fmt=DATE_FORMAT,
        delimiter=";",
        encoding="latin1",
        header_converter=HEADER_CONVERTER,
    )

    transactions = sparkasse.import_transactions(file_path)

    return transactions
