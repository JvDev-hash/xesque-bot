import discord
import os
import asyncio
from dotenv import load_dotenv
from ai import process_ndjson_stream

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")
    
@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"Pong! Latency is {bot.latency}")
    
@bot.command(description="Interacts with the AI")
async def llm(ctx: discord.ApplicationContext, prompt: discord.Option(discord.SlashCommandOptionType.string)):
    await ctx.defer(ephemeral = False)
    resposta = process_ndjson_stream("http://localhost:11434/api/generate", prompt)
    await ctx.respond(resposta)

bot.run(os.getenv('TOKEN')) # run the bot with the token