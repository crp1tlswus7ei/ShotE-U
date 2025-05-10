import discord

async def CreateMuteRole(interaction: discord.Interaction):
   await interaction.guild.create_role(
      name = 'Muted',
      permissions = discord.Permissions(4296082432),
      colour = discord.Colour.dark_red(),
      hoist = False,
      mentionable = False,
      reason = 'Mute or Hardmute role.'
   )