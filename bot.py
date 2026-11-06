import os
import discord
from discord.ext import commands
from tuya_connector import TuyaOpenAPI

TUYA_CLIENT_ID = os.getenv("TUYA_CLIENT_ID", "xc933ngu7ncxmpg9ka9x")
TUYA_SECRET = os.getenv("TUYA_SECRET", "")
ID_BARDI = os.getenv("ID_BARDI", "a305cd32bdb0a988b2iiw6")
ID_ITSMART = os.getenv("ID_ITSMART", "a300dc97aa5533b282l0qq")

# Singapore Data Center - 【entity-Bardi¦canonical_name=BARDI】-bot-SIN
openapi = TuyaOpenAPI(endpoint="https://openapi.tuyasg.com", access_id=TUYA_CLIENT_ID, access_key=TUYA_SECRET)
openapi.connect()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

SWITCHES = {
    "dapur": (ID_BARDI, "switch_1"),
    "dorong": (ID_BARDI, "switch_2"),
    "hisap": (ID_BARDI, "switch_3"),
    "beranda": (ID_ITSMART, "switch_1"),
    "ruang": (ID_ITSMART, "switch_2"),
}

def set_switch(device_id, code, on: bool):
    return openapi.post(f"/v1.0/iot-03/devices/{device_id}/commands", {"commands": [{"code": code, "value": on}]})

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

@bot.command(name="nyala")
async def nyala(ctx, nama: str = ""):
    nama = nama.lower()
    if nama not in SWITCHES:
        await ctx.send("Coba: dapur, dorong, hisap, beranda, ruang")
        return
    did, code = SWITCHES[nama]
    set_switch(did, code, True)
    await ctx.send(f"✅ {nama.capitalize()} NYALA!")

@bot.command(name="mati")
async def mati(ctx, nama: str = ""):
    nama = nama.lower()
    if nama not in SWITCHES:
        await ctx.send("Coba: dapur, dorong, hisap, beranda, ruang")
        return
    did, code = SWITCHES[nama]
    set_switch(did, code, False)
    await ctx.send(f"💤 {nama.capitalize()} MATI!")

@bot.command(name="list")
async def list_sw(ctx):
    await ctx.send("💡 !nyala dapur / dorong / hisap / beranda / ruang")

bot.run(os.getenv("DISCORD_TOKEN"))
