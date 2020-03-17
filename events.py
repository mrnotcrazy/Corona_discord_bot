# home_base_bot.py
import os
import discord
import random
import asyncio
import csv

from asgiref.sync import async_to_sync, sync_to_async

client = discord.Client()


class Town:

    def __init__(self, name):
        self._name = name
        self._res = {"population": 100,
                     "lumber": 0,
                     "stones": 0,
                     "labor": 0,
                     "magic": 0,
                     "treasury": 0,
                     "lumber_growth": 0,
                     "stones_growth": 0,
                     "labor_growth": 0,
                     "magic_growth": 0,
                     "income": 0,
                     "upkeep": 0
                     }

        self._channel = 634250073823510529

    def get_name(self):
        return self._name

    def get_res(self):
        return self._res

    def get_channel(self):
        return self._channel

    def set_name(self, name_pass):
        self._name = name_pass

    def set_res(self, res_pass):
        self._res = res_pass
        self.save_to_file()

    def set_channel(self, channel_pass):
        self._channel = channel_pass

    def production_totals(self):
        return "lumber Per Day:" + str(self._res["lumber_growth"]) + "\nStones Per Day:" + str(
            self._res["stones_growth"]) + "\nLabor Per Day:" + str(self._res["labor_growth"]) + "\nMagic Per Day" + str(
            self._res["magic_growth"]) + "\nIncome Per Day:" + str(self._res["income"]) + "\nUpkeep Per Day:" + str(
            self._res["upkeep"])

    def resource_totals(self):
        return "Population:" + str(self._res["population"]) + "\nLumber:" + str(
            self._res["lumber"]) + "\nStones:" + str(
            self._res["stones"]) + "\nLabor" + str(self._res["labor"]) + "\nMagic:" + str(
            self._res["magic"]) + "\nTreasury:" + str(
            self._res["treasury"])

    def save_to_file(self):
        filename = self._name + ".txt"
        f = open(filename, "w")
        f.write(str(self._res["population"]) + "\n")
        f.write(str(self._res["lumber"]) + "\n")
        f.write(str(self._res["stones"]) + "\n")
        f.write(str(self._res["labor"]) + "\n")
        f.write(str(self._res["magic"]) + "\n")
        f.write(str(self._res["treasury"]) + "\n")
        f.write(str(self._res["lumber_growth"]) + "\n")
        f.write(str(self._res["stones_growth"]) + "\n")
        f.write(str(self._res["labor_growth"]) + "\n")
        f.write(str(self._res["magic_growth"]) + "\n")
        f.write(str(self._res["income"]) + "\n")
        f.write(str(self._res["upkeep"]) + "\n")
        f.write(str(self.get_channel()))

        f.close()
        pass

    def load_from_file(self):
        filename = self._name + ".txt"
        if os.path.isfile(filename):
            f = open(filename, "r")
            self._res["population"] = int(f.readline())
            self._res["lumber"] = int(f.readline())
            self._res["stones"] = int(f.readline())
            self._res["labor"] = int(f.readline())
            self._res["magic"] = int(f.readline())
            self._res["treasury"] = int(f.readline())
            self._res["lumber_growth"] = int(f.readline())
            self._res["stones_growth"] = int(f.readline())
            self._res["labor_growth"] = int(f.readline())
            self._res["magic_growth"] = int(f.readline())
            self._res["income"] = int(f.readline())
            self._res["upkeep"] = int(f.readline())
            self._channel = int(f.readline())
        else:
            self.save_to_file()
        pass


# I place my token in a key.txt file
def load_discord_token():
    with open("key.txt", "r") as f:
        return f.read().rstrip("\n")


def random_event(town):
    roll = random.randint(1, 6)
    with open('events.csv', 'r') as csv_file:
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


#event codes: pincrease(percentile increase), pdecrease(percentile decrease), increase and decrease, other. 


def upkeep_event(town_pass):
    res = town_pass.get_res()

    return_string = ""
    roll = random.randint(1, 101)
    if 0 < roll < 11:
        res["treasury"] = int(res["treasury"] - res["upkeep"])
        return_string = "No income, bad day. Upkeep cost still applies\n Income =" + str(-res["upkeep"])
    elif 10 < roll < 51:
        res["treasury"] = int(res["treasury"] - res["upkeep"] + res["income"])
        return_string = "standard day, profit =income-upkeep\n income =" + str(-res["upkeep"] + (res["income"]))
    elif 50 < roll < 61:
        res["treasury"] = int(res["treasury"] - res["upkeep"] + 1.25 * (res["income"]))
        return_string = "Good day, profit =(income-upkeep)*1.25 25% more profit\n Income =" + str(
            -res["upkeep"] + 1.25 * (res["income"]))
    elif 60 < roll < 81:
        res["treasury"] = int(res["treasury"] - res["upkeep"] + 1.5 * (res["income"]))
        return_string = "Good day, profit =(income-upkeep)*1.5 50% more profit\n Income =" + str(
            -res["upkeep"] + 1.5 * (res["income"]))
    elif 80 < roll < 91:
        res["treasury"] = int(res["treasury"] - res["upkeep"] + 1.75 * (res["income"]))
        return_string = "Good day, profit =(income-upkeep)*1.75 75% more profit\n Income =" + str(
            -res["upkeep"] + 1.75 * (res["income"]))
    elif 90 < roll < 101:
        res["treasury"] = int(res["treasury"] - res["upkeep"] + 2 * (res["income"]))
        return_string = "Good day, profit =(income-upkeep)*2 100% more profit\nIncome =" + str(
            -res["upkeep"] + 2 * (res["income"]))

    res["population"] += int(res["population"] * .1)  # assuming 10% growth per week, will adjust as needed
    res["lumber"] += int(res["lumber_growth"])
    res["stones"] += int(res["stones_growth"])
    res["labor"] += int(res["labor_growth"])
    res["magic"] += int(res["magic_growth"])

    town_pass.set_res(res)
    town_pass.save_to_file()
    return_string += "\n" + town_pass.resource_totals()

    town_pass.save_to_file()

    return return_string


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = str.split(str.lower(message.content))
    if len(msg) == 3:
        if msg[1] == "totals" and msg[2] == "please":
            for each in towns:
                if str.lower(each.get_name()) == msg[0]:
                    await message.channel.send(each.resource_totals())

    if message.content == "help":
        await message.channel.send("Commands: 'List towns', 'townname totals please', 'help''")
        pass
    if message.content == "list towns":
        return_string = ""
        for each in towns:
            return_string += each.get_name() + "\n"
            await message.channel.send(return_string)
        pass


async def events_rotation():
    await client.wait_until_ready()
    print("event rotation started")
    rotation = 0

    while client.is_closed:

        for town in towns:
            discord_channel = client.get_channel(town.get_channel())
            if rotation == 3:
                rotation = 0
                return_string = await sync_to_async(upkeep_event)(town)
                await discord_channel.send(return_string)
            else:
                return_string = await sync_to_async(random_event)(town)
                rotation += 1
                await discord_channel.send(return_string)
        print(rotation)
        await asyncio.sleep(10)
        # 3600 seconds in an hour just in case you didnt already know that
    print("?")
    pass


# load towns
towns = []
f = open("towns.txt", "r")
i = 0
for line in f:
    towns.append(Town(line.rstrip("\n")))
    i += 1
f.close()

for each in towns:
    each.load_from_file()
    print(each.get_name())

discord_token = load_discord_token()
token = os.getenv('DISCORD_TOKEN')

client.loop.create_task(events_rotation())
client.run(load_discord_token())
