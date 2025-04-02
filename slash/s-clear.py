import discord
from discord.ext import commands
from discord.app_commands import commands as app_commands
from utils.embeds import embed_interaction

class Sclear(commands.Cog):
   def __init__(self, bot):
      self.bot = bot

   @app_commands.command(
      name = 'clear',
      description = 'Clear messages from a channel.'
   )
   @app_commands.describe(
      amount = 'Number of messages to clean'
   )
   async def clear(self, interaction: discord.Interaction, amount: int):
      if not interaction.user.guild_permissions.manage_messages:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text = 'Permission required: manage_messages')
         await interaction.response.send_message(embed = no_perms, ephemeral = True)
         return

      if amount is None or amount <= 0:
         no_amount = embed_interaction(interaction, 'Enter a valid amount', discord.Color.orange())
         no_amount.set_footer(text = 'The amount must be greater than 0.')
         await interaction.response.send_message(embed = no_amount, ephemeral = True)
         return

      await interaction.response.defer(ephemeral = True)
      try:
         await interaction.channel.purge(limit = amount)
         clear_ = embed_interaction(interaction, f'{amount} deleted message(s)', discord.Color.dark_blue())
         await interaction.followup.send(embed = clear_, ephemeral = True)
      except discord.Forbidden:
         nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
         nobot_perms.set_footer(text = 'Check the error documentation.')
         await interaction.response.send_message(embed = nobot_perms, ephemeral = True) # pendiente

async def setup(bot):
   await bot.add_cog(Sclear(bot))

# Solved / English