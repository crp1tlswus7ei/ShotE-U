import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction

class SclearW(commands.Cog):
   from mdw.warn_system import clear_warns
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'clear-warns',
      description = 'Clears all warnings from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clear warns.'
   )
   async def clearwarns(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles: #
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try: #
         user_id = str(user.id)
         self.clear_warns(user_id)
         clearw_ = embed_interaction(interaction, f'**{user.display_name}** warns cleaned.', discord.Color.dark_blue())
         clearw_.set_footer(text=f'Cleaned by: {interaction.user.display_name}', icon_url=interaction.user.avatar)
         await interaction.response.send_message(embed = clearw_, ephemeral = False)
      except discord.Forbidden: #
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e: #
         print(f's-clear_warns: {e}')

async def setup(bot):
   await bot.add_cog(SclearW(bot))

# Solved