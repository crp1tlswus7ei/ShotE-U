import discord

def embed_interaction(interaction: discord.Interaction, title: str, color: discord.Color) -> discord.Embed:
    embed = discord.Embed(
        title = title,
        color = color
    )
    return embed

def interaction_desc(interaction: discord.Interaction, title: str, description: str, color: discord.Color) -> discord.Embed:
    embed = discord.Embed(
        title = title,
        description = description,
        color = color
    )
    return embed

def only_desc(interaction: discord.Interaction, description: str, color: discord.Color) -> discord.Embed:
    embed = discord.Embed(
        description = description,
        color = color
    )
    return embed