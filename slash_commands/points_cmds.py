from discord_slash.utils.manage_commands import create_option
from discord_slash.cog_ext import cog_slash
import discord
from operator import itemgetter

from PIL import Image
from io import BytesIO
import requests


import utils.bank_utils as bank_utils
import utils.utils as utils
import constants

guild_ids = constants.GUILD_IDS

class UtilsCharadesCog(discord.ext.commands.cog.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.last_call_author = None

	@cog_slash(
		name="Pontuação", 
		description= "🔎 Verifique sua pontuação ou a de outro player!", 
		options=[
			create_option(
				name="member",
				description="Qual usuário deseja verificar?",
				option_type=6, required=False
			)
		], 
		guild_ids=guild_ids
	)

	async def points(self, ctx, member=None):
		self.last_call_author = ctx.author.mention

		if not member:
			member = ctx.author

		await bank_utils.open_account(member)
		users = await bank_utils.get_bank_data()

		wallet_amt = users[str(member.id)]["wallet"]
		user_name = member.display_name

		if wallet_amt == 0:
			em = await utils.simple_embed(f"**{user_name}** não possui pontuação!")
		else:
			points = 'ponto' if wallet_amt == 1 else 'pontos'
			em = discord.Embed(title= f"Pontuação de **{user_name}**", color=0xff9126)
			em.add_field(name= 'Pontuação:', value = f'{wallet_amt} {points}')

		await ctx.send(embed=em, hidden=True)

	@cog_slash(
		name="leaderboard", 
		description= "⭐️ Veja os membros que mais pontuaram nas charadas!",
		guild_ids=guild_ids, 
		options=[
			create_option(
				name="tamanho",
				description="Quantos posições deseja ver? O padrão são 10 posições.",
				option_type=4,
				required=False
			)
		]
	)

	async def leaderboard(self, ctx, tamanho=10):
		self.last_call_author = ctx.author.mention

		size = tamanho

		users = await bank_utils.get_bank_data()
		leader_board = {}
		
		for user in users:
			id_ = int(user)
			total_amount = users[user]["wallet"]
			leader_board[id_] = total_amount


		list_infos = sorted(leader_board.items(), key=itemgetter(1), reverse=True)

		size_list_infos = len(list_infos)
		size_leaderboard = size if size < size_list_infos else size_list_infos

		description = "```Estes são os membros mais ativos e sábios do servidor!```"

		guild = (self.bot).get_guild(constants.GUILD_ID)

		for index, (id, amt) in enumerate(list_infos, 1):
			if amt != 0:
				try:
					member = guild.get_member(id)
					member = member.mention
				except:
					member = users[str(id)]["name"] + " _[Saiu do servidor]_ "
					

				points = 'ponto' if amt == 1 else 'pontos'
				description += f"\n**{index}.** {member} ➜ {amt} {points}\n"

				if index == size_leaderboard:
					break


		em = discord.Embed(title = f"ㅤㅤTop {size_leaderboard} líderes de pontuação!" , description = description, color = 0xff9126)

		await ctx.send(embed = em, hidden=True)	

def setup(bot):
    bot.add_cog(UtilsCharadesCog(bot))