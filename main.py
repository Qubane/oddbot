import os
import sys
import discord
from discord.ext import commands


class Client(commands.Bot):
    def __init__(self):
        super(Client, self).__init__(command_prefix="!", intents=discord.Intents.all(),
                                     help_command=None)

        # make sure the var directory is present
        if not os.path.isdir("var"):
            os.mkdir("var")

        # list of all discord cogs
        # format: {"extension": "filepath"}
        self.working_extensions: dict[str, str] = {}

        # list of discord cogs that loaded by default
        # format: ["extension1", "extension2", ...]
        self.loaded_extensions: list[str] = [
            "SillyID"
        ]

        # check all the installed extensions
        self.check_working_extensions()

    def check_working_extensions(self):
        """
        Checks all working extensions for the presence of main.py file
        """

        for folder in os.listdir("client_cogs"):
            # check if main file exists
            if os.path.isfile(f"client_cogs/{folder}/main.py"):
                # import the extension to the list of working extensions
                # with the name being the name of the folder it's in
                self.working_extensions[folder] = f"client_cogs.{folder}.main"

    async def load_custom_extension(self, name):
        """
        Loads custom cog
        """

        await self.load_extension(self.working_extensions[name])

    async def unload_custom_extension(self, name):
        """
        UnLoads custom cog
        """

        await self.unload_extension(self.working_extensions[name])

    async def reload_custom_extension(self, name):
        """
        ReLoads custom cog
        """

        await self.reload_extension(self.working_extensions[name])

    async def setup_hook(self) -> None:
        """
        Cog loading when the bot is launched
        """

        for ext in self.loaded_extensions:
            await self.load_custom_extension(ext)

    async def on_ready(self) -> None:
        """
        Things that happen when the bot is launched
        """

        # change activity
        print("\nBot started successfully!\n")
        await self.change_presence(activity=discord.Game("God Revision 2"))

        # # sync the command tree
        # sync = await self.tree.sync()
        # print(f"Slash command tree synced {len(sync)} commands\n")

        # print the done message
        print("Done!\n")


def main():
    # Useless message at the start of the bot
    if os.name != "nt":
        print("NOTE: You are running on non-windows machine, some of the things may be buggy\n"
              "Please report any issues to 'https://github.com/UltraQbik/oddbot/issues'\n\n")

    client = Client()
    client.run(sys.argv[1])


if __name__ == '__main__':
    main()
