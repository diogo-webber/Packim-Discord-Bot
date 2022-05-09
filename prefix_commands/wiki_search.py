import discord
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import time

from utils.utils import simple_embed

async def get_meta_tag(soup, property: str):
	meta_tag = None

	if soup.find("meta", property="og:" + property):
		meta_tag = soup.find("meta", property="og:" + property)

	elif soup.find("meta", property=property):
		meta_tag = soup.find("meta", property=property)

	elif soup.find("meta", property="twitter:" + property):
		meta_tag = soup.find("meta", property="twitter:" + property)

	elif soup.find("div", class_="mw-parser-output").p and len(soup.find("div", class_="mw-parser-output").p) > 75:
		return soup.find("div", class_="mw-parser-output").p.get_text()

	elif soup.find("meta", attrs={"name":"twitter:"+ property}):
		meta_tag = soup.find("meta", attrs={"name":"twitter:"+ property})
	
	if meta_tag:
		return meta_tag.get("content")

async def get_prefabs_in(code_tag_list: list):

	if not code_tag_list:
		return

	prefabs = []
	for code_tag in code_tag_list:
		code_tag_splited_list = code_tag.get_text().split('"')

		for item in code_tag_splited_list:
			if item != "" \
			and " " not in item \
			and item.lower() == item:
				prefabs.append(item)
	
	return prefabs
		
async def get_code_tags(soup):
	unique_code_tags_list = None

	code_tags_list = []
	aside_tags = soup.find_all("aside")
	for aside_tag in aside_tags:
		code_tags_list.extend(aside_tag.find_all("code"))

	unique_code_tags_list = list(dict.fromkeys(code_tags_list))

	if unique_code_tags_list:
		return unique_code_tags_list


async def insert_prefab_fields(soup, embed):
	unique_code_tags = await get_code_tags(soup)
	prefabs = await get_prefabs_in(unique_code_tags)
	
	if not prefabs:
		return

	if len(prefabs) > 1:
		for index, prefab in enumerate(prefabs, 1):
			if index % 2 == 0:
				embed.add_field(name="ㅤ", value="ㅤ", inline=True)

			if index == len(prefabs):
				embed.add_field(name=f"Prefab {index}", value=f'"{prefab}"\nㅤ', inline=True)
				continue
			
			embed.add_field(name=f"Prefab {index}", value=f'"{prefab}"', inline=True)

	else:
		embed.add_field(name=f"Prefab", value=f'"{prefabs[0]}"\nㅤ', inline=True)


async def get_thumbnail_url(soup, title):
	tumbnail_url = "invalid"

	if soup.find("img", class_="pi-image-thumbnail"):
		tumbnail_url = soup.find("img", class_="pi-image-thumbnail").get("src")

	elif soup.find("img", alt= title + ".png"):
		tumbnail_url = soup.find("img", alt= title + ".png").get("src")

	elif soup.find("img", class_="thumbimage"):
		img_tag = soup.find("img", class_="thumbimage")

		if "src=" in str(img_tag):
			thumbnail_url = img_tag.get("src")

			if thumbnail_url.startswith("https"):
				return thumbnail_url

		if "data-src=" in str(img_tag):
			thumbnail_url = img_tag.get("data-src")

			if thumbnail_url.startswith("https"):
				return thumbnail_url
	
	
	return tumbnail_url

async def send_error_msg(ctx, target_msg, msg: str):
	await ctx.message.delete()
	await target_msg.edit(embed = await simple_embed(msg), delete_after=5)

def setup(bot):
	@bot.command(name="wiki")
	async def wiki_search(ctx, *, termo):
		time_start = time.time()

		embed = await simple_embed(f"Iniciando pesquisa pelo termo `{termo.capitalize()}`")
		inicial_response = await ctx.send(embed=embed)

		google_results = search("Don't Starve Wiki" + termo, num_results=1)
		first_result = next(google_results)
		
		is_correct_page = first_result.startswith("https://dontstarve.fandom.com") \
		and first_result != "https://dontstarve.fandom.com/wiki/Don%27t_Starve_Wiki"
		
		if not is_correct_page:
			await send_error_msg(ctx, inicial_response, f"Nenhuma página encontrada!")
			return

		embed = await simple_embed(f"Página encontrada! Coletando **informações**...")
		await inicial_response.edit(embed=embed)

		page = requests.get(first_result)
		soup = BeautifulSoup(page.text, 'lxml')

		title = await get_meta_tag(soup, "title")
		description = await get_meta_tag(soup, "description")

		if not title or not description:
			await send_error_msg(ctx, inicial_response, f"**Não foi possível concluir a busca!**\n O site consultado foi: `{first_result}`")
			return

		embed = discord.Embed(
		title=f"**{title}**",
		url=first_result,
		description=f"ㅤ{description}...\nㅤ", 
		color=0xff9126)

		await insert_prefab_fields(soup, embed)

		tumbnail_url = await get_thumbnail_url(soup, title)

		if tumbnail_url and tumbnail_url.startswith("https"):
			embed.set_thumbnail(url=tumbnail_url)

		embed.set_footer(
			text=f'{ctx.author.display_name} pesquisou por: "{termo}"ㅤ|ㅤ{round((time.time() - time_start), 2)} segundos de execução.',
			icon_url=ctx.author.avatar_url
		)

		await ctx.message.delete()
		await inicial_response.edit(embed=embed)
