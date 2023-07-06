
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import discord, datetime, json, os, dotenv

with open("settings.json", "r") as read_file: data = json.load(read_file)
CHANNEL_ID = int(data["channel_id"])
REPORT_TIME0 = datetime.datetime.strptime(data["time0"], '%H:%M')
MESSAGE0 = data["message0"]
REPORT_TIME1 = datetime.datetime.strptime(data["time1"], '%H:%M')
MESSAGE1 = data["message1"]
try: TOKEN = os.environ["TOKEN"]
except: TOKEN = dotenv.dotenv_values(".env")["TOKEN"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    task0.start()
    task1.start()
    print(f'{client.user} online!')

time0 = datetime.time(hour=REPORT_TIME0.hour, minute=REPORT_TIME0.minute, tzinfo=ZoneInfo("Europe/Prague"))
@tasks.loop(time=time0)
async def task0():
    channel = client.get_channel(CHANNEL_ID)
    message = await channel.send(MESSAGE0.replace("%date%", datetime.datetime.now().strftime("%d/%m")))
    await channel.create_thread(name=datetime.datetime.now().strftime("%d/%m"), message=message)

time1 = datetime.time(hour=REPORT_TIME1.hour, minute=REPORT_TIME1.minute, tzinfo=ZoneInfo("Europe/Prague"))
@tasks.loop(time=time1)
async def task1():
    channel = client.get_channel(CHANNEL_ID)
    message = await channel.send(MESSAGE1.replace("%date%", datetime.datetime.now().strftime("%d/%m")))
    await message.add_reaction("❌")
    await message.add_reaction("✅")

client.run(TOKEN)