import requests
from discord.ext.tasks import loop
import discord
import constants

API_URL = "https://api.thecatapi.com/v1/images/search"

headers = {
	'x-api-key': "c0f0f0d3-9e21-4a3b-b0a6-97f98fc600cc"
}

def setup(bot):

	@loop(hours=24)
	async def daily_cat_picture():

		response = requests.get(url=API_URL, headers=headers)
		picture_url = response.json()[0]["url"]
		
		channel = bot.get_channel(id=constants.CHAT_GERAL_ID)
		
		embed = discord.Embed(
			title = "Foto de Gatinho Diária!",
			color = 0xff9126
		)

		embed.set_image(url=picture_url)

		await channel.send(embed=embed)

	@daily_cat_picture.before_loop
	async def loop_charade_before():
		await bot.wait_until_ready()

	daily_cat_picture.start()