# Eldoria Chronicles

A text-based fantasy RPG built in Python with branching storylines, turn-based combat, companions, crafting, side quests, achievements, persistent saves, and multiple endings.

## The Story

One hundred years ago, the sorcerer Malachar shattered the five Crystal Shards that kept Eldoria alive.

Official history says he destroyed them out of madness.

The surviving records say something different.

The Shards may have been broken to stop something from entering the world — and the kingdom may have spent a century hiding the truth.

You begin as an ordinary traveller in Greyhaven. Then the Crown arrives looking for you, your mother disappears, and a strange mark appears beneath your palm.

From the burning roads of Greyhaven to the drowned ruins beyond the Sea of Glass, your choices determine who trusts you, which companions remain at your side, what Eldoria remembers, and what waits behind the final door.

## Campaign

The game is structured as a five-act campaign:

1. **Ashes of Greyhaven** — flee the Crown and uncover the first lie surrounding the Shattering.
2. **The Green That Remains** — enter the dying Root-City and discover that the forest remembers history differently.
3. **The City Without a King** — infiltrate the capital and learn why the throne has been empty for twelve years.
4. **The Sea of Glass** — explore the wound left by the Shattering and discover the original prophecy.
5. **The Shattered Crown** — face Malachar, the Regent, the five Shards, and the truth behind the Sixth.

The expanded narrative content lives in `eldoria_story.py`, keeping story data separate from combat and save-state logic.

## Character Classes

There are **8 playable classes**, each with a different combat identity and lore:

- Knight of Ashenveil
- Shadowblade
- Arcanist
- Warden of the Wild
- Paladin of the Eternal Flame
- Necromancer
- Beastcaller
- Runeblade

## Features

- **5-act story campaign** with branching decisions
- **8 playable classes**
- **Turn-based combat** with enemy abilities and AI
- **Class skills** with different mechanics
- **Levelling system** with multi-level XP handling
- **Companions** with independent combat state and personal stories
- **8 side quests** with narrative consequences
- **Crafting system** with chained recipes
- **Dynamic weather** that affects combat
- **Inventory and consumables**
- **Achievements and bestiary tracking**
- **Reputation and moral choices**
- **Persistent JSON saves** with validation and atomic writes
- **Multiple endings**, including a hidden Sixth Shard ending
- **Standard-library only** — no external Python packages required

## Endings

The campaign now supports five major outcomes:

- **The Warrior's Crown** — defeat the threat through strength and claim responsibility for what follows.
- **The Price of Mercy** — refuse the easy answer of revenge and give Malachar a chance to finish what he started.
- **The Unlikely Alliance** — unite enemies who have spent a century blaming one another.
- **The Shattered World** — destroy the Shards and end the cycle of magical power.
- **The Sixth Shard** — uncover the hidden memory behind the prophecy and reject the roles written for you.

A darker outcome is also possible if the player's reputation collapses far enough.

## How to Play

```bash
python3 eldoria_chronicles.py
```

The game requires Python 3 and the Python standard library only.

## Development

The stability branch focuses on fixing state-related bugs while expanding the campaign without introducing third-party dependencies.

Before merging, run:

```bash
python3 -m py_compile eldoria_chronicles.py eldoria_story.py
python3 eldoria_chronicles.py
```

The first command catches syntax errors without starting the game. The second is a manual gameplay check for saves, combat, progression, story flow, and endings.

*The prophecy tells you what you are supposed to become. The game lets you decide whether it is telling the truth.*
