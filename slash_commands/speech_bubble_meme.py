from discord_slash.utils.manage_commands import create_option
from discord_slash.cog_ext import cog_slash, cog_context_menu

from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType

import discord

from PIL import Image
from io import BytesIO
import requests

import constants
from utils.utils import simple_embed


guild_ids = constants.GUILD_IDS

async def bubbling(self, ctx, image_url):
	self.last_call_author = ctx.author.mention
	
	bubble_image = Image.open("slash_commands/bubbling_assets/bubble.png")

	try:
		image_data = BytesIO(requests.get(image_url).content)
		input_image = Image.open(image_data)
		
		width, height = bubble_image.size

		new_width  = input_image.size[0]
		new_height = int(new_width * height / width)
		
		bubble_image = bubble_image.resize((new_width,new_height), Image.ANTIALIAS)
		
		input_image.paste(bubble_image, (0,0), bubble_image)
		
		input_image.save("slash_commands/bubbling_assets/quote.gif")
		
		await ctx.send(file = discord.File("slash_commands/bubbling_assets/quote.gif"))

	except requests.exceptions.MissingSchema:
		await ctx.send(embed=await simple_embed("A mensagem não possui uma imagem!"), hidden=True)
		
	except Exception as e:
		await ctx.send(
			embed = discord.Embed
			(
				title = "**ERROR: **",
				description = f"{str(e).capitalize()}", 
				color = 0xff9126
			)
		)

class SpeechBubblingCog(discord.ext.commands.cog.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.last_call_author = None

	@cog_slash(
		name="balão", 
		description= "Cria um gif do meme Speech Bubbling com a imagem enviada.",
		
		options=[
			create_option( 
				name="image_url",
				description="URL da imagem a ser editada",
				option_type=3, 
				required=True
			)
		], 
		
		guild_ids= [390561492686077983, 981709317872971866, 844681140744617984]
	)
	async def bubbling_slash(self, ctx, image_url):
		await bubbling(self, ctx, image_url)
			
	@cog_context_menu(
		target=ContextMenuType.MESSAGE,
		name="Criar-balão",
		guild_ids=[790710877632462860, 390561492686077983]
	)
	
	async def bubbling_menu(self, ctx: MenuContext):
		if ctx.target_message.attachments:
			if ctx.target_message.attachments[0].content_type in ("image/jpeg", "image/png"):
				await bubbling(self, ctx, ctx.target_message.attachments[0].url)
				return
				
			await ctx.send(embed=await simple_embed("A mensagem não possui uma imagem!"), hidden=True)
			return

		await bubbling(self, ctx, ctx.target_message.content)
		
def setup(bot):
	bot.add_cog(SpeechBubblingCog(bot))