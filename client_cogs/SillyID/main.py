"""
This is a cog, which adds silly id's to users.
Also adds a command, which allows to check that ID.
"""


import json
import os.path
import logging
import discord
from discord import app_commands
from discord.ext import commands


class EXTSillyID(commands.Cog):
    """
    This is a SillyID cog
    """

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

        # some cog configs
        self.gap_size: int = 3
        self.bit_width: int = self.gap_size * 3
        self.max_int: int = (2 ** self.bit_width) - 1

        # path to silly id database
        self.db_path: str = "var/silly_db.json"

        # silly database
        self.silly_db: dict[str, int] | None = None

        # read the silly database
        self.read_db()

    @app_commands.command(name="ckusr", description="returns information about the user")
    async def check_user(
        self,
        interaction: discord.Interaction,
        user: discord.Member
    ) -> None:
        """
        This is the ckusr slash command, which prints information about the user, including the silly id.
        """

        # die if database is not yet loaded
        if self.silly_db is None:
            return

        # make sure the user have their silly id
        if user.id.__str__() not in self.silly_db:
            # add new id
            self.silly_db[user.id.__str__()] = self.make_silly_id(user.id)

            # store the database
            self.store_db()

        # make a pretty embed
        embed = discord.Embed(title=f"Discord ID", description=f"{user.id}",
                              color=discord.Color.green())
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.add_field(name="Silly ID",
                        value=f"{self.format_silly_id(self.silly_db[user.id.__str__()])}", inline=False)

        # send that embed to user
        await interaction.response.send_message(embed=embed)

    def make_silly_id(self, id_: int) -> int:
        """
        Returns a silly id from normal user id
        :return: silly id
        """

        # calculate basic silly id
        silly_id = id_ & self.max_int

        # prevent any collisions
        count = 0
        while silly_id in self.silly_db.values():
            silly_id = (silly_id + 1) & self.max_int

            # check if we ran out of id's
            count += 1
            if count > self.max_int+1:  # +1 just to be safe
                logging.error("no more id's available. Shutting down SillyID cog")
                self.cog_unload()
                raise IndexError

        # if everything went well -> return id
        return silly_id

    def format_silly_id(self, sid_: int) -> str:
        """
        Outputs sillily formatted silly id. Ex. 110.010.101
        :param sid_: silly id
        :return: formatted id
        """

        # make string
        sid = bin(sid_)[2:].rjust(self.bit_width, '0')

        # return formatted silly id
        return '.'.join([sid[i:i+self.gap_size] for i in range(0, len(sid), self.gap_size)])

    def store_db(self):
        """
        Stores the database
        """

        with open(self.db_path, "w", encoding='utf8') as file:
            file.write(json.dumps(self.silly_db, indent=2))

    def read_db(self):
        """
        Reads the database
        """

        if not os.path.isfile(self.db_path):
            logging.error("unable to locate sillyid database")
            logging.info("creating empty sillyid database")
            self.store_db()
            return

        with open(self.db_path, "r", encoding='utf8') as file:
            self.silly_db = json.loads(file.read())


async def setup(client: commands.Bot) -> None:
    await client.add_cog(EXTSillyID(client))
