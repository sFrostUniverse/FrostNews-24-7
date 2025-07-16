# 🧊 FrostNews 24/7 — Live Indian News on Discord

FrostNews 24/7 is a global-ready Discord bot that delivers **real-time Indian news headlines** straight into your server — powered by direct web scraping from trusted Indian sources like *The Indian Express*.

> ❄️ Built with 💙 by [@sFrostUniverse](https://github.com/sFrostUniverse)

---

## ✨ Features

- 📰 **Top Indian Headlines** delivered every 15 minutes
- 📡 Uses live scraping from news websites (no API key needed)
- 📍 Server-specific news channels via `/setup`
- 🧪 `/news` for manual headline fetch anytime
- 🔁 `/reconfigure` to change the news channel later
- 🌐 Fully production-ready and scalable for any public server

---

## 🔧 Setup Guide

### 1. Invite the Bot
> *(This depends on your public bot setup — add your invite link here when ready)*

### 2. Run `/setup`
Use the `/setup` command and select a text channel where the news will be posted.

### 3. That’s it!
FrostNews will now post updates every 15 minutes automatically.

---

## 📦 Slash Commands

| Command       | Description                                |
|---------------|--------------------------------------------|
| `/setup`      | Set the channel to receive auto-news       |
| `/reconfigure`| Change the news channel later              |
| `/news`       | Manually fetch top headlines anytime       |
| `/help`       | View all bot commands                      |

---

## ⚙️ Requirements

- Python 3.10+
- `requirements.txt` dependencies (install using `pip install -r requirements.txt`)
- `.env` file with your bot token:
  ```
  DISCORD_TOKEN=your_token_here
  ```

---

## 📁 Project Structure

```
FrostNews/
│
├── cogs/                # Bot commands and news logic
│   ├── news.py
│   ├── setup.py
│   └── reconfigure.py
│
├── data/config.json     # Stores per-server news channel settings
├── utils/config.py      # Load/save news channels
├── utils/logger.py      # Logging system
├── keep_alive.py        # Render hosting support
├── main.py              # Bot entry point
├── requirements.txt
└── .env
```

---

## 📸 Preview

*(Add a screenshot here of your bot posting a real headline)*

---

## 🛡️ License

This project is open-source and available under the MIT License.

---

### 🤖 Built for the people, by the people — Indian news never stops.
