import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
import feedparser
from utils.config import load_config


class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_news.start()

    def cog_unload(self):
        self.fetch_news.cancel()

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
        feed_url = "https://indianexpress.com/section/latest-news/feed/"
        headlines = []

        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logging.error(f"[IndianExpress] RSS Failed: {e}")
            return []

        for entry in feed.entries[:limit]:
            title = entry.title
            link = entry.link

            embed = discord.Embed(
                title=title,
                url=link,
                description="📰 Source: Indian Express",
                color=discord.Color.orange()
            )

            # ✅ Improved thumbnail handling
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
        feed_url = "https://feeds.feedburner.com/ndtvnews-latest"
        headlines = []

        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logging.error(f"[NDTV] RSS Failed: {e}")
            return []

        for entry in feed.entries[:limit]:
            title = entry.title
            link = entry.link

            embed = discord.Embed(
                title=title,
                url=link,
                description="📰 Source: NDTV",
                color=discord.Color.dark_blue()
            )

            # ✅ Improved thumbnail handling
            if "media_thumbnail" in entry and entry.media_thumbnail:
                embed.set_thumbnail(url=entry.media_thumbnail[0]["url"])
            elif "media_content" in entry and entry.media_content:
                embed.set_thumbnail(url=entry.media_content[0]["url"])
            elif "enclosures" in entry and entry.enclosures:
                embed.set_thumbnail(url=entry.enclosures[0]["href"])

            embed.set_footer(text="FrostNews 24/7 • NDTV.com")
            headlines.append(embed)

        return headlines

    @tasks.loop(minutes=30)  # ⏱️ every 30 min
    async def fetch_news(self):
        logging.info("Auto-fetching headlines...")
        embeds = self.get_all_headlines()

        if not embeds:
            logging.warning("No headlines to send.")
            return

        config = load_config()
        for guild_id, guild_data in config.items():
            channel_id = int(guild_data["news_channel"])
            channel = self.bot.get_channel(channel_id)
            if channel:
                try:
                    for embed in embeds:
                        await channel.send(embed=embed)
                    logging.info(f"Headlines sent to {channel.guild.name} ({channel.name})")
                except Exception as e:
                    logging.error(f"Failed to send to {channel_id}: {e}")


async def setup(bot):
    await bot.add_cog(NewsCog(bot))
