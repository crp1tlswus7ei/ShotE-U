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

def embed_prefix(ctx, title, color):
    embed = discord.Embed(
        title = title,
        color = color
    )
    return embed