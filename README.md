# plom's bots

This repo is an effort to consolidate my bots into a single codebase.

## Contents

```bash
├── cogs                   # shared cogs
│   ├── audio.py           # audio library - handles anything that can be heard
│   ├── error_handler.py   # generic error handler
│   └── new_cog_example.py # template cog
├── dota
│   ├── cogs
│   │   ├── database.py    # database that holds hero names and voice lines
│   │   ├── emojis.py      # dota hero emojis that are stored across 3 different discord servers
│   │   ├── help.py        # dota help command
│   │   ├── quiz.py        # Shopkeeper's Quiz!
│   │   ├── voice_lines.py # dota voice line commands
│   │   └── wiki.py        # access data scraped from the dota wiki
│   ├── dota_wiki.json     # dota wiki data (scraped by dota_wiki.py)
│   ├── dota_wiki.py       # scrapes dota wiki data
│   └── dotabot.py         # dotabot
├── plomcord               # shared utility functions that don't fit in a cog
└── requirements.txt       # python dependencies
```

## Bots

- [**dotabot**:](dotabot) plays Dota 2 voice lines & Shopkeeper's Quiz - [original repo](https://github.com/plomdawg/dotabot)
- **musicbot**: plays music from youtube/spotify - [original repo](https://github.com/plomdawg/plombot)
- **ttsbot**: plays text-to-speech clips from Elevenlabs - [original repo](https://github.com/plomdawg/discord-ai-voice-bot)
