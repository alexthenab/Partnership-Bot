import discord
from discord.ext import commands
import random
import logging

# Logging setup
logging.basicConfig(filename='assignments.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Intents
intents = discord.Intents.default()
intents.members = True 
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")

@bot.command(name="partnershipassign")
async def partnershipassign(ctx, amount: int):
    guild = ctx.guild
    role_name = f"{amount} ping"

    # Check if role already exists
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        await ctx.send(f"Role `{role_name}` already exists.")
        return

    # Create the role
    try:
        new_role = await guild.create_role(name=role_name)
    except discord.Forbidden:
        await ctx.send("I don't have permission to create roles.")
        return

    # Fetch members (excluding bots)
    members = [member for member in guild.members if not member.bot]

    # Pick X random members
    if amount > len(members):
        await ctx.send(f"Only {len(members)} eligible members found. Assigning role to all of them.")
        amount = len(members)

    selected_members = random.sample(members, amount)

    # Assign the role
    for member in selected_members:
        try:
            await member.add_roles(new_role)
            logging.info(f"Assigned role '{role_name}' to {member.name}#{member.discriminator} ({member.id})")
        except discord.Forbidden:
            await ctx.send(f"Permission error while assigning role to {member.name}")
            continue

    await ctx.send(f"Created role `{role_name}` and assigned it to {amount} random users.")

# Replace YOUR_BOT_TOKEN with your bot's token
bot.run("YOUR_BOT_TOKEN")
