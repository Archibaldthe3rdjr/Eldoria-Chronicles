"""Expanded narrative content for Eldoria Chronicles.

The story is deliberately data-driven so the main game can present long-form
scenes without burying game logic inside thousands of print statements.
Standard library only.
"""

STORY_VERSION = 3

PROLOGUE = [
    ("The Last Dawn", "The bells of Greyhaven ring before sunrise. Not for prayer. For warning."),
    ("The Last Dawn", "For three nights the moon has appeared fractured, a white scar running through its centre."),
    ("The Last Dawn", "You wake with ash on your tongue and a mark burning beneath your palm."),
    ("The Last Dawn", "Nobody in the village remembers seeing the mark before. Your mother does."),
    ("The Last Dawn", "She looks at it once, then locks the door."),
    ("The Last Dawn", "'Whatever happens,' she whispers, 'do not let the Crown find you.'"),
    ("The Last Dawn", "Outside, riders in silver masks enter the village. Their banners bear the symbol of the Eternal Crown."),
    ("The Last Dawn", "The oldest rider calls your name."),
    ("The Last Dawn", "He should not know it."),
    ("The Last Dawn", "Your mother pushes a rusted sword into your hands and points towards the forest."),
    ("The Last Dawn", "'Run. Find the old road. Find the ruined chapel. And when the dead begin speaking, listen.'"),
]

ACTS = {
    1: {
        "title": "Ashes of Greyhaven",
        "subtitle": "A village remembers what the kingdom chose to forget.",
        "scenes": [
            ("The Burning Gate", "Greyhaven's eastern gate is already burning when you reach it. Behind you, bells turn to screams."),
            ("The Old Road", "The forest road is almost swallowed by roots. Someone has scratched five circles into the bark of every third tree."),
            ("The Chapel of Cinders", "The ruined chapel contains no priest, only a black altar and a child's drawing of five stars."),
            ("The Stranger", "A masked stranger waits beneath the altar. He knows about your mark. He also knows your mother's name."),
            ("The First Shard", "Beneath the chapel lies a crystal fragment. It does not glow. It remembers."),
            ("The Crown's Lie", "The stranger tells you the kingdom did not lose the Crystal Shards. The kingdom has been hiding them."),
            ("The Hollow Knight", "A knight without a face guards the road north. His armour bears the same symbol as your mark."),
        ],
        "choice_prompts": [
            "Trust the stranger's warning or demand the truth.",
            "Take the shard for yourself or leave it where it was found.",
        ],
    },
    2: {
        "title": "The Green That Remains",
        "subtitle": "The forest is dying, but it has not forgotten how to fight.",
        "scenes": [
            ("The Briar March", "The road into the western forest changes when you stop looking at it. Trees lean closer. Paths move."),
            ("The Warden", "A masked warden mistakes you for a Crown hunter and draws a bow before hearing the shard hum."),
            ("The Root-City", "Deep beneath the forest stands a city grown from living wood. Its people have not seen sunlight in twenty years."),
            ("The Beast's Memory", "A wounded stag leads you to a clearing where the same five-star symbol has been carved into stone."),
            ("The Green Heart", "The forest's ancient spirit offers a bargain: restore one life, or restore one piece of the land."),
            ("The Hunt", "Crown soldiers arrive before you can answer. Someone betrayed the location of the Root-City."),
            ("The Burning Grove", "You must decide whether to save the people, the forest, or the shard hidden beneath both."),
        ],
        "choice_prompts": [
            "Protect the Root-City or chase the Crown commander.",
            "Accept the forest's bargain or refuse to trade one life for another.",
        ],
    },
    3: {
        "title": "The City Without a King",
        "subtitle": "Every throne is built from promises. Some are made of bones.",
        "scenes": [
            ("Veyr", "The capital rises beyond the plains, its towers shining while the streets below starve."),
            ("The Masked Court", "Every noble wears a mask. The palace insists it is tradition. Nobody laughs at the explanation."),
            ("The Archive", "An imprisoned historian reveals that Malachar's name was erased from royal records exactly one hundred years ago."),
            ("The Empty Throne", "There is no king in the throne room. There has not been one for twelve years."),
            ("The Regent", "The Regent claims the Shards must remain hidden because their power caused the old catastrophe."),
            ("The Prisoner", "In the palace dungeons you find a man who looks exactly like the figure from your dreams."),
            ("The First Truth", "He says Malachar did not shatter the Shards to destroy Eldoria. He shattered them to stop something from entering it."),
            ("The Night of Masks", "The capital erupts into rebellion. Every faction wants you, and every faction claims to be saving the kingdom."),
        ],
        "choice_prompts": [
            "Expose the Regent's secret or use it to gain access to the royal vault.",
            "Free the prisoner or leave him to the Crown.",
        ],
    },
    4: {
        "title": "The Sea of Glass",
        "subtitle": "Beyond the kingdom lies the wound where the world broke.",
        "scenes": [
            ("The Glass Coast", "The sea has become a field of transparent stone. Beneath it, ships drift frozen in impossible poses."),
            ("The Lighthouse Keeper", "An old keeper has spent forty years lighting a lamp for ships that no longer exist."),
            ("The Drowned Library", "A submerged library contains records from before the Shattering. One book has your name in it."),
            ("The Sixth Name", "The prophecy was altered. The original text names six souls, not one."),
            ("The Sleeping Door", "A door stands upright in the middle of the Glass Sea. There is no wall around it."),
            ("Malachar's Echo", "The sorcerer's echo appears beside the door. He does not ask you to save him. He asks you to stop him."),
            ("The Choice Beneath the Tide", "You discover that each restored Shard strengthens the barrier — but also wakes the thing behind it."),
        ],
        "choice_prompts": [
            "Restore the Shard immediately or hide it until you know more.",
            "Believe Malachar's warning or believe the prophecy.",
        ],
    },
    5: {
        "title": "The Shattered Crown",
        "subtitle": "The final battle is not about who wins. It is about what survives.",
        "scenes": [
            ("The Black Spire", "The final road climbs through a storm that falls upward. Lightning crawls from the ground into the clouds."),
            ("The Five Chambers", "Each Shard tests a different part of you: courage, mercy, truth, sacrifice, and ambition."),
            ("The Forgotten Sixth", "A hidden chamber reveals the Sixth Shard — not a crystal, but a piece of living memory."),
            ("Malachar", "The sorcerer waits at the summit, older than any human should be and terrified of the thing beyond the door."),
            ("The Crown Arrives", "The Regent arrives with the royal army. He has never wanted the kingdom. He wants the door."),
            ("The Breaking Point", "The five Shards begin to resonate. The barrier cracks. Every decision you made echoes through the chamber."),
            ("The Last Question", "Malachar offers you the only choice he believes matters: preserve Eldoria as it is, or destroy the old world so something better can grow."),
        ],
        "choice_prompts": [
            "Trust Malachar or turn against him.",
            "Use the Shards to seal the door, open it, or destroy the Shards forever.",
        ],
    },
}

