# Define the words/phrases that you want to look for in the banner
banner_texts = [   
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
    "Time w",
    "Morroc w",
    "Lost Dragon w",
    "Tao Gunka w",
    "Bishop w",
    "Dead w",
    "Arc Ang",
    "Gioia w",
    "Eclipse w",
    "Dragon Fly w",
    "Mastering w",
    "Ghostring w",
    "Toad w",
    "Dramoh w",
    "Deviling w",
    "Angeling w",
    "Priest w",
    "Wolf w",
    "Chimera w",
    "Mysteltainn w",
    "Ogretooth w",
    "Necromancer w",
    "Sieger w",
    "Coelacanth w",
    "Skeggiold w",
    "Observation w",]

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
    'Time w': 'Overseer of Time',
    'Morroc w': 'Morroc',
    'Lost Dragon w': 'Lost Dragon',
    'Tao Gunka w': 'Tao Gunka',
    'Bishop w': 'Fallen Bishop',
    'Dead w': 'Lord of the Dead',
    'Arc Ang': 'Arc Angeling',
    'Gioia w': 'Gioia',
    'Eclipse w': 'Eclipse',
    'Dragon Fly w': 'Dragon Fly',
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
    'Coelacanth w': 'Coelacanth',
    'Skeggiold w': 'Skeggiold',
    'Observation w': 'Observation',
}

# Define a dictionary that maps full boss names to their corresponding emoji IDs
emoji_id = {
    'Mistress' : '<:mistress:1128500941654601758>',
    'Phreeoni' : '<:phreeoni:1128500973225136200>',
    'Kraken' : '<:kraken:1128500912948776970>',
    'Eddga' : '<:eddga:1128500904291729408>',
    'Maya' : '<:maya:1128500937917481044>',
    'Orc Hero' : '<:orchero:1128500955172851732>',
    'Pharaoh' : '<:pharaoh:1128500967042732163>',
    'Orc Lord' : '<:orclord:1128500958037540916>',
    'Amon Ra' : '<:amonra:1128500895320113293>',
    'Doppelganger' : '<:doppelganger:1128500900659470438>',
    'Overseer of Time' : '<:overseeroftime:1128500962076663878>',
    'Morroc' : '<:morroc:1128500946008277103>',
    'Lost Dragon' : '<:lostdragon:1128500935195369533>',
    'Tao Gunka' : '<:taogunka:1128500987758391326>',
    'Fallen Bishop' : '<:fallenbishop:1128500908431527956>',
    'Lord of the Dead' : '<:lordofthedead:1128500924466331678>',
    'Arc Angeling' : '<:arcangeling:1156347567530070077>',
    'Gioia' : '<:gioia:1156347569920815165>',
    'Eclipse' : '<:eclipse:1128501089814192250>',
    'Dragon Fly' : '<:dragonfly:1128501085783457833>',
    'Mastering' : '<:mastering:1128501105152761936>',
    'Ghostring' : '<:ghostring:1128501095765909615>',
    'Toad' : '<:toad:1128501130767368283>',
    'King Dramoh' : '<:kingdramoh:1128501100933304340>',
    'Deviling' : '<:deviling:1128501081677250632>',
    'Angeling' : '<:angeling:1128501060651204688>',
    'Dark Priest' : '<:darkpriest:1128501077571022879>',
    'Vagabond Wolf' : '<:vagabondwolf:1128501134886182955>',
    'Chimera' : '<:chimera:1128501071283753020>',
    'Mysteltainn' : '<:mysteltainn:1128501109095399504>',
    'Ogretooth' : '<:ogretooth:1128501126266892379>',
    'Necromancer' : '<:necromancer:1128501119723769918>',
    'Naght Sieger' : '<:naghtsieger:1128501113625268424>',
    'Coelacanth' : '<:coelacanth:1128501073599008770>',
    'Skeggiold' : '<:skeggiold:1156347499091599463>',
    'Observation' : '<:observation:1156347494511415316>',
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
    'Angeling': -1,
    'Deviling': -1,
    'Vagabond Wolf': -1,
    'Dark Priest': -1,
    'Mysteltainn': -1,
    'Chimera': -1,
    'Necromancer': -1,
    'Ogretooth': -1,
    'Coelacanth': -1,
    'Naght Sieger': -1,
    'Skeggiold': -1,
    'Observation': -1,
}

# Define a dictionary for the status of MVP bosses
# The initial status is set to -1 which might represent 'unknown' or 'not yet checked'
mvps = {
    'Mistress': -1,
    'Phreeoni': -1,
    'Kraken': -1,
    'Eddga': -1,
    'Maya': -1,
    'Orc Hero': -1,
    'Pharaoh': -1,
    'Orc Lord': -1,
    'Amon Ra': -1,
    'Doppelganger': -1,
    'Overseer of Time': -1,
    'Morroc': -1,
    'Lost Dragon': -1,
    'Tao Gunka': -1,
    'Lord of the Dead': -1,
    'Fallen Bishop': -1,
    'Arc Angeling': -1,
    'Gioia': -1,
}