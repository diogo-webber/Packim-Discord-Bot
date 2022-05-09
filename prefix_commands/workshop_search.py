import discord
import requests
from bs4 import BeautifulSoup
import time

from utils.utils import simple_embed

async def get_first_page_url(soup: BeautifulSoup) -> str:
	first_item = soup.find("div", class_ = "workshopBrowseItems").find("div")
	return first_item.find("a").get("href")


async def get_first_page_soup(soup: BeautifulSoup) -> BeautifulSoup:
	
	item_url = await get_first_page_url(soup)

	response = requests.get(item_url)
	return BeautifulSoup(response.text, 'lxml')


async def send_error_msg(ctx, target_msg, msg: str):
	await ctx.message.delete()
	await target_msg.edit(embed = await simple_embed(msg), delete_after=5)

def setup(bot):
	@bot.command(name="oficina")
	async def workshop_search(ctx, *, termo):
		time_start = time.time()

		embed = await simple_embed(f"Iniciando pesquisa pelo termo `{termo.capitalize()}`")
		inicial_response = await ctx.send(embed=embed)

		url = f"https://steamcommunity.com/workshop/browse/?appid=322330&searchtext={termo}&browsesort=trend&actualsort=trend&days=-1"
		
		response = requests.get(url)
		soup = BeautifulSoup(response.text, 'lxml')

		mod_page = await get_first_page_soup(soup)

		title = mod_page.find("div", class_="workshopItemTitle").get_text()
		description = mod_page.find("div", class_="workshopItemDescription").get_text(" ", strip=True)
		item_url = await get_first_page_url(soup)
		tumbnail_url = soup.find("img", class_="workshopItemPreviewImage").get("src")

		#tumbnail_url = mod_page.find("img", id="previewImageMain").get("src")

		embed = discord.Embed(
		title=f"**{title}**",
		description=f"ㅤ{description[:370]}...\nㅤ",
		url=item_url,
		color=0xff9126)
		
		embed.set_thumbnail(url=tumbnail_url)

		#embed.set_author(name=author_name, url=author_url, icon_url= author_icon)

		embed.set_footer(
			text=f'{ctx.author.display_name} pesquisou por: "{termo}"ㅤ|ㅤ{round((time.time() - time_start), 2)} segundos de execução.',
			icon_url=ctx.author.avatar_url
		)

		await ctx.message.delete()
		await inicial_response.edit(embed=embed)