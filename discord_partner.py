import waitlist as wl
import asyncio
import discord
import config
from constants.bosses import mvps, minis
import time

class CommandCenter:
    admin_id = "<@1043418696560951306>"
    channel_id = 1178294879449784380
    guild_id = 1096915549302313011
    channel = None
    guild = None
    emojis = None
    active_instance = None
    
    def __init__(self):
        self.channel = client.get_channel(self.channel_id)
        self.guild = client.get_guild(self.guild_id)
        self.emojis = self.guild.emojis
    
class Discord:
    guild = None
    category = None
    roles_channel = None
    bot_announcements = None
    bot_guide = None
    live_notifications = None
    drop_database = None
    boss_channels = {}
    
    def __init__(self, guild_id):
        self.guild = client.get_guild(guild_id)
    
    async def setup_guild(self):
        await self.setup_category()
        await self.setup_roles_channel()
        await self.setup_bot_announcements()
        await self.setup_bot_guide()
        await self.setup_live_notifications()
        await self.setup_drop_database()
        
    async def setup_category(self):
        category_name = "MVP/Mini Notification"
        self.category = discord.utils.get(self.guild.categories, name=category_name)
        
    async def setup_roles_channel(self):
        roles_channel_name = "get-bh-roles"
        self.roles_channel = discord.utils.get(self.category.channels, name=roles_channel_name)
    
    async def setup_bot_announcements(self):
        bot_announcements_name = "bot-announcements"
        self.bot_announcements = discord.utils.get(self.category.channels, name=bot_announcements_name)
        
    async def setup_bot_guide(self):
        bot_guide_name = "bot-guide"
        self.bot_guide = discord.utils.get(self.category.channels, name=bot_guide_name)
    
    async def setup_live_notifications(self):
        live_notifications_name = "live-notifications"
        self.live_notifications = discord.utils.get(self.category.channels, name=live_notifications_name)
    
    async def setup_drop_database(self):
        drop_database_name = "drop"
        self.drop_database = discord.utils.get(self.category.channels, name=drop_database_name)


def startClient():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    return discord.Client(intents=intents)
        
# Create a Discord client
client = startClient()

# Event listener for when the bot is ready
@client.event
async def on_ready():
    global cc, active_guilds, bosses
    
    bosses = list(mvps.keys()) + list(minis.keys())
    
    cc = CommandCenter()
    active_guilds = []

    active_guilds_data = wl.get_active_guilds()
    for guild_id in active_guilds_data:
        active_guild = Discord(guild_id)
        await active_guild.setup_guild()
        is_already_active = False
        
        for obj in active_guilds:
            if obj.guild.id == guild_id:
                print(f"***{obj.guild.name} (ID: {obj.guild.id}) is already active!***")
                is_already_active = True
        
        if not is_already_active:
            active_guilds.append(active_guild)
            print(f"***{active_guild.guild.name} (ID: {active_guild.guild.id}) has been set as an active guild!***")
    
    await process_items()
            
@client.event
async def on_disconnect():
    print('Bot disconnected from Discord!')
    
async def process_items():
    print('process_items starting')
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 300:  # 300 seconds = 5 minutes
            # Do something when 5 minutes have elapsed without changeDetected
            await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} 5 minutes has passed without any updates!!! Routine check is recommended.*** ⚠️⚠️")
            start_time = time.time()  # Reset the start time
            
        type = wl.get_type_waitlist()
        
        if type == "haze":
            is_not_empty = wl.check_haze_waitlist()
            if is_not_empty:
                await process_haze()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} haze type detected but no haze to push!*** ⚠️⚠️")
                
        elif type == "message":
            is_not_empty = wl.check_message_waitlist()
            if is_not_empty:
                await process_message()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} message type detected but no message to push!*** ⚠️⚠️")
                
        elif type == "dead":
            is_not_empty = wl.check_image_waitlist()
            if is_not_empty:
                await process_dead()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} dead type detected but no dead to push!*** ⚠️⚠️")
                
        elif type == "update":
            start_time = time.time()
            is_not_empty = wl.check_status_waitlist()
            if is_not_empty:
                await process_update()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} update type detected but no update to push!*** ⚠️⚠️")
                
        elif type == "error":
            is_not_empty = wl.check_error_waitlist()
            if is_not_empty:
                await process_error()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} error type detected but no error to push!*** ⚠️⚠️")
                
        elif type == "error_image":
            is_not_empty = wl.check_errimage_waitlist()
            if is_not_empty:
                await process_error_image()
            else:
                await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} errimage type detected but no errimage to push!*** ⚠️⚠️")
                
        else:
          await pop_all_json()
                
        await asyncio.sleep(1)
        
