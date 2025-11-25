import discord
from discord.ext import commands
from discord import app_commands
import logging
import feedparser


class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Fetch top headlines from multiple sources")
    async def manual_news(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embeds = self.get_all_headlines()

        if embeds:
            for embed in embeds:
                await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("⚠️ Unable to fetch news at the moment. Please try again later.")

    def get_all_headlines(self):
        return self.scrape_indian_express(limit=2) + self.scrape_ndtv(limit=2)

    def scrape_indian_express(self, limit=2):
        url = "https://indianexpress.com/section/latest-news/feed/"
        headlines = []
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            logging.error(f"[IndianExpress] RSS Failed: {e}")
            return []

        for entry in feed.entries[:limit]:
            embed = discord.Embed(
                title=entry.title,
                url=entry.link,
                description="📰 Source: Indian Express",
                color=discord.Color.orange()
            )

            if "media_thumbnail" in entry and entry.media_thumbnail:
                embed.set_thumbnail(url=entry.media_thumbnail[0]["url"])
            elif "media_content" in entry and entry.media_content:
                embed.set_thumbnail(url=entry.media_content[0]["url"])
            elif "enclosures" in entry and entry.enclosures:
                embed.set_thumbnail(url=entry.enclosures[0]["href"])

            embed.set_footer(text="FrostNews 24/7 • IndianExpress.com")
            headlines.append(embed)
        return headlines

    def scrape_ndtv(self, limit=2):
        url = "https://feeds.feedburner.com/ndtvnews-latest"
        headlines = []
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            logging.error(f"[NDTV] RSS Failed: {e}")
            return []

        for entry in feed.entries[:limit]:
            embed = discord.Embed(
                title=entry.title,
                url=entry.link,
                description="📰 Source: NDTV",
                color=discord.Color.dark_blue()
            )

            if "media_thumbnail" in entry and entry.media_thumbnail:
                embed.set_thumbnail(url=entry.media_thumbnail[0]["url"])
            elif "media_content" in entry and entry.media_content:
                embed.set_thumbnail(url=entry.media_content[0]["url"])
            elif "enclosures" in entry and entry.enclosures:
                embed.set_thumbnail(url=entry.enclosures[0]["href"])

            embed.set_footer(text="FrostNews 24/7 • NDTV.com")
            headlines.append(embed)
        return headlines


async def setup(bot):
    await bot.add_cog(NewsCog(bot))
