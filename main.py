
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

def calculate_wait_time(target_time):
    now = datetime.datetime.now()
    hours = int(target_time.split(":")[0])-now.hour
    minutes = int(target_time.split(":")[1])-now.minute
    time = (hours*60*60) + (minutes*60)
    if time < 0: 
        return (24*60*60) - abs(time)
    return time

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
    print(calculate_wait_time(REPORT_TIME))
    await asyncio.sleep(calculate_wait_time(REPORT_TIME))

client.run(TOKEN)