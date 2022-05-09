from discord_slash.cog_ext import cog_slash
import discord
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_permission

import utils.utils as utils
import constants

guild_ids = constants.GUILD_IDS

class OthersCog(discord.ext.commands.cog.Cog):
	def __init__(self, bot):
		self.bot = bot

	@cog_slash(
	name="Convite", 
	description= "🥰 Convite jogadores para participar do servidor!",
	guild_ids=guild_ids)

	async def discord_invite(self, ctx):
		self.last_call_author = ctx.author.mention
		embed = await utils.simple_embed("```https://discord.gg/QTe87kcceu```")

		await ctx.send(embed=embed, hidden=True)

	@cog_slash(
	name="Aviso", 
	description= "📢 Comando para postar avisos, disponível para administradores.",
	permissions = create_permission(
		constants.PIG_KING_ROLE_ID, 
		SlashCommandPermissionType.ROLE, True
	), 

	options=[
		create_option(
			name="linha_1",
			description="O que deve estar escrito na linha 1?",
			option_type=3, 
			required=True), 

		create_option(
			name="linha_2",
			description="O que deve estar escrito na linha 2?",
			option_type=3, 
			required=False),

		create_option(
			name="linha_3",
			description="O que deve estar escrito na linha 3?",
			option_type=3, 	required=False
		)
	], 

	guild_ids=guild_ids)

	async def aviso(self, ctx, linha_1: str, linha_2 = None, linha_3 = None):
		self.last_call_author = ctx.author.mention
		channel_aviso = (self.bot).get_channel(839924430267220039)
	
		description_aviso = f"ㅤ\n<:e_setazul:865233380038803496>   {linha_1}\nㅤ"

		if linha_2 != None:
			description_aviso += f"\n <:e_setazul:865233380038803496>   {linha_2}\nㅤ"
		
			if linha_3 != None:
				description_aviso += f"\n <:e_setazul:865233380038803496>   {linha_3}\nㅤ"


		aviso = discord.Embed(
			title = " <:Server_Updated:853120289050591242>ㅤNOVIDADES:",
			description = description_aviso,
			color=0x36B12B)
		
		aviso.set_footer(
			text = "Leonidas IVㅤ |ㅤConfirme sua visualização com a reação!",
			icon_url = 'https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/72/728d9c6aac06ad87ebe12b9fd8d1253267a0dbd8_full.jpg')


		await channel_aviso.send('<@&839948580503552062>' , embed = aviso)

		em = await utils.simple_embed(f"Mensagem enviada ao canal {channel_aviso.mention}")
		
		await ctx.send(embed=em, hidden=True)

def setup(bot):
    bot.add_cog(OthersCog(bot))