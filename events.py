# home_base_bot.py
import os
import discord
import random
import asyncio
import csv

from asgiref.sync import async_to_sync, sync_to_async

client = discord.Client()
#init the three lists we will need
places = []
events = []
tips = []




# I place my token in a key.txt file
def load_discord_token():
    with open("key.txt", "r") as f:
        return f.read().rstrip("\n")


def random_event(place):
    roll = random.randint(1, 6)
    with open('events.txt', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';', quotechar='|')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print("loading event")
                line_count += 1
            

            if int(row["roll"]) == roll:
                #print(row["text"])
                if row["code"]=="pincrease":
                    res=town.get_res()
                    percent=(int(row["amount"]))/100#convert to decimal cause of reasons
                    
                    res[row["resource"]]=(percent*res[row["resource"]])+res[row["resource"]]
                    town.set_res(res)
                    pass
                elif row["code"]=="pdecrease":
                    res=town.get_res()
                    percent=(int(row["amount"]))/100#convert to decimal cause of reasons
                    
                    res[row["resource"]]=res[row["resource"]]-(percent*res[row["resource"]])
                    town.set_res(res)
                    pass
                 
                elif row["code"]=="increase":
                    res=town.get_res()
                                    
                    res[row["resource"]]+=int(row["amount"])
                    town.set_res(res)
                 #   pass
                elif row["code"]=="decrease":
                    res=town.get_res()
                                    
                    res[row["resource"]]+=int(-row["amount"])
                    town.set_res(res)
                 #   pass
                
                return "Random event:"+row["text"]
                
                pass







@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = str.split(str.lower(message.content))
    if len(msg) == 3:
        if msg[1] == "count":
            random_number=random.randint(1000000)
            return_string =random.choice(places)+" has "+str(random_number)+"Cases of the Covid19 Virus"
                    await message.channel.send(return_string)

    if message.content == "help":
        await message.channel.send("Commands: 'Tips, help, count'")
        pass
    if message.content == "tip":
        return_string = random.choice(tips)
        await message.channel.send(return_string)
        pass


async def events_rotation():
    await client.wait_until_ready()
    print("event rotation started")
    

    while client.is_closed:

        discord_channel = client.get_channel(town.get_channel())
        return_string = await sync_to_async(random_event())
        await discord_channel.send(return_string)
        await asyncio.sleep(10)
        # 3600 seconds in an hour just in case you didn't already know that
    print("?")
    pass


# load places
f = open("places.txt", "r")
i = 0
for line in f:
    places.append(place(line.rstrip("\n")))
    i += 1
f.close()
# load events

f = open("events.txt", "r")
i = 0
for line in f:
    places.append(event(line.rstrip("\n")))
    i += 1
f.close()
#load tips

f = open("tips.txt", "r")
i = 0
for line in f:
    places.append(tips(line.rstrip("\n")))
    i += 1
f.close()
for each in places:
    each.load_from_file()
    print(each.get_name())

discord_token = load_discord_token()
token = os.getenv('DISCORD_TOKEN')

client.loop.create_task(events_rotation())
client.run(load_discord_token())