SIDE_QUESTS = [
    {
        "id": "bells",
        "title": "The Bells That Wouldn't Stop",
        "giver": "Mira the Bellkeeper",
        "text": "Every midnight the abandoned bell tower rings by itself. Mira believes the bells are warning the dead.",
        "steps": [
            "Climb the ruined tower.",
            "Find the bell rope beneath the floorboards.",
            "Discover the names carved into the bell.",
            "Choose whether to silence the bell or let it finish its final warning.",
        ],
        "reward": "A hidden route into the capital and +2 reputation.",
    },
    {
        "id": "wolves",
        "title": "The Wolf at the Door",
        "giver": "Kael",
        "text": "A wounded wolf follows the party for three days. It carries a Crown seal around its neck.",
        "steps": [
            "Treat the wolf instead of chasing it away.",
            "Follow its tracks into the northern ravine.",
            "Find the abandoned Crown camp.",
            "Return the seal to the wolf's pack.",
        ],
        "reward": "A Beastcaller bonus and a permanent companion dialogue.",
    },
    {
        "id": "lantern",
        "title": "The Last Lantern",
        "giver": "Elder Mara",
        "text": "A village keeps one lantern burning for people who vanished during the Shattering.",
        "steps": [
            "Carry the lantern through the Ashen Road.",
            "Find the names of the missing.",
            "Light the abandoned shrine.",
            "Return before sunrise.",
        ],
        "reward": "A healing relic and +3 reputation.",
    },
    {
        "id": "merchant",
        "title": "A Debt in Red Ink",
        "giver": "Tomas the Merchant",
        "text": "A merchant claims the Crown seized his shop because of a debt he never owed.",
        "steps": [
            "Find the original ledger.",
            "Question the Crown clerk.",
            "Decide whether to expose the clerk or accept a bribe.",
            "Return the ledger to Tomas.",
        ],
        "reward": "Discounts at every friendly merchant.",
    },
    {
        "id": "mirror",
        "title": "The Mirror Room",
        "giver": "The Stranger",
        "text": "A room beneath Greyhaven contains a mirror that reflects a version of Eldoria where the Shattering never happened.",
        "steps": [
            "Enter the mirror room.",
            "Speak to the person who looks like you.",
            "Resist the temptation to remain.",
            "Break the mirror or preserve it.",
        ],
        "reward": "Unlocks a hidden dialogue in Act V.",
    },
    {
        "id": "ashes",
        "title": "Ashes Remember",
        "giver": "The Hollow Knight",
        "text": "A faceless knight asks you to recover the sword of a soldier whose name has been erased.",
        "steps": [
            "Search the old battlefield.",
            "Read the surviving soldiers' letters.",
            "Recover the broken sword.",
            "Speak the forgotten name aloud.",
        ],
        "reward": "Knight-exclusive upgrade and +1 defence.",
    },
    {
        "id": "star",
        "title": "A Star Below the Earth",
        "giver": "Lyra",
        "text": "Lyra has seen a star beneath the ground and refuses to explain how that is possible.",
        "steps": [
            "Follow the underground river.",
            "Solve the three constellation doors.",
            "Recover the fallen star.",
            "Return it to the night sky.",
        ],
        "reward": "A powerful magic upgrade and +20 maximum MP.",
    },
    {
        "id": "sixth",
        "title": "The Sixth Memory",
        "giver": "Malachar's Echo",
        "text": "Something remembers the world before Eldoria existed. It wants you to remember too.",
        "steps": [
            "Collect five memory fragments.",
            "Refuse three false memories.",
            "Enter the chamber beyond the Sixth Shard.",
            "Choose what history should remember.",
        ],
        "reward": "Unlocks the secret ending.",
    },
]

