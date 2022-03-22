import json
import discord
from discord import Intents, Game
from discord.ext import commands, tasks
import aiohttp

#Loads from config file
with open("./config.json", "r") as file:
    secret_file = json.load(file)
_BotToken = secret_file["BotToken"]
_BM_ServerID = secret_file["BM_ServerID"]


client = commands.Bot(command_prefix=")(")

#BotStartUp
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

    


#Every 30s it sets the bot's status to your server pop
@tasks.loop(seconds=30)
async def pop_status():


    url = f"https://api.battlemetrics.com/servers/{_BM_ServerID}" 
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                print(f"Battlemetrics Error with status code: {resp.status}")
            if resp.status == 200:
                resp_dict = json.loads(await resp.text())
                status = resp_dict["data"]["attributes"]["status"] 
                ConnectedPlayers = resp_dict["data"]["attributes"]["players"] 
                MaxPlayers = resp_dict["data"]["attributes"]["maxPlayers"]
                QueuedPlayers = resp_dict["data"]["attributes"]["details"]["rust_queued_players"]
  
       
        if status == "online":
            if QueuedPlayers > 0:
                await client.change_presence(activity=Game(f"{ConnectedPlayers}/{MaxPlayers} (+{QueuedPlayers})"))
                
            else:
                await client.change_presence(activity=Game(f"{ConnectedPlayers}/{MaxPlayers}")) 
        else:
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="[Offline]"))




@pop_status.before_loop
async def before_pop_status():
    await client.wait_until_ready()

if __name__ == "__main__":
    pop_status.start()
    client.run(_BotToken)



