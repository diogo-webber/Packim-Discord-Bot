from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_option, create_choice, create_permission
import discord
from replit import db
from datetime import datetime

import constants
from utils.utils import simple_embed

guild_ids = constants.GUILD_IDS

async def make_msg(codigo: str):
   return f"\n\n<:level:875108907159269377>   **[link/{codigo}](https://accounts.klei.com/link/{codigo})**"

class SpoolsCog(discord.ext.commands.cog.Cog, name="spools_cog"):
	def __init__(self, bot):
		self.bot = bot
		self.last_call_author = None

	@cog_slash(
		name="Spools", 
		description= "🧶 Links para resgate de Klei Points e Spools.",
		guild_ids=guild_ids
	)

	async def spools(self, ctx):
		self.last_call_author = ctx.author.mention

		embed = discord.Embed(
			title = 'ㅤㅤㅤㅤㅤKLEI POINTSㅤ&ㅤSPOOLS!',
			description = '```\nEstes são os links de recompensa disponíveis!```', 
			color = 0xff9126
		)

		codigos = db["klei-codes"]

		msg_spools = ""
		msg_points = ""

		for codigo in codigos["spools"]:
			msg_spools += await make_msg(codigo)

		for codigo in codigos["points"]:
			msg_points += await make_msg(codigo)


		embed.add_field(
			name="ㅤ", 
			value=f"ㅤㅤ<:spools:875095328687288360> **SPOOLS**{msg_spools}\n\nㅤ", 
			inline=True
		)

		embed.add_field(
			name="ㅤ", 
			value='ㅤ'
		)

		embed.add_field(
			name="ㅤ", 
			value=f" ㅤㅤ<:klei_points:875095453920800789>  **POINTS** {msg_points}\n\nㅤ", 
			inline=True
		)

		embed.set_thumbnail(
			url="https://media.discordapp.net/attachments/820710354874269726/875103169695322142/spools.png"
		)

		timestamp = db["klei-codes"]["last-update"]

		embed.set_footer(
			text=f"Última atualização: {timestamp}", 
			icon_url="https://cdn-icons-png.flaticon.com/512/724/724897.png"
		)
		
		await ctx.send(embed=embed)

#----------------------------------------------------------------------
		
	@cog_slash(
		name= "adicionar-codigo-klei", 
		description= "🧶 Adicionar Klei Points ou Spools.",
		guild_ids=guild_ids,
		permissions = create_permission(
			constants.PIG_KING_ROLE_ID, 
			SlashCommandPermissionType.ROLE, True
		),

		options=[
			create_option(
				name="type",
				description="Klei Points ou Spools?",
				choices= [
					create_choice(
						name="Klei Points",
						value="points"
					),

					create_choice(
						name="Spools",
						value="spools"
					),
				],
				
				option_type=3, 
				required=True
			),

			create_option(
				name="name",
				description="Nome do link, só o último código!",
				option_type=3, 
				required=True,
			),
		],
	)

	async def add_code(self, ctx, type, name):
		self.last_call_author = ctx.author.mention

		db["klei-codes"][type].append(name)
		
		db["klei-codes"]["last-update"] = str(datetime.now().strftime('%d/%m/%Y'))

		await ctx.send(embed= await simple_embed(f"Código **{name}** adicionado para **{type}** com sucesso!"), hidden=True)

#--------------------------------------------------------------------------------------------
	list_codes = []

	klei_codes = db["klei-codes"]

	for key in klei_codes["spools"]:
		list_codes.append(key)

	for key in klei_codes["points"]:
		list_codes.append(key)
		
	@cog_slash(
		name= "remover-codigo-klei", 
		description= "🧶 Remover Klei Points ou Spools.",
		guild_ids=guild_ids,
		permissions = create_permission(
			constants.PIG_KING_ROLE_ID, 
			SlashCommandPermissionType.ROLE, True
		),

		options=[
			create_option(
				name="name",
				description="Qual código deseja remover?",
				option_type=3, 
				required=True,
				choices = [create_choice(name=name, value=name) for name in list_codes]
			),
		],
	)

	async def remove_code(self, ctx, name):
		self.last_call_author = ctx.author.mention

		try:
			db["klei-codes"]["points"].remove(name)
			type_ = "points"
		except:
			db["klei-codes"]["spools"].remove(name)
			type_ = "spools"

		db["klei-codes"]["last-update"] = str(datetime.now().strftime('%d/%m/%Y'))

		await ctx.send(embed= await simple_embed(f"Código **{name}** removido de **{type_}** com sucesso!"), hidden=True)
		
		
def setup(bot):
    bot.add_cog(SpoolsCog(bot))