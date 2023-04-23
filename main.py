
from discord.ext import commands
import discord, datetime, asyncio, json

with open("settings.json", "r") as read_file: data = json.load(read_file)
REPORT_TIME = data["time"]
CHANNEL_ID = int(data["channel_id"])
MESSAGE = data["message"]
TOKEN = open("token.txt", "r").read()

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    client.loop.create_task(timer())
    print(f'{client.user} online!')

async def timer():
    while True:
        await asyncio.sleep(1)
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time == REPORT_TIME and (not now.weekday() == 4 or not now.weekday() == 5):
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(MESSAGE)

client.run(TOKEN)