COMPANION_STORIES = {
    "Seraphine": [
        "Seraphine admits that Ashenveil was not destroyed by Malachar. The Crown ordered the evacuation and locked the gates.",
        "She has spent ten years believing she was the only survivor. Then she sees the Ashenveil crest on your sword.",
        "Her final loyalty quest asks whether vengeance is worth becoming the thing she hates.",
    ],
    "Elder Mara": [
        "Mara remembers the first day the sky went dark. She was a child, but she remembers a second moon.",
        "She reveals that the healers were ordered to erase memories of the Shattering from survivors.",
        "Her final quest is about forgiving someone who never asked to be forgiven.",
    ],
    "Kael": [
        "Kael once served the Crown as an information runner. He knows every secret road into the capital.",
        "He insists he never killed anyone for the Crown. He does not say whether that is the same as being innocent.",
        "His loyalty quest forces him to confront the person who recruited him.",
    ],
    "Lyra": [
        "Lyra believes the stars are memories left behind by dead worlds.",
        "She discovers that one star has been following your journey since Greyhaven.",
        "Her final quest reveals why your mark responds to magic.",
    ],
}

ENDING_TEXT = {
    "crown": [
        "You raise the restored Shards and the Black Spire bends around their light.",
        "The Crown's army falls silent. The door closes.",
        "Eldoria survives, but the old kingdom does not.",
        "You become the first ruler in a century who knows exactly what the throne cost.",
    ],
    "mercy": [
        "You lower your weapon when every voice around you demands blood.",
        "Malachar finally remembers how to cry.",
        "The barrier seals without consuming him.",
        "Years later, people still argue whether mercy saved Eldoria or merely delayed its judgement.",
    ],
    "alliance": [
        "The Crown, the rebels, the forest wardens and Malachar stand together for one impossible moment.",
        "The door closes because nobody tries to claim what lies beyond it.",
        "Eldoria enters an age without a single ruler.",
        "For the first time, the people decide what their future means.",
    ],
    "destroy": [
        "You destroy the Shards.",
        "The magic holding the old world together vanishes like a breath in winter.",
        "The kingdom loses its miracles, its curses and its excuses.",
        "What grows afterward is smaller, harder and entirely human.",
    ],
    "secret": [
        "You remember the Sixth Shard.",
        "It was never a source of power. It was a memory of every world that came before this one.",
        "You refuse the roles written for you by prophecy, Crown and sorcerer alike.",
        "Instead of saving the old world or opening the new one, you rewrite the boundary between them.",
        "The next morning, children are born who have never heard of Malachar.",
        "Somewhere beyond the mountains, a sixth star appears.",
    ],
}


def act_scene_lines(act_number):
    """Return the narrative scenes for an act."""
    return list(ACTS[act_number]["scenes"])


def side_quest(quest_id):
    for quest in SIDE_QUESTS:
        if quest["id"] == quest_id:
            return quest
    return None


def companion_story(name):
    return list(COMPANION_STORIES.get(name, []))


def ending_lines(ending):
    return list(ENDING_TEXT.get(ending, ENDING_TEXT["crown"]))
