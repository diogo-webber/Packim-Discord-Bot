from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.cog_ext import cog_slash
import discord

import constants

guild_ids = constants.GUILD_IDS

class ConsoleCog(discord.ext.commands.cog.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_slash(
        name="Console", 
        description= "🌲 Comandos úteis para o DST!", 

        options=[
            create_option( 
                name="comando",
                description="Qual comando dejesa solicitar?",
                choices=[
                    create_choice(
                        name="🌵 Grupos de Cabra",
                        value="Grupos de Cabra"),

                    create_choice(
                        name="🍂 Spawns do Klaus",
                        value="Spawns do Klaus"),

                    create_choice(
                        name="🌱 Seed do mapa",
                        value="Seed do mapa"),

                    create_choice(
                        name="O orb já caiu?",
                        value="O orb já caiu?"),

                        ],

                option_type=3, 
                required=True)], 


        guild_ids=guild_ids)

    async def console(self, ctx, comando):
        self.last_call_author = ctx.author.mention
        
        async def embed_console_command(codigo):
            await ctx.send(embed=discord.Embed(
                title= f"<:level:875108907159269377> Comando  -  {comando}",
                description=codigo, 
                color=0xff9126), 
                hidden=True)

        if comando == "Grupos de Cabra":
            await embed_console_command('```lua\nc_announce(Grupos de cabra: ".. c_countprefabs("lightninggoatherd"))```')

        elif comando == "Spawns do Klaus":
            await embed_console_command('```lua\nc_announce("Spawns de Loot Stash: ".. c_countprefabs("deerspawningground"))```')


        elif comando == "Seed do mapa":
            await embed_console_command('```lua\nc_announce("Seed: ".. TheWorld.meta.seed)```')

        else:
            await ctx.send(content="MIAU")


def setup(bot):
    bot.add_cog(ConsoleCog(bot))