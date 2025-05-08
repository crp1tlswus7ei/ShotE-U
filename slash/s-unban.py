import discord
from discord.ext import commands
from discord import app_commands
from utils.embeds import embed_interaction

class Sunban(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'unban',
      description = 'Remove ban of a user.'
   )
   @app_commands.describe(
      user_id = 'ID of the user to remove ban.'
   )
   async def unban(self, interaction: discord.Interaction, *, user_id: str):
      if not interaction.user.guild_permissions.ban_members:
         insf_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         insf_perms.set_footer(text = 'Permission required: ban_members')
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      if user_id is None:
         no_user = embed_interaction(interaction, 'The ID cannot be empty.', discord.Color.orange())
         await interaction.response.send_message(embed = no_user, ephemeral = True)
         return

      try:
         user_id = int(user_id)
      except ValueError:
         w_e = embed_interaction(interaction, 'Invalid ID.', discord.Color.orange())
         await interaction.response.send_message(embed = w_e, ephemeral = True)
         return
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-unban: {e}')

      banned_users = interaction.guild.bans()
      async for ban_entry in banned_users:
         user = ban_entry.user
         if user.id == user_id:
            await interaction.guild.unban(user)
            unban_ = embed_interaction(interaction, f'Unban: {user_id}', discord.Color.dark_blue())
            unban_.set_footer(text = f'Unban by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = unban_, ephemeral = False)
            return

      no_user = embed_interaction(interaction, 'This ID does no exist.', discord.Color.orange())
      no_user.set_footer(text = 'Make sure the ID is correct.')
      await interaction.response.send_message(embed = no_user, ephemeral = True)
      return

async def setup(bot):
   await bot.add_cog(Sunban(bot))

# Solved