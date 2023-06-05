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

- **dotabot** plays Dota 2 voice lines - [src](https://github.com/plomdawg/dotabot)
- **musicbot** plays music from youtube - [src](https://github.com/plomdawg/plombot)
- **ttsbot** plays text clips from Elevenlabs - [src](https://github.com/plomdawg/discord-ai-voice-bot)

## Notes

each bot has a different list of:
- secret tokens
- permissions needed
- commands

---

plombot
- downloading mp3s from youtube
- database containing song playcount
- database containing user's Spotify IDs?


dotabot
- downloading mp3s from url
- database mapping of hero names to mp3s
- database containing quiz leaderboard
- database containing user's steam IDs



ai voice bot
- downloading mp3s from url
- database containing metrics (per use cost, voice popularity, etc)

---

shared things:
- playing mp3s in voice channel with a queue
- user in voice channel check
- database with guild settings (volume, etc)
- error handling
- chat formatting
- logging