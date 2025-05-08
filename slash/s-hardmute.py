import discord
from discord import app_commands
from discord.ext import commands
from utils.embeds import embed_interaction, interaction_desc

class Shardmute(commands.Cog):
   def __init__(self, bot):
        self.bot = bot

   @app_commands.command(
      name = 'hard-mute',
      description = 'Remove all roles of a user and applies mute.'
   )
   @app_commands.describe(
      user = 'User to be sanctioned.',
      reason = 'Reason for sanction.'
   )
   async def hardmute(self, interaction: discord.Interaction, user: discord.Member, reason: str):
      if not interaction.user.guild_permissions.administrator:
         no_perms = embed_interaction(interaction, 'You are not allowed to use this command.', discord.Color.orange())
         no_perms.set_footer(text = 'Permission required: administrator')
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

      h_role = discord.utils.get(interaction.guild.roles, name = 'Hardmute')
      if not h_role:
         try:
            h_role = await interaction.guild.create_role(
               name = 'Hardmute',
               permissions = discord.Permissions(66560),
               colour = discord.Colour.dark_red(),
               hoist = False,
               mentionable = False,
               reason = 'Removes all roles and applies this role.'
            )
            create_hrole = embed_interaction(interaction, 'Role not found and was automatically created.', discord.Color.dark_grey())
            await interaction.response.send_message(embed = create_hrole, ephemeral = True)

            for channel in interaction.guild.channels:
               await channel.set_permissions(h_role)

         except discord.Forbidden:
            nobot_perms = embed_interaction(interaction, 'Error executing command.', discord.Color.dark_red())
            nobot_perms.set_footer(text = 'Check the error documentation.')
            await interaction.response.send_message(embed = nobot_perms, ephemeral = True)
         except Exception as e:
            print(f's-hardmute: {e}')

      if h_role in member.roles:
         alr_mute = embed_interaction(interaction, 'User is already muted.', discord.Color.orange())
         await interaction.response.send_message(embed = alr_mute, ephemeral = True)
         return

      r_r = [role for role in user.roles if role != user.guild.default_role] # filter

      await user.remove_roles(*r_r, reason = 'Remove all roles')
      await user.add_roles(h_role, reason = reason)
      hardmute_ = interaction_desc(interaction, f'Hard Mute: {user.id}', f'Reason: "{reason}"', discord.Color.dark_blue())
      hardmute_.set_footer(text = f'Mute by: {interaction.user.display_name}', icon_url = interaction.user.avatar)
      await interaction.response.send_message(embed = hardmute_, ephemeral = False)

async def setup(bot):
   await bot.add_cog(Shardmute(bot))

# Not solved (test pending)