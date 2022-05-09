from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.cog_ext import cog_slash
import discord

import constants

guild_ids = constants.GUILD_IDS

class NAMECog(discord.ext.commands.cog.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_call_author = None

    @cog_slash(
        name="", 
        description= "",

        options=[
            create_option( 
                name="",
                description="",
                option_type=3, 
                required=True)], 

        guild_ids=guild_ids)

    async def NAME(self, ctx):
        self.last_call_author = ctx.author.mention
        

def setup(bot):
    bot.add_cog(NAMECog(bot))