async def process_haze():
    new_haze = wl.get_haze_waitlist()
    await send_haze(new_haze)
    
async def process_message():
    new_message = wl.get_message_waitlist()
    message, boss_name = new_message
    await send_message(message, boss_name)
    
async def process_dead():
    new_image = wl.get_image_waitlist()
    message, boss_name, image_buffer = new_image
    await send_image(message, boss_name, image_buffer)
    
async def process_update():
    new_update = wl.get_status_waitlist()
    boss_name, status, is_announced = new_update
    await update_status(boss_name, status, is_announced)
    
async def process_error():
    new_error = wl.get_error_waitlist()
    error_report, e = new_error
    await send_error(error_report, e)
    
async def process_error_image():
    new_errimage = wl.get_errimage_waitlist()
    message, image_buffer = new_errimage
    await send_error_image(message, image_buffer)
    
async def pop_all_json():
    ## UPDATE ##
    while True:
        type = wl.check_status_waitlist()
        if type:
            await process_update()
        else:
            break
    ## MESSAGE ##
    while True:
        type = wl.check_message_waitlist()
        if type:
            await process_message()
        else:
            break
    ## DEAD ##
    while True:
        type = wl.check_image_waitlist()
        if type:
            await process_dead()
        else:
            break
    ## HAZE ##
    while True:
        type = wl.check_haze_waitlist()
        if type:
            await process_haze()
        else:
            break
    ## ERROR ##
    while True:
        type = wl.check_error_waitlist()
        if type:
            await process_error()
        else:
            break
    ## ERROR_IMAGE ##
    while True:
        type = wl.check_errimage_waitlist()
        if type:
            await process_error_image()
        else:
            break
    
# Returns a pre-formatted emoji_id
def getEmoji(boss_name):
    formatted_string = boss_name.lower().replace(" ", "")
    
    for emoji in cc.emojis:
        if emoji.name == formatted_string:
            return f"<:{emoji.name}:{emoji.id}>"
    
    print("No emoji matched the provided boss name")

async def send_error(error_report, e):
    if e == "banner-not-found":
        await cc.channel.send(f"⚠️⚠️ ***{wl.instance_id} ran into an error:*** *{error_report}* ⚠️⚠️")
        print(error_report)
    else:
        await cc.channel.send(f"{cc.admin_id} ⚠️⚠️ ***{wl.instance_id} ran into an error:*** *{error_report}* ⚠️⚠️")
        print(str(e))

