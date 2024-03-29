# Define the words/phrases that you want to look for in the banner
banner_texts = [
    "Eclipse w",
    "Fly w",
    "Mastering w",
    "Ghostring w",
    "Toad w",
    "Dramoh w",
    "Deviling w",
    "Arc An",
    "Angeling w",
    "Priest w",
    "Wolf w",
    "Chimera w",
    "Mysteltainn w",
    "Ogretooth w",
    "Necromancer w",
    "Sieger w",
    "canth w",
    "Skeggiold w",
    "Observation w",
    "Mistress w",
    "Phreeoni w",
    "Kraken w",
    "Eddga w",
    "Maya w",
    "Orc Hero w",
    "Pharaoh w",
    "Orc Lord w",
    "Amon Ra w",
    "ganger w",
    "Holder w",
    "Morroc w",
    "ragon w",
    "Gunka w",
    "Bishop w",
    "f the Dead w",
    "Gioia w",]

# Define a lookup dictionary that maps lookup boss words/phrases from the banner to their actual names
banner_lookup = {
    'Mistress w': 'Mistress',
    'Phreeoni w': 'Phreeoni',
    'Kraken w': 'Kraken',
    'Eddga w': 'Eddga',
    'Maya w': 'Maya',
    'Orc Hero w': 'Orc Hero',
    'Pharaoh w': 'Pharaoh',
    'Orc Lord w': 'Orc Lord',
    'Amon Ra w': 'Amon Ra',
    'ganger w': 'Doppelganger',
    'Holder w': 'Time Holder',
    'Morroc w': 'Morroc',
    'ragon w': 'Lost Dragon',
    'Gunka w': 'Tao Gunka',
    'Bishop w': 'Fallen Bishop',
    'f the Dead w': 'Lord of the Dead',
    'Arc An': 'Arc Angeling',
    'Gioia w': 'Gioia',
    'Eclipse w': 'Eclipse',
    'Fly w': 'Dragon Fly',
    'Mastering w': 'Mastering',
    'Ghostring w': 'Ghostring',
    'Toad w': 'Toad',
    'Dramoh w': 'King Dramoh',
    'Deviling w': 'Deviling',
    'Angeling w': 'Angeling',
    'Priest w': 'Dark Priest',
    'Wolf w': 'Vagabond Wolf',
    'Chimera w': 'Chimera',
    'Mysteltainn w': 'Mysteltainn',
    'Ogretooth w': 'Ogretooth',
    'Necromancer w': 'Necromancer',
    'Sieger w': 'Naght Sieger',
    'canth w': 'Coelacanth',
    'Skeggiold w': 'Skeggiold',
    'Observation w': 'Observation',
}

# Define a dictionary for the status of bosses
boss_status = {
    0: 'Longer Time',
    1: 'Short Time',
    2: 'Refreshing Soon',
    3: 'Appeared',
}

# Define a dictionary for the status of mini bosses
# The initial status is set to -1 which might represent 'unknown' or 'not yet checked'
minis = {
    'Dragon Fly': -1,
    'Eclipse': -1,
    'Ghostring': -1,
    'Mastering': -1,
    'Toad': -1,
    'King Dramoh': -1,
    'Deviling': -1,
    'Angeling': -1,
    'Dark Priest': -1,
    'Vagabond Wolf': -1,
    'Chimera': -1,
    'Mysteltainn': -1,
    'Necromancer': -1,
    'Ogretooth': -1,
    'Naght Sieger': -1,
    'Coelacanth': -1,
    'Observation': -1,
    'Skeggiold': -1,
}

# Define a dictionary for the status of MVP bosses
# The initial status is set to -1 which might represent 'unknown' or 'not yet checked'
mvps = {
    'Mistress': -1,
    'Phreeoni': -1,
    'Kraken': -1,
    'Eddga': -1,
    'Orc Hero': -1,
    'Maya': -1,
    'Pharaoh': -1,
    'Orc Lord': -1,
    'Amon Ra': -1,
    'Doppelganger': -1,
    'Morroc': -1,
    'Time Holder': -1,
    'Tao Gunka': -1,
    'Lost Dragon': -1,
    'Lord of the Dead': -1,
    'Fallen Bishop': -1,
    'Arc Angeling': -1,
    'Gioia': -1,
}

is_announced = {
    'Dragon Fly': False,
    'Eclipse': False,
    'Ghostring': False,
    'Mastering': False,
    'Toad': False,
    'King Dramoh': False,
    'Angeling': False,
    'Deviling': False,
    'Vagabond Wolf': False,
    'Dark Priest': False,
    'Mysteltainn': False,
    'Chimera': False,
    'Necromancer': False,
    'Ogretooth': False,
    'Coelacanth': False,
    'Naght Sieger': False,
    'Skeggiold': False,
    'Observation': False,
    'Mistress': False,
    'Phreeoni': False,
    'Kraken': False,
    'Eddga': False,
    'Maya': False,
    'Orc Hero': False,
    'Pharaoh': False,
    'Orc Lord': False,
    'Amon Ra': False,
    'Doppelganger': False,
    'Time Holder': False,
    'Morroc': False,
    'Lost Dragon': False,
    'Tao Gunka': False,
    'Lord of the Dead': False,
    'Fallen Bishop': False,
    'Arc Angeling': False,
    'Gioia': False,
}