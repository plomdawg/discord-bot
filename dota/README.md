# dotabot

`dotabot` is a Discord bot that brings Dota 2 to your server. Its primary features include Dota 2 voice lines and the Shopkeeper's Quiz.

## Features

### Voice Lines

The voice lines feature allows users to play audio clips of voice responses from Dota 2 heroes. Here's how the bot responds to different types of messages:

- If the message is an exact match for a response, the bot will play that response in the user's voice channel.
- If the message starts with "dota" (e.g., "dota haha"), the bot will play a random response from any hero that contains the text.
- If the message starts with "hero" (e.g., "hero juggernaut"), the bot will play a random response from the specified hero.
- If the message ends with a number (e.g., "dota haha 2"), the bot will play the nth response in the query.

Responses can be searched for by either the full quote with exact punctuation (e.g., "Haha!") or by a partial quote prefixed by "dota" (e.g., "dota haha").

### Shopkeeper's Quiz

The Shopkeeper's Quiz is an interactive game where users have to guess Dota 2 heroes, abilities, and items based on their scrambled names. The quiz consists of several rounds, and each round follows these four phases:

1. The bot shows a hard scramble of the word without the category.
2. The bot shows a hard scramble with the category hint.
3. The bot shows an easy scramble (spaces in their places) with the category hint.
4. If there's an additional hint available, the bot shows an easy scramble with both category and the additional hint.

The quiz tracks each user's performance and calculates scores based on the speed of correct answers and the number of participants. Once the quiz concludes, it displays the results showing winners, losers, and earned gold for each participant. Users can hit the 🆕 reaction to start a new game.

## Setup and Usage

To set up and use the `dotabot`, follow these steps:

1. Invite the bot to your server using the provided invite link.
2. The bot will greet you and provide basic instructions on usage.
3. Join a voice channel to enable voice lines playback.
4. Type or send the desired command (e.g., "dota haha" or "hero juggernaut") in the text channel to play a voice line.
5. To start the Shopkeeper's Quiz, type `/quiz` in the text channel.

Enjoy!

---

## File Structure Overview

The bot consists of several Python files, each handling specific responsibilities:

- `dotabot.py`: Main script responsible for loading and running the cogs.
- `wiki.py`: A utility cog that handles the Dota 2 wiki data, used by other cogs.
- `voice_lines.py`: A cog dedicated to the voice lines feature.
- `quiz.py`: A cog responsible for managing and running the Shopkeeper's Quiz.
- `dota_wiki.py`: A script used to scrape the Dota 2 wiki for data.


## Scraping data from dota wiki

The `dota_wiki.py` script is responsible for scraping data from the Dota 2 wiki. It extracts information about heroes, their abilities, responses, and in-game items. A combination of Python libraries, including `requests`, and `BeautifulSoup`, is used to achieve this.

1. The `DOTA_WIKI_URL` constant is created, containing the base URL for the Dota 2 wiki.
2. Several helper functions are implemented, such as `_load_page`, `get_abilities`, `get_responses`, `get_thumbnail`, `get_heroes`, and `get_items`.
3. The `_load_page` function retrieves a specified webpage and returns its BeautifulSoup object.
4. The `get_abilities` function extracts ability details, including names, lore text, and thumbnails for a given hero.
5. The `get_responses` function gathers details about responses, such as their text and corresponding URLs for each hero.
6. The `get_thumbnail` function retrieves a hero or announcer pack's thumbnail URL.
7. The `Hero` class is initialized, and each hero object is constructed with related attributes, such as name, URL, thumbnail, abilities, and responses.
8. The `get_heroes` function obtains a list of hero objects by scraping the Dota wiki.
9. The `get_items` function collects a list of in-game item details, including name, URL, gold cost, lore, and thumbnails.
10. In the `__main__` block, the script compiles gathered data into a single dictionary containing heroes and items.
11. It finally exports the data in the YAML and JSON formats.

The exported data is utilized by the `dotabot` for various tasks, including voice lines playback and the Shopkeeper's Quiz game.
