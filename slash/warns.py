import os
import discord
from pymongo import MongoClient
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction

MONGO_URI = os.getenv("MONGO_URI")
shot = MongoClient(MONGO_URI)
db = shot["kiko"]
w_coll = db["warns"]

class WarnSys(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   def get_warns(self, user_id):
      user_data = w_coll.find_one({"_id": user_id})
      return user_data["warnings"] if user_data else []

   def add_warns(self, user_id, reason):
      warns = self.get_warns(user_id)
      warns.append(reason)
      w_coll.update_one({"_id": user_id}, {"$set": {"warnings": warns}}, upsert=True)
      return len(warns)

   def clear_warns(self, user_id):
      w_coll.update_one({"_id": user_id}, {"$set": {"warnings": []}})

   def remove_warn(self, user_id, amount):
      warns = self.get_warns(user_id)
      if 0 <= amount < len(warns):
         del warns[amount]
         w_coll.update_one({"_id": user_id}, {"$set": {"warnings": warns}})
         return True
      return False

   @app_commands.command(
      name = 'warn',
      description = 'Warn a user about behavior.',
      nsfw = False
   )
   @app_commands.describe(
      user='User to be sanctioned',
      reason = 'Reason for sanction'
   )
   async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         user_id = str(user.id)
         total_warns = self.add_warns(user_id, reason)
         warn_ = embed_interaction(interaction, f'**{user.display_name}** has been warned.', discord.Color.dark_blue())
         warn_.set_footer(text=f'Warns: {total_warns}')
         await interaction.response.send_message(embed = warn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

   @app_commands.command(
      name = 'unwarn',
      description = 'Removes only one warn from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clean warn.'
   )
   async def unwarn(self, interaction: discord.Interaction, user: discord.Member, amount: int):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      user_id = str(user.id)
      warns_ = self.get_warns(user_id)

      if not warns_:
         no_warns = embed_interaction(interaction, f'**{user.display_name}** has no warns to clean.', discord.Color.dark_blue())
         await interaction.response.send_message(embed = no_warns, ephemeral = True)
         return

      try:
         if 1 <= amount <= len(warns_):
            self.remove_warn(user_id, amount - 1)
            unwarn_ = embed_interaction(interaction, f'**{user.display_name}** warn removed.', discord.Color.dark_blue())
            unwarn_.set_footer(text=f'Warns: {len(warns_) - 1}')
         else:
            uw_e = embed_interaction(interaction, 'Invalid warn.', discord.Color.orange())
            uw_e.set_footer(text='Enter a valid number.')
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

   @app_commands.command(
      name = 'clear-warns',
      description = 'Clears all warnings from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clear warns.'
   )
   async def clearwarns(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         user_id = str(user.id)
         self.clear_warns(user_id)
         clearw_ = embed_interaction(interaction, f'**{user.display_name}** warns cleaned.', discord.Color.dark_blue())
         clearw_.set_footer(text=f'Cleaned by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = clearw_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

   @app_commands.command(
      name = 'warnings',
      description = 'list of user warnings',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to review warns.'
   )
   async def warnings(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         user_id = str(user.id)
         user_warns = self.get_warns(user_id)
         if user_warns:
            warnn_ = embed_interaction(interaction, f'**{user.display_name}** warns:\n' + '\n'.join(user_warns), discord.Color.dark_blue())
            warnn_.set_footer(text=f'List requested by: {interaction.user.display_name}',  icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = warnn_, ephemeral = False)
         else:
            no_warnn_ = embed_interaction(interaction, f'**{user.display_name}** has no warnings.', discord.Color.dark_blue())
            no_warnn_.set_footer(text=f'List requested by: {interaction.user.display_name}', icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed = no_warnn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

async def setup(bot):
   await bot.add_cog(WarnSys(bot))