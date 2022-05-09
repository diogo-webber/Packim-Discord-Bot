from discord.ext.tasks import loop
import discord
from replit import db
import random
import asyncio
from typing import Union

import utils.charades_utils as charades_utils
import utils.utils as utils
import constants

async def create_answer_tip(answer: Union[str, int]):
	tip = ''
		
	for letter in answer:
		if letter.isnumeric():
			tip += '_ '
		elif letter == letter.upper():
			tip += f'{letter} '
		else:
			tip += '_ '

	return tip

async def get_answer_type_text(answer: Union[str, int]):
	if answer.isnumeric():
		return "ㅤㅤㅤ**Valor númerico!**"
	
	return "ㅤㅤㅤ**Em inglês!**"

async def set_author_footer_and_tumbnail(embed: discord.Embed):
	embed.set_author(
		name='Um gnomo apareceu!', 
		icon_url="https://static.wikia.nocookie.net/dont-starve-game/images/b/b7/Gnomo.png/revision/latest/scale-to-width-down/64?cb=20151204063604&path-prefix=es"
	)
		
	embed.set_footer(
		text="Use /rc para responder!", 
		icon_url='https://cdn.discordapp.com/attachments/820710354874269726/874468665507082300/aa.png'
	)
	
	thumbnails = [
		"https://cdn.discordapp.com/attachments/908190016944087081/908190090059186186/wagstaff_thinking.gif", "https://cdn.discordapp.com/attachments/908190016944087081/908190094614204476/wilba_thinking.gif", "https://cdn.discordapp.com/attachments/908190016944087081/908190101098602526/wheeler_thinking.gif", "https://cdn.discordapp.com/attachments/908190016944087081/908190108371525682/wilbur_thinking.gif", "https://cdn.discordapp.com/attachments/908190016944087081/908190109654982706/woodlegs_thinking.gif"
	]

	embed.set_thumbnail(url= random.choice(thumbnails))


def setup(bot):

	@loop(seconds=30)
	async def charade_loop():
		channel = bot.get_channel(id=constants.CHANNEL_CHARADES)

		answered = await charades_utils.is_answered()
		if not answered: 
			return
		
		timer = random.randint(270,1200)
		print(f'\n - Proxima charada em {timer//60} minutos!')	
		await asyncio.sleep(timer)
		
		question, answer = await charades_utils.generate_new_charade()

		tip = await create_answer_tip(answer)
		answer_type_text = await get_answer_type_text(answer)
					
		embed_description = \
		f"**CHARADA:**  {question}\n\n" \
		f"**DICA:**ㅤ` {tip}`{answer_type_text}"

		embed = await utils.simple_embed(embed_description)

		await set_author_footer_and_tumbnail(embed)

		message_sent = await channel.send(embed=embed)

		db["actual-charade"]["id"] = int(message_sent.id)

		print(f"\nCharada enviada!\n")

	@charade_loop.before_loop
	async def loop_charade_before():
		await bot.wait_until_ready()

	charade_loop.start()