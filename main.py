
from discord.ext import commands, tasks
import discord, datetime, asyncio, json, dotenv

with open("settings.json", "r") as read_file: data = json.load(read_file)
REPORT_TIME = data["time"]
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

@tasks.loop(hours=24)
async def my_task():
    channel = client.get_channel(CHANNEL_ID)
    message = await channel.send(MESSAGE.replace("%date%", datetime.datetime.now().strftime("%d/%m")))
    await channel.create_thread(name=datetime.datetime.now().strftime("%d/%m"), message=message)

@my_task.before_loop
async def before_msg1():
    now = datetime.datetime.now()
    time = (abs(int(REPORT_TIME.split(":")[0])-now.hour)*60*60) + (abs(int(REPORT_TIME.split(":")[1])-now.minute)*60)
    await asyncio.sleep(time)

client.run(TOKEN)