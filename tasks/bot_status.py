import discord
from itertools import cycle
from discord.ext.tasks import loop

STATUS_LIST = cycle(["/spools", "/leaderboard", "/pontuação","/convite"])
STATUS_LOOP_DURATION_SEGS = 5

def setup(bot):
	@loop(seconds=STATUS_LOOP_DURATION_SEGS)
	async def status_loop():
		activity = discord.Activity(type=discord.ActivityType.watching, name=next(STATUS_LIST))
		await bot.change_presence(status=discord.Status.online, activity=activity)

	@status_loop.before_loop
	async def status_loop_before():
		await bot.wait_until_ready()


	status_loop.start()