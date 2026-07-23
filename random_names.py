"""
random_names.py
----------------
Generates a fallback name when OCR fails or no name can be
confidently detected on a page. Picks a random first + last name
so the result looks like a real detected name (e.g. 'david_akoto')
instead of an obviously-fake placeholder. file_manager.py appends
its own random (1234) number on top of whatever this returns, so
no number is generated here.
"""

import random

_FIRST_NAMES = [
    "David", "Emmanuel", "Kwame", "Kofi", "Samuel", "Michael",
    "Joseph", "Daniel", "Isaac", "Benjamin", "Gabriel", "Nathaniel",
    "Ama", "Akosua", "Abena", "Efua", "Grace", "Comfort",
    "Patience", "Mary", "Sarah", "Elizabeth", "Linda", "Priscilla",
]

_LAST_NAMES = [
    "Akoto", "Mensah", "Owusu", "Boateng", "Asante", "Appiah",
    "Osei", "Agyemang", "Adjei", "Amoah", "Darko", "Antwi",
    "Frimpong", "Yeboah", "Addo", "Ofori", "Sarpong", "Gyasi",
]


def generate_random_name() -> str:
    """Return something like 'David_Akoto'. A random number is added later."""
    first = random.choice(_FIRST_NAMES)
    last = random.choice(_LAST_NAMES)
    return f"{first}_{last}"