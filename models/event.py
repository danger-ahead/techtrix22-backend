from unicodedata import category

from models.category import Category


class Event:
    name: str
    category: Category
    desc: str
    rules: str
    contact: str
    id: int
    fee: int
    tags: list(str)
    regs_enabled: bool
    popular: bool
    flagship: bool
    min_participants: int
    max_participants: int
    info: str
