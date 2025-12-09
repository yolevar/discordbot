import discord
from discord.ext import commands
import asyncio

TOKEN = "DEIN_TOKEN_HIER"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Merkt sich nur die Channels, die der Bot selbst erstellt hat
created_channels = []
testing_active = False

@bot.event
async def on_ready():
    print(f"Bot eingeloggt als {bot.user}")

# -------------------------------
#        TESTNUKE BEFEHL
# -------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def testnuke(ctx, channels: int = 3, messages: int = 2):
    global testing_active
    if testing_active:
        return await ctx.send("⚠️ Es läuft bereits ein Test!")

    # Sicherheitsbegrenzung
    channels = min(channels, 5)
    messages = min(messages, 5)

    testing_active = True
    created_channels.clear()

    await ctx.send(f"💣 Starte sicheren Test:\n"
                   f"- Erstelle **{channels}** Channels\n"
                   f"- Sende **{messages}** Nachrichten pro Channel")

    for i in range(channels):
        if not testing_active:
            break

        # Channel erstellen
        channel = await ctx.guild.channels.create(name=f"test-channel-{i+1}")
        created_channels.append(channel.id)

        await asyncio.sleep(0.5)  # kleine Pause

        # Nachrichten senden
        for j in range(messages):
            if not testing_active:
                break
            await channel.send(f"Test Nachricht {j+1}")
            await asyncio.sleep(0.3)

    await ctx.send("✅ Test abgeschlossen.")
    testing_active = False


# -------------------------------
#              STOP
# -------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    global testing_active
    if not testing_active:
        return await ctx.send("❗ Kein Test läuft derzeit.")
    testing_active = False
    await ctx.send("🛑 Test wurde gestoppt.")


# -------------------------------
#           CLEANUP
# -------------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def clean(ctx):
    if not created_channels:
        return await ctx.send("ℹ️ Es gibt keine Test-Channels zum Löschen.")

    deleted = 0
    for channel_id in created_channels:
        channel = ctx.guild.get_channel(channel_id)
        if channel:
            await channel.delete(reason="Sicherer Test-Cleanup")
            deleted += 1

    created_channels.clear()

    await ctx.send(f"🗑️ **{deleted} Test-Channels gelöscht.**")


bot.run(MTQ0NjE3NTEzNTM0NTQxNDE4NA.G3N9tL.UnaOZeHKUALdWOSO8YPP_Ni-O_Jp8TPdR9P2Js)
