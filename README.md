# plom's bots

This repo is an effort to consolidate my bots into a single codebase.

## Contents

```bash
├── cogs                   # shared cogs
│   ├── audio.py           # audio library - handles anything that can be heard
│   ├── dota               # dota-related cogs
│   │   ├── database.py    # dota-related database that holds hero names and voice lines
│   │   ├── emojis.py      # dota-related emojis that are stored in 3 different discord servers
│   │   ├── help.py        # dota-related help command
│   │   ├── quiz.py        # Shopkeeper's Quiz!
│   │   ├── voice_lines.py # dota voice line commands
│   │   └── wiki.py        # used to access data scraped from the dota wiki
│   ├── error_handler.py   # generic error handler
│   └── new_cog_example.py # template cog
├── dota_wiki.json         # dota wiki data (scraped by dota_wiki.py)
├── dota_wiki.py           # scrapes dota wiki data
├── dotabot.py             # dotabot
├── plomcord               # shared utility functions that don't fit in a cog
└── requirements.txt       # python dependencies
```

## Bots

- [**dotabot**:](dota) plays Dota 2 voice lines & Shopkeeper's Quiz - [original repo](https://github.com/plomdawg/dotabot)
- **musicbot**: plays music from youtube/spotify - [original repo](https://github.com/plomdawg/plombot)
- **ttsbot**: plays text-to-speech clips from Elevenlabs - [original repo](https://github.com/plomdawg/discord-ai-voice-bot)
