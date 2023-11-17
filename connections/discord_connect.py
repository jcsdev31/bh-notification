import discord

class Channel:
    def __init__(self, client, ann_id, app_id, dead_id):
        self.ann = client.get_channel(ann_id)
        self.app = client.get_channel(app_id)
        self.dead = client.get_channel(dead_id)

# Create a Discord client with default intents
def startClient():
    intents = discord.Intents.default()
    return discord.Client(intents=intents)
    
def getChannel(client, server_name):
    ann_id = ann_channel_list[server_name]
    app_id = app_channel_list[server_name]
    dead_id = dead_channel_list[server_name]
    
    channel = Channel(client, ann_id, app_id, dead_id)
    
    return channel
        
ann_channel_list = {
    'Opera Phantom': 1128801882559762552,
    'Boulders and Horns': 1130856686882664479,
    'Tome of Glory': 1128802609650745424,
    'Manila': 1128801527969091736,
    'Frenetic Land': 1128800941743812718,
    'Test-Server': 1131350310284185631
}

app_channel_list = {
    'Opera Phantom': 1128801894542884865,
    'Boulders and Horns': 1130856726124576828,
    'Tome of Glory': 1128802659965620294,
    'Manila': 1128801544473677985,
    'Frenetic Land': 1128801060341948588,
    'Test-Server': 1131350310284185631
}

dead_channel_list = {
    'Opera Phantom': 1128801902478499950,
    'Boulders and Horns': 1130856748513771530,
    'Tome of Glory': 1128802668102565958,
    'Manila': 1128801554686820432,
    'Frenetic Land': 1128801081879699513,
    'Test-Server': 1131350334908932197
}

# ann_channel_list = {
#     'Opera Phantom': 1128801882559762552,
#     'Boulders and Horns': 1130856686882664479,
#     'Tome of Glory': 1128802609650745424,
#     'Manila': 1128801527969091736,
#     'Frenetic Land': 1128800941743812718,
#     'Test-Server': 1131350310284185631
# }

# app_channel_list = {
#     'Opera Phantom': 1128801894542884865,
#     'Boulders and Horns': 1130856726124576828,
#     'Tome of Glory': 1128802659965620294,
#     'Manila': 1128801544473677985,
#     'Frenetic Land': 1128801060341948588,
#     'Test-Server': 1131350326855880734
# }

# dead_channel_list = {
#     'Opera Phantom': 1128801902478499950,
#     'Boulders and Horns': 1130856748513771530,
#     'Tome of Glory': 1128802668102565958,
#     'Manila': 1128801554686820432,
#     'Frenetic Land': 1128801081879699513,
#     'Test-Server': 1131350334908932197
# }