async def send_error_image(message, image):
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        while retries < max_retries and not sent:
            try:
                image.seek(0)
                await cc.channel.send(message, file=discord.File(image, filename="battle-results.png"))
                print("Message sent successfully.")
                sent = True
            except discord.errors.HTTPException as e:
                print(f"Error encountered while trying to send a message: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)
        
        if not sent:
            print("Max retries reached. Message could not be sent.")
            
async def send_message(message, boss):    
    for guild in active_guilds:
        
        role_name = boss
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        msg = f"{getEmoji(boss)} {role.mention} {message}"
        
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        while retries < max_retries and not sent:
            try:
                await guild.live_notifications.send(msg)
                sent = True
            except discord.errors.HTTPException as e:
                print(f"Error encountered while trying to send a message: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)
        
        if not sent:
            print("Max retries reached. Message could not be sent.")

async def send_haze(message):
    for guild in active_guilds:
        
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        
        role_name = "BH Bot"
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        
        while retries < max_retries and not sent:
            try:
                await guild.live_notifications.send(f"{role.mention} {message}")
                sent = True
            except discord.errors.HTTPException as e:
                print(f"Error encountered while trying to send a message: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)
        
        if not sent:
            print("Max retries reached. Message could not be sent.")
            
async def send_dead(guild, message):
    max_retries = 3
    retry_interval = 5
    retries = 0
    sent = False
    while retries < max_retries and not sent:
        try:
            await guild.live_notifications.send(message)
            sent = True
        except discord.errors.HTTPException as e:
            print(f"Error encountered while trying to send a message: {e}")
            retries += 1
            print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
            await asyncio.sleep(retry_interval)
    
    if not sent:
        print("Max retries reached. Message could not be sent.")
    
async def send_image(message, boss, image):
    for guild in active_guilds:
        
        role_name = boss
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        msg = f"{getEmoji(boss)} {role.mention} {message}"
        
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        message_link = None
        while retries < max_retries and not sent:
            try:
                image.seek(0)
                temp_msg = f"{getEmoji(boss)} **{boss}** {message}"
                res = await guild.drop_database.send(temp_msg, file=discord.File(image, filename="battle-results.png"))
                message_link = res.jump_url
                sent = True
            except discord.errors.HTTPException as e:
                print(f"Error encountered while trying to send a message: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)
        
        if sent:
            msg = f"{msg} {message_link}"
            await send_dead(guild, msg)
        
        if not sent:
            print("Max retries reached. Message could not be sent.")        

# Function to get the emoji based on the status
def get_status_emoji(status):
    if status == 0:
        return "🔴"
    elif status == 1:
        return "🟠"
    elif status == 2:
        return "🟡"
    elif status == 3:
        return "🟢"
    else:
        return ""

async def update_status(boss, status, is_announced):
    for guild in active_guilds:
        is_update = False
        
        role_name = boss
        
        # Check if the role already exists
        role = discord.utils.get(guild.guild.roles, name=role_name)
        
        for i in range(4):
            channel_name = f"{get_status_emoji(i)}{boss}"
            channel = discord.utils.get(guild.guild.channels, name=channel_name)
            if channel:
                await channel.delete()
                print(f"{channel_name} voice channel deleted in {guild.guild.name}")
                position = channel.position
                is_update = True
                break
            channel_name = f"{get_status_emoji(i)}🌟{boss}"
            channel = discord.utils.get(guild.guild.channels, name=channel_name)
            if channel:
                await channel.delete()
                position = channel.position
                is_update = True
                break
        
        # Define the permissions
        overwrites = {
            guild.guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
            role: discord.PermissionOverwrite(view_channel=True),
            guild.guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True, connect=True)
        }
            
        # Create the voice channel within the category
        if is_announced:
            channel_name = f"{get_status_emoji(status)}🌟{boss}"
        else:
            channel_name = f"{get_status_emoji(status)}{boss}"
        
        max_retries = 3
        retry_interval = 5
        retries = 0
        sent = False
        while retries < max_retries and not sent:
            try:
                if is_update:
                    channel = await guild.category.create_voice_channel(name=channel_name, overwrites=overwrites, position=position)
                else:
                    channel = await guild.category.create_voice_channel(name=channel_name, overwrites=overwrites)
                sent = True
                
                print(f"{channel_name} voice channel created in {guild.guild.name}")
            except Exception as e:
                print(f"Error: {e}")
                retries += 1
                print(f"Retrying ({retries}/{max_retries}) in {retry_interval} seconds...")
                await asyncio.sleep(retry_interval)

        if not sent:
            print("Max retries reached. Message could not be sent.")
        
        # Save boss_name:channel to boss_channels
        guild.boss_channels[boss] = channel

client.run(config.BOT_TOKEN)