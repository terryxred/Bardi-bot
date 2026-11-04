import os
from discord.ext import commands
import discord
from tuya_connector import TuyaOpenAPI

TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("TUYA_CLIENT_ID")
SECRET = os.getenv("TUYA_SECRET")

ID_TERAS = os.getenv("ID_TERAS")
ID_DAPUR = os.getenv("ID_DAPUR")
ID_KAMAR = os.getenv("ID_KAMAR")

api = TuyaOpenAPI("https://openapi.tuyaeu.com", CLIENT_ID, SECRET)
api.connect()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def nyalakan(id_dev, on):
    if not id_dev:
        return
    try:
        c = {'commands': [{'code': 'switch_1', 'value': on}]}
        api.post(f'/v1.0/iot-03/devices/{id_dev}/commands', c)
    except Exception as e:
        print(e)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} ONLINE')

@bot.command(name="nyala")
async def nyala_cmd(ctx, nama: str):
    m = {"teras": ID_TERAS, "dapur": ID_DAPUR, "kamar": ID_KAMAR}
    nyalakan(m.get(nama.lower()), True)
    await ctx.send(f"✅ {nama} NYALA")

@bot.command(name="mati")
async def mati_cmd(ctx, nama: str):
    m = {"teras": ID_TERAS, "dapur": ID_DAPUR, "kamar": ID_KAMAR}
    nyalakan(m.get(nama.lower()), False)
    await ctx.send(f"💤 {nama} MATI")

bot.run(TOKEN)
