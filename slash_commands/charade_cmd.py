from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option
import discord
import random

import utils.charades_utils as charades_utils
import constants
import utils.utils as utils
import utils.bank_utils as bank_utils

guild_ids = constants.GUILD_IDS

async def skip_charade(bot):
	await charades_utils.set_answered()

	target_channel = bot.get_channel(constants.CHANNEL_CHARADES)

	message = await charades_utils.get_charade_message(target_channel)
	if message:
		await message.delete()

class CharedesCog(discord.ext.commands.cog.Cog):
	def __init__(self, bot):
		self.bot = bot

	@cog_slash(
		name="rc", 
		description= '🍀 Um gnomo precisa de ajuda? Responda a charada!',
		guild_ids=guild_ids,
		options=[
			create_option(
				name="resposta",
				description='👀 Responda com ❔ para ir até a charada atual!',
				option_type=3, required=True)])

	async def rc(self, ctx, resposta: str):
		self.last_call_author = ctx.author.mention

		actual_answer = await charades_utils.get_answer()

		if actual_answer == 'reset':
			reply_to_user = await utils.simple_embed(f"Não há charada ativa no momento, {ctx.author.display_name}.")

		else:
			if resposta == '?':
				
				actual_charade = await charades_utils.get_actual_charade()
				message_id = actual_charade["id"]

				await ctx.send(embed=await utils.simple_embed(f"Clique **[aqui](https://discord.com/channels/790710877632462860/{constants.CHANNEL_CHARADES}/{message_id})** para ir para a última charada postada.") , delete_after = 60)
				reply_to_user = None

				#await send_log(f'**{ctx.author.display_name}** perguntou a charada atual.', client=client, ctx=ctx)
			
			elif resposta == 'admin':
				await skip_charade(self.bot)
				
				reply_to_user = await utils.simple_embed(f'Charada pulada com sucesso!')

			elif actual_answer.strip().replace(' ', '').lower() == resposta.strip().replace(' ', '').lower():

				await bank_utils.give_point(ctx)
				user_wallet = await bank_utils.get_user_wallet(ctx)

				reply_to_user = discord.Embed(title= '**Você acertou!** Parabéns!', description=f"✨ Sua pontução aumentou! Você possui {user_wallet} pontos!", color=0xff9126)

				reply_to_user.set_author(name='O Gnomo está contente!', icon_url="https://static.wikia.nocookie.net/dont-starve-game/images/b/b7/Gnomo.png/revision/latest/scale-to-width-down/64?cb=20151204063604&path-prefix=es")

				reply_to_user.set_thumbnail(url='https://cdn.discordapp.com/attachments/820710354874269726/874479372604690452/cabra_feliz.gif')

				await charades_utils.set_answered()

				description = f"{ctx.author.mention} acertou a **charada** e ganhou **1 ponto**!  <a:other_clap:861054501724487681>"

				embed = await utils.simple_embed(description)

				target_channel = (self.bot).get_channel(constants.CHANNEL_CHARADES)
				charade_message = await charades_utils.get_charade_message(target_channel)

				if charade_message:
					await charade_message.edit(embed=embed)

				await charades_utils.give_charade_roles(ctx, self.bot, charade_message, description)

			else:
				reply_to_user = None

				gifs = ["https://tenor.com/view/matrix-dodge-neo-errou-keanu-reeves-gif-16896074", "https://tenor.com/view/errou-errou-feio-errou-rude-no-talk-gif-17014486", "https://tenor.com/view/errou-raiva-vermelho-missed-angry-gif-14676554", "https://tenor.com/view/faustao-silva-fausto-churrasqueira-controle-gif-9324361", "https://tenor.com/view/tiago-cadore-galo-frito-comedy-show-errado-negativo-gif-13498265", "https://tenor.com/view/bernie-sanders-finger-wag-no-nope-bad-gif-5081015"]

				await ctx.send(content= random.choice(gifs), hidden= True)

		# Realmente enviando
		if reply_to_user:
			await ctx.send(embed=reply_to_user, hidden=True)



def setup(bot):
    bot.add_cog(CharedesCog(bot))