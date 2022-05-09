import discord

async def give_role_safely(user, role):
	if role in user.roles:
		return
	
	await user.add_roles(role)
	
async def simple_embed(description: str):
	return discord.Embed(description = description, color = 0xff9126)
