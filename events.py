
MESSAGE_ID = 825533017744998420

def setup(bot):
	@bot.event
	async def on_raw_reaction_add(paylord):
		
		guild = bot.get_guild(paylord.guild_id)
		message = await (guild.get_channel(816469390521401344)).fetch_message(MESSAGE_ID)
		divider_role_reaction_roles = guild.get_role(890693539514695680)
		
		if paylord.message_id == MESSAGE_ID and divider_role_reaction_roles not in paylord.member.roles:

			for reaction in message.reactions:
				users = await reaction.users().flatten()
				if paylord.member in users:
					await paylord.member.add_roles(divider_role_reaction_roles)
					print(f'\n {paylord.member.display_name} rebeceu o divisor "REAÇÕES"')
					return
				