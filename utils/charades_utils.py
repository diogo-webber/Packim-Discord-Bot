import random
import discord
from replit import db

import utils.bank_utils as bank_utils
import utils.utils as utils
import constants

async def get_info():
  return db["info"]

async def get_actual_charade():
   return db["actual-charade"]

async def get_charade_message(channel):
	actual_charade = await get_actual_charade()
	message_id = actual_charade["id"]
	try:
		message = await channel.fetch_message(message_id)
		return message
	except:
		return False
		
async def get_answer():
	actual_charade = await get_actual_charade()
	return actual_charade["answer"]

async def get_charade_bank():
	return db["charade-bank"]


async def is_answered():
	answer = await get_answer()
	if answer == "reset":
		return True

	return False
	
async def set_answered():
	db["actual-charade"]["answer"] = "reset"
    

async def get_max_number_charades():
	return await get_info()["total"]


async def change_order():
	charades = await get_charade_bank()

	options = list(range(1, len(charades)))

	random_list = []

	while options != []:
		random_n = random.choice(options)

		random_list.append(int(random_n))
		options.remove(random_n)

	db["info"]["random-list"] = random_list
	db["info"]["actual-charade"] = 0

	print("A ORDEM DAS CHARADAS MUDOU")

    
async def generate_new_charade():
    
    info = await get_info()

    random_list = info["random-list"]

    if info["actual-charade"] >= len(random_list):
        await change_order()

    info = await get_info() # Pega as novas infos pós mudar a ordem

    i = info["actual-charade"]

    selected_charade_index = random_list[i]

    charade_bank = await get_charade_bank()

    question = charade_bank[str(selected_charade_index)]["p"]
    answer = charade_bank[str(selected_charade_index)]["r"]

    db["actual-charade"]["question"] = question
    db["actual-charade"]["answer"] = answer

    db["info"]["actual-charade"] += 1

    return question, answer


async def give_rewards(ctx, message, number, role, description):
	await utils.give_role_safely(ctx.author, role)
	embed = discord.Embed(
		description = description, 
		color=0xff9126)

	embed.add_field(name="Conquista:", value= f"**{ctx.author.display_name}** chegou a {number} pontos e recebeu a role **{role.mention}**")

	await message.edit(embed = embed)


async def give_charade_roles(ctx, bot, message, description): 

	guild = bot.get_guild(constants.GUILD_ID)
	#log_channel = bot.get_channel(837530478907097140)

	role_20_points = guild.get_role(constants.ROLES_IDS["TWENTY_POINTS"])
	role_50_points = guild.get_role(constants.ROLES_IDS["FIFTY_POINTS"])
	role_100_points = guild.get_role(constants.ROLES_IDS["HUNDRED_POINTS"])
	role_divider = guild.get_role(constants.ROLES_IDS["CHARADES_DIVIDER"])

	users = await bank_utils.get_bank_data()
	user_wallet =  users[str(ctx.author.id)]["wallet"]

	if user_wallet == 20:
		await give_rewards(ctx, message, 20, role_20_points, description)
		await utils.give_role_safely(ctx.author, role_divider)

	elif user_wallet == 50:
		await give_rewards(ctx, message, 50, role_50_points, description)

	elif user_wallet == 100:
		await give_rewards(ctx, message, 100, role_100_points, description)
