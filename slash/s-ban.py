import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import embed_interaction

class Sban(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'ban',
      description = 'Permanent expulsion to a user'
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def ban(self, interaction: discord.Interaction, user: discord.Member, *, reason: str = None):
      if not interaction.user.guild_permissions.ban_members: #
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text = 'Permission required: ban_members')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None: #
         no_user = embed_interaction(interaction, 'You must mention a user.', discord.Color.orange())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      try:
         await user.ban(reason = reason) #
         ban_ = embed_interaction(interaction, f'Ban: {user.id}', discord.Color.dark_blue())
         ban_.set_footer(text = f'Ban by: {interaction.user.display_name}', icon_url = interaction.user.avatar) #
         await interaction.response.send_message(embed = ban_, ephemeral = False)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)

async def setup(bot):
   await bot.add_cog(Sban(bot))

# Solved / English