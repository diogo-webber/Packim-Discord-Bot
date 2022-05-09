from replit import db

async def open_account(user):
	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		db["bank"][str(user.id)] = {}
		db["bank"][str(user.id)]["wallet"] = 0
		db["bank"][str(user.id)]["name"] = user.display_name
	

	return True


async def get_bank_data():
	return db["bank"]


async def give_point(ctx):
	user = ctx.author

	await open_account(user)

	db["bank"][str(user.id)]["wallet"] += 1

async def get_user_wallet(ctx):

  user = ctx.author
  users = await get_bank_data()
  
  wallet_amt = users[str(user.id)]["wallet"]

  return wallet_amt
  
  #--------------------------------------------------------

