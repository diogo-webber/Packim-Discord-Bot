import discord
from discord_slash import SlashCommand
from discord.ext import commands
import os

import constants
from utils.keep_alive import keep_alive
import utils.utils as utils

#--------------------------------------------------------------------------------------

bot = commands.Bot(command_prefix = "!", intents = discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

#--------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------

@bot.event
async def on_ready():
	os.system("clear")
	print('\n ' + 8*"-" +'  BOT OPERACIONAL  ' + 7*'-')
	
	#await remove_all_commands(bot_id=865579294368858182, guild_ids=[844681140744617984, constants.GUILD_ID], bot_token=os.environ['TOKEN']) # Packims 1


# kill 1 in shell for change IP adress
	
@bot.event
async def on_slash_command(ctx):
		
	if ctx.cog.last_call_author and not ctx.cog.last_call_author == "<@361300567471161354>":

		channel_log = bot.get_channel(constants.LOG_CHANNEL_ID)
		
		msg = f"{ctx.cog.last_call_author} usou o comando `{ctx.name}`"
		len_arg = len(ctx.args)
		
		if len_arg > 0:
			if len_arg == 1:
				msg += f" com o parametro: `{ctx.args[0]}`"
			else:
				msg += f" com os parametros: "
				for arg in ctx.args:
					msg += f"`{arg}` "
		
		await channel_log.send(embed=await utils.simple_embed(msg))

	if ctx.cog.qualified_name == "spools_cog" and ctx.name != "spools":
		bot.reload_extension("slash_commands.codes_cmd")


#--------------------------------------------------------------------------------------
"""
@bot.event
async def on_slash_command_error(ctx, ex):
	channel_log = bot.get_channel(LOG_CHANNEL_ID)

	await channel_log.send(
		embed = discord.Embed(
		title = "**ERROR: **",
		description = f"{ex}", 
		color = 0xff9126
		)
	)
"""
#--------------------------------------------------------------------------------------

bot.load_extension("slash_commands.charade_cmd")
bot.load_extension("slash_commands.codes_cmd")
bot.load_extension("slash_commands.console_cmds_cmd")
bot.load_extension("slash_commands.points_cmds")
bot.load_extension("slash_commands.others_cmds")
bot.load_extension("tasks.send_charade")
bot.load_extension("tasks.bot_status")
#bot.load_extension("tasks.cat_picture")
bot.load_extension("prefix_commands.wiki_search")
bot.load_extension("prefix_commands.workshop_search")
bot.load_extension("events")

keep_alive()
bot.run(os.environ['BOT_TOKEN'])