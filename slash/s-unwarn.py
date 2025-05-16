import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction

class Sunwarn(commands.Cog):
   from mdw.warn_system import get_warns, remove_warn
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'unwarn',
      description = 'Removes only one warn from a user.',
      nsfw = False
   )
   @app_commands.describe(
      user = 'User to clean warn.'
   )
   async def unwarn(self, interaction: discord.Interaction, user: discord.Member, amount: int):
      if not interaction.user.guild_permissions.manage_roles: #
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.light_gray())
         no_perms.set_footer(text = 'Permission required: manage_roles')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if interaction.user.top_role <= user.top_role: #
         insf_perms = embed_interaction(interaction, 'You do not have permissions on this user.', discord.Color.light_gray())
         await interaction.response.send_message(embed = insf_perms, ephemeral = True)
         return

      user_id = str(user.id)
      warns_ = self.get_warns(user_id)

      if not warns_:
         no_warns = embed_interaction(interaction, f'**{user.display_name}** has no warns to clean.', discord.Color.dark_blue())
         await interaction.response.send_message(embed = no_warns, ephemeral = True)
         return

      try: #
         if 1 <= amount <= len(warns_):
            self.remove_warn(user_id, amount - 1)
            unwarn_ = embed_interaction(interaction, f'**{user.display_name}** warn removed.', discord.Color.dark_blue())
            unwarn_.set_footer(text = f'Warns: {len(warns_) - 1}')
            await interaction.response.send_message(embed = unwarn_, ephemeral = False)
         else: #
            uw_e = embed_interaction(interaction, 'Invalid warn.', discord.Color.orange())
            uw_e.set_footer(text = 'Enter a valid number.')
            await interaction.response.send_message(embed = uw_e, ephemeral = True)
      except discord.Forbidden: #
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text='Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
      except Exception as e:
         print(f's-unwarn: {e}')

async def setup(bot):
   await bot.add_cog(Sunwarn(bot))

# Solved