"""
Handles interactions with the discordbots.org API
"""

from asyncio import sleep
from os import environ
import aiohttp
import utils

try:
    dblToken = environ["dblToken"]
except KeyError:
    utils.err("Environment Variable \"dblToken\" cannot be found")

dblAPI = "https://discordbots.org/api/bots/{}/stats"
dblHeaders = {"Authorization": dblToken, "Content-Type": "application/json"}

async def dblPostServerCount(count):
    async with aiohttp.ClientSession() as session:
        try:
            await session.post(
                dblUpdateURL,
                json={"server_count": count},
                headers=dblHeaders
            )
        except Exception as e:
            print("[dblPostServerCount] Failed to post server count\n{}: {}".format(type(e).__name__, e))

async def dblBackgroundTask(client, sleepMinutes):
    await client.wait_until_ready()
    dblUpdateURL = dblAPI.format(client.user.id)
    while not client.is_closed:
        await dblPostServerCount(len(list(client.servers)))
        await sleep(60 * sleepMinutes)