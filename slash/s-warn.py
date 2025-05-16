import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction, interaction_desc

class Swarn(commands.Cog):
   from mdw.warn_system import add_warns, get_warns
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'warn',
      description = 'Warn a user about behavior.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to be sanctioned',
      reason = 'Reason for sanction'
   )
   async def warn(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text='Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         user_id = str(user.id)
         total_warns = self.add_warns(user_id, reason)
         warn_ = interaction_desc(interaction, f'**{user.display_name}** has been warned.', f'**Warns:** {total_warns}', discord.Color.dark_blue())
         warn_.set_footer(text = f'Warn by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
         await interaction.response.send_message(embed = warn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-warn: {e}')

async def setup(bot):
   await bot.add_cog(Swarn(bot))

# Solved