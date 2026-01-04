import discord
from discord.ext import commands
from discord import app_commands
import feedparser
import logging


NEWS_SOURCES = {
    "india": [
        {
            "name": "Indian Express",
            "url": "https://indianexpress.com/section/latest-news/feed/",
            "color": discord.Color.orange(),
            "footer": "IndianExpress.com"
        },
        {
            "name": "NDTV",
            "url": "https://feeds.feedburner.com/ndtvnews-latest",
            "color": discord.Color.dark_blue(),
            "footer": "NDTV.com"
        },
        {
            "name": "The Hindu",
            "url": "https://www.thehindu.com/news/feeder/default.rss",
            "color": discord.Color.red(),
            "footer": "TheHindu.com"
        }
    ],
    "international": [
        {
            "name": "BBC World",
            "url": "http://feeds.bbci.co.uk/news/world/rss.xml",
            "color": discord.Color.gold(),
            "footer": "BBC News"
        },
        {
            "name": "Reuters",
            "url": "https://feeds.reuters.com/reuters/worldNews",
            "color": discord.Color.light_grey(),
            "footer": "Reuters"
        },
        {
            "name": "Al Jazeera",
            "url": "https://www.aljazeera.com/xml/rss/all.xml",
            "color": discord.Color.dark_gold(),
            "footer": "AlJazeera.com"
        }
    ]
}


class NewsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Fetch latest news headlines")
    @app_commands.describe(
        region="India or International",
        topic="Politics, Sports, Tech, Business, World",
        state="Indian state (optional)"
    )
    @app_commands.choices(
        region=[
            app_commands.Choice(name="India", value="india"),
            app_commands.Choice(name="International", value="international"),
        ],
        topic=[
            app_commands.Choice(name="Politics", value="politics"),
            app_commands.Choice(name="Sports", value="sports"),
            app_commands.Choice(name="Technology", value="tech"),
            app_commands.Choice(name="Business", value="business"),
            app_commands.Choice(name="World", value="world"),
        ]
    )
    async def news(
        self,
        interaction: discord.Interaction,
        region: app_commands.Choice[str] | None = None,
        topic: app_commands.Choice[str] | None = None,
        state: str | None = None
    ):
        await interaction.response.defer()

        embeds = self.fetch_news(
            region=region.value if region else None,
            topic=topic.value if topic else None,
            state=state
        )

        if not embeds:
            await interaction.followup.send(
                "⚠️ No matching news found.",
                ephemeral=True
            )
            return

        for embed in embeds:
            await interaction.followup.send(embed=embed)

    def fetch_news(self, region=None, topic=None, state=None, limit=6):
        embeds = []

        regions = [region] if region else NEWS_SOURCES.keys()

        for reg in regions:
            for source in NEWS_SOURCES.get(reg, []):
                try:
                    feed = feedparser.parse(source["url"])
                except Exception as e:
                    logging.error(f"[{source['name']}] RSS failed: {e}")
                    continue

                for entry in feed.entries:
                    title = entry.title.lower()

                    if topic and topic not in title:
                        continue

                    if state and state.lower() not in title:
                        continue

                    embed = discord.Embed(
                        title=entry.title,
                        url=entry.link,
                        description=f"📰 Source: {source['name']}",
                        color=source["color"]
                    )

                    if "media_thumbnail" in entry and entry.media_thumbnail:
                        embed.set_thumbnail(url=entry.media_thumbnail[0]["url"])
                    elif "media_content" in entry and entry.media_content:
                        embed.set_thumbnail(url=entry.media_content[0]["url"])
                    elif "enclosures" in entry and entry.enclosures:
                        embed.set_thumbnail(url=entry.enclosures[0]["href"])

                    embed.set_footer(
                        text=f"FrostNews 24/7 • {source['footer']}"
                    )

                    embeds.append(embed)

                    if len(embeds) >= limit:
                        return embeds

        return embeds


async def setup(bot):
    await bot.add_cog(NewsCog(bot))
    logging.info("NewsCog loaded.")