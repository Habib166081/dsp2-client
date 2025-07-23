from enum import Enum

class AccountType(str, Enum):
    CARD = "CARD"
    CACC = "CACC"

class AccountUsage(str, Enum):
    PRIV = "PRIV"
    ORGA = "ORGA"

class TransactionCreditDebitIndicator(str, Enum):
    CRDT = "CRDT"
    DBIT = "DBIT"

class TransactionStatus(str, Enum):
    BOOK = "BOOK"
    PENDING = "PENDING"
