"""Simple A2S Player Count Bot v1.0"""
import asyncio
import discord
from discord.ext import commands
import a2s


class Timer:
    def __init__(self, timeout, name, callback):
        self._timeout = timeout
        self._callback = callback
        self.name = name
        self.wait_for = asyncio.create_task(self.wait_for_task())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()
        self.cancel()

    async def wait_for_task(self):
        while True:
            tasks = asyncio.all_tasks()
            try:
                if self.name in f'{tasks}':
                    await asyncio.sleep(self._timeout)
                else:
                    break
            except Exception as err:
                print(err)
                break
        self._task = asyncio.create_task(self._job(), name=self.name)

    def cancel(self):
        self._task.cancel()


class PlayerCountBot(commands.Bot):
    """Player Count Bot"""
    def __init__(self):
        super().__init__(
            command_prefix='&',
            intents=discord.Intents.all(),
            application_id=#Replace this comment with the application ID of the bot account
        )

    async def player_count(self):
        """Player Count Job"""
        try:
            # Replace anything wrapped in <> with what it is asking for. ie. '<foo>' with 'bar'
            server_addr = ('<IP address>', int(<Query Port Number>))

            response = a2s.info(server_addr, timeout=10.0)
            players = int(response.player_count)
            max_players = int(response.max_players)

            if max_players > 0:
                # You can replace the "name" of the status to whatever you want. Keep in mind that {players} is the online number and {max_players} is your server limit
                await self.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{players}/{max_players}'))
            else:
                # This is just so the bot looks away when there is no one online
                await self.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f'{players}/{max_players}'))

            # This is where you set how often you want it updating (in seconds)
            Timer(60, 'player_count', self.player_count)
        except Exception as err:
            print(f'Error in getting the player count: {err}')
            await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=f'Trying to connect...'))
            # Even if it fails, you still want it to try again later
            Timer(60, 'player_count', self.player_count)


    async def run_jobs(self):
        """Run the async jobs"""
        try:
            await self.player_count()
            print('Jobs started.')
        except Exception as err:
            print(f'Error starting jobs: {err}')

    async def on_ready(self):
        """Do stuff when ready"""
        try:
            # While we're starting up, we'll call the job that will run the player count
            await self.run_jobs()
            # Won't really need anything in here since there won't be any commands
            print("Player Count Bot is running!")
        except Exception as err:
            print(err)


asyncio.run(PlayerCountBot().start(#Replace this comment with the Application Token from the Bot config. You will likely need to generate it using the site
    ))
        