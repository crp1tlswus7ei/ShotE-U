import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction

class WarnSys(commands.Cog):
   from mdw.warn_system import get_warns
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'warnings',
      description = 'list of user warnings',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to review warns.'
   )
   async def warnings(self, interaction: discord.Interaction, user: discord.Member):
      if not interaction.user.guild_permissions.manage_roles: #
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
         if user_warns: #
            warnn_ = embed_interaction(interaction, f'**{user.display_name}** warns:\n' + '\n'.join(user_warns), discord.Color.dark_blue())
            warnn_.set_footer(text=f'List requested by: {interaction.user.display_name}',  icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = warnn_, ephemeral = False)
         else: #
            no_warnn_ = embed_interaction(interaction, f'**{user.display_name}** has no warnings.', discord.Color.dark_blue())
            no_warnn_.set_footer(text=f'List requested by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = no_warnn_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

async def setup(bot):
   await bot.add_cog(WarnSys(bot))

# Solved