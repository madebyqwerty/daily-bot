
from discord.ext import commands, tasks
from zoneinfo import ZoneInfo
import discord, datetime, json, dotenv

with open("settings.json", "r") as read_file: data = json.load(read_file)
REPORT_TIME = datetime.datetime.strptime(data["time"], '%H:%M')
CHANNEL_ID = int(data["channel_id"])
MESSAGE = data["message"]
config = dotenv.dotenv_values(".env")
TOKEN = config["TOKEN"]

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
    my_task.start()
    print(f'{client.user} online!')

time = datetime.time(hour=REPORT_TIME.hour, minute=REPORT_TIME.minute, tzinfo=ZoneInfo("Europe/Prague"))
@tasks.loop(time=time)
async def my_task():
    channel = client.get_channel(CHANNEL_ID)
    message = await channel.send(MESSAGE.replace("%date%", datetime.datetime.now().strftime("%d/%m")))
    await channel.create_thread(name=datetime.datetime.now().strftime("%d/%m"), message=message)

client.run(TOKEN)