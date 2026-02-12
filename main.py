import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import datetime
import random
from config import TOKEN, STATUS_TEXT
from utils import parse_time

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.target_channel_id = None
        self.target_role = None

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Slash Commands Synced for {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    activity = discord.Game(name=STATUS_TEXT)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f'Logged in as {bot.user.name}')

# --- NICKNAME SYSTEM ---
@bot.tree.command(name="set-nick-channel", description="Set nickname auto channel")
async def set_nick_sys(interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
    bot.target_channel_id = channel.id
    bot.target_role = role.id
    
    embed = discord.Embed(
        title="📝 Nickname System",
        description=f"Ei channel-e naam likhle automatic nickname set hobe!\n\n✅ Role: {role.mention}\n🔄 Reset: `reset` likhun",
        color=0x00ffcc
    )
    embed.set_footer(text=f"System by HRIDOY HASAN")
    await channel.send(embed=embed)
    await interaction.response.send_message("✅ Setup Complete!", ephemeral=True)

@bot.event
async def on_message(message):
    if message.author.bot: return
    if bot.target_channel_id and message.channel.id == bot.target_channel_id:
        user = message.author
        role = message.guild.get_role(bot.target_role)
        try:
            if message.content.lower() == "reset":
                await user.edit(nick=None)
                if role in user.roles: await user.remove_roles(role)
                msg = await message.channel.send(f"✅ {user.mention} Nickname Reset!")
            else:
                await user.edit(nick=message.content)
                if role: await user.add_roles(role)
                msg = await message.channel.send(f"✅ {user.mention} Name set to **{message.content}**")
            
            await asyncio.sleep(2)
            await message.delete()
            await msg.delete()
        except: pass

# --- GIVEAWAY SYSTEM ---
@bot.tree.command(name="giveaway-create", description="Start a giveaway")
async def g_create(interaction: discord.Interaction, prize: str, time: str, winners: int):
    sec = parse_time(time)
    if sec is None: return await interaction.response.send_message("❌ Invalid Time!", ephemeral=True)

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=sec)
    embed = discord.Embed(
        title="🎁 GIVEAWAY START! 🎁",
        description=f"**Prize:** `{prize}`\n**Winners:** `{winners}`\n**Host:** {interaction.user.mention}",
        color=0xff0066, timestamp=end_time
    )
    await interaction.response.send_message("Giveaway Live!", ephemeral=True)
    msg = await interaction.channel.send(embed=embed)
    await msg.add_reaction("🎉")

    await asyncio.sleep(sec)
    new_msg = await interaction.channel.fetch_message(msg.id)
    users = [u async for u in new_msg.reactions[0].users() if not u.bot]
    
    if len(users) < winners:
        await interaction.channel.send(f"❌ Participant kom chilo prize: {prize}")
    else:
        winner_list = random.sample(users, min(len(users), winners))
        mentions = ", ".join([w.mention for w in winner_list])
        await interaction.channel.send(f"🎉 Congrats {mentions}! Won: **{prize}**")

# Bot Start
bot.run(TOKEN)
