import discord
from discord import app_commands
from discord.ext import commands

from mdw.c_roles import CreateMuteRole
from utils.embeds import embed_interaction, interaction_desc

class Smute(commands.Cog):
   from mdw.c_roles import CreateMuteRole
   def __init__(self, bot):
        self.bot = bot

   @app_commands.command(
      name = "mute",
      description = "Mutes a user indefinitely.",
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def mute(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.manage_roles:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if user is None:
         no_user = embed_interaction(interaction, 'You must mention a user.', discord.Color.orange())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role:
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.orange())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      m_role = discord.utils.get(interaction.guild.roles, name = "Muted")
      if not m_role:
         try:
            await CreateMuteRole(interaction)
            create_role = embed_interaction(interaction, 'Role not found and was automatically created.', discord.Color.dark_grey())
            create_role.set_footer(text = 'Check the documentation for more details.')
            await interaction.response.send_message(embed = create_role, ephemeral = True)

            for channel in interaction.guild.channels:
               await channel.set_permissions(m_role)

         except discord.Forbidden:
            nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
            nobot_perms.set_footer(text = 'Check the error documentation.')
            await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
         except Exception as e:
            print(f's-mute: {e}')

      if m_role in user.roles:
         alr_mute = embed_interaction(interaction, 'User is already muted.', discord.Color.orange())
         await interaction.response.send_message(embed = alr_mute, ephemeral = True)
         return

      await user.add_roles(m_role, reason = reason)
      mute_ = interaction_desc(interaction, f'Mute: **{user.id}**', f'Reason: "{reason}"', discord.Color.dark_blue())
      mute_.set_footer(text = f'Mute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
      await interaction.response.send_message(embed = mute_, ephemeral = False)

async def setup(bot):
   await bot.add_cog(Smute(bot))

# Solved