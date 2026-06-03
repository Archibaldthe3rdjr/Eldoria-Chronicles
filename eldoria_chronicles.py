import time
import os
import random

# ─────────────────────────────────────────────
#  Utility
# ─────────────────────────────────────────────

def slow_type(text, delay=0.04):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=1.0):
    time.sleep(sec)

def divider():
    print("\n" + "═" * 50 + "\n")

def get_choice(prompt, options):
    while True:
        if prompt:
            slow_type(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        choice = input("\n> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        slow_type("Please enter a valid number.")

def typewriter_pause(text, delay=0.04, after=0.8):
    slow_type(text, delay)
    pause(after)

# ─────────────────────────────────────────────
#  THE WORLD OF ELDORIA — Lore
# ─────────────────────────────────────────────
#
#  Long ago the realm of Eldoria was governed by five
#  Crystal Shards — ancient relics that kept peace and
#  held back the Void. An immortal sorcerer named Malachar
#  shattered them, unleashing the Void Tide across the land.
#  Villages fell. Kings wept. The gods went silent.
#
#  A prophecy survived, carved into the Throne of Ashes:
#  "When darkness swallows the five flames, one soul from
#   the dust shall rise — and either save the world, or
#   become its end."
#
#  That soul is you.
#
# ─────────────────────────────────────────────

LORE_INTRO = [
    "In the beginning, there was light.",
    "Five Crystal Shards — each holding a fragment of\ncreation — floated above the realm of Eldoria.",
    "They gave warmth to the fields of Greenhollow,\nstrength to the warriors of Ironpeak,\nwisdom to the mages of the Arcane Spire,\nand hope to every soul beneath the sky.",
    "Then came Malachar.",
    "Once the greatest sorcerer who ever lived.\nNow something far older. Far darker.",
    "He shattered the Shards in a single night.\nThe sky turned black. The oceans boiled.\nThe gods... fell silent.",
    "That was one hundred years ago.",
    "You were born into the ash.",
    "You have nothing — no army, no crown, no power.\nOnly a name. And a prophecy that will not let you rest.",
    "The Throne of Ashes speaks:\n'One soul from the dust shall rise —\n and either save the world, or become its end.'",
    "That soul is you.",
    "The question is: what kind of soul are you?",
]

# ─────────────────────────────────────────────
#  Character Classes
# ─────────────────────────────────────────────

CLASSES = {
    "Knight of Ashenveil": {
        "description": "A battle-hardened warrior sworn to protect the weak. High HP and defence.",
        "hp": 140, "mp": 30, "attack": 22, "defence": 12, "magic": 5,
        "skill": "Rallying Cry",
        "skill_desc": "Restores 25 HP and increases attack by 5 for 3 rounds.",
        "lore": "The Knights of Ashenveil were once Eldoria's greatest guard. You are the last.",
    },
    "Shadowblade": {
        "description": "A rogue who strikes from darkness. High attack, low defence.",
        "hp": 100, "mp": 50, "attack": 35, "defence": 6, "magic": 10,
        "skill": "Void Step",
        "skill_desc": "Teleport behind the enemy — guaranteed critical hit dealing 4x damage.",
        "lore": "You learned to survive in the gutters of Malachar's empire. Shadows are your home.",
    },
    "Arcanist": {
        "description": "A spellweaver wielding forbidden magic. High magic damage, fragile.",
        "hp": 85, "mp": 120, "attack": 12, "defence": 4, "magic": 45,
        "skill": "Starfall",
        "skill_desc": "Summons meteors dealing 60 magic damage. Costs 30 MP.",
        "lore": "You survived the burning of the Arcane Spire. Magic flows through your blood like grief.",
    },
    "Warden of the Wild": {
        "description": "A nature guardian bonded to beasts. Balanced stats with healing ability.",
        "hp": 115, "mp": 80, "attack": 18, "defence": 9, "magic": 20,
        "skill": "Nature's Wrath",
        "skill_desc": "Summons roots to bind the enemy (stun 2 turns) and deals 25 damage.",
        "lore": "The forests of Eldoria still live. You speak for them.",
    },
}

def pick_class():
    divider()
    slow_type("Before your journey begins — who are you?\n")
    names = list(CLASSES.keys())
    for i, name in enumerate(names, 1):
        c = CLASSES[name]
        print(f"  {i}. {name}")
        print(f"       {c['description']}")
        print(f"       HP:{c['hp']}  MP:{c['mp']}  ATK:{c['attack']}  DEF:{c['defence']}  MAG:{c['magic']}")
        print(f"       Skill: {c['skill']} — {c['skill_desc']}")
        print()
    choice = get_choice("", names)
    chosen = names[choice - 1]
    return chosen, dict(CLASSES[chosen])

# ─────────────────────────────────────────────
#  Player
# ─────────────────────────────────────────────

class Player:
    def __init__(self, name, cls_name, stats):
        self.name = name
        self.cls = cls_name
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.mp = stats["mp"]
        self.max_mp = stats["mp"]
        self.attack = stats["attack"]
        self.base_attack = stats["attack"]
        self.defence = stats["defence"]
        self.magic = stats["magic"]
        self.skill = stats["skill"]
        self.skill_desc = stats["skill_desc"]
        self.lore = stats["lore"]
        self.skill_used = False
        self.stunned = False
        self.attack_boost = 0
        self.attack_boost_rounds = 0
        self.shards = 0  # Crystal Shards collected
        self.inventory = []
        self.level = 1
        self.xp = 0
        self.xp_needed = 50

    def is_alive(self):
        return self.hp > 0

    def gain_xp(self, amount):
        self.xp += amount
        slow_type(f"  [+{amount} XP — Total: {self.xp}/{self.xp_needed}]")
        if self.xp >= self.xp_needed:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp = self.xp - self.xp_needed
        self.xp_needed = int(self.xp_needed * 1.6)
        hp_gain = random.randint(10, 20)
        atk_gain = random.randint(2, 5)
        self.max_hp += hp_gain
        self.hp = min(self.hp + hp_gain, self.max_hp)
        self.attack += atk_gain
        self.base_attack = self.attack
        divider()
        slow_type(f"✨ LEVEL UP! You are now Level {self.level}!")
        slow_type(f"  HP +{hp_gain}  |  Attack +{atk_gain}")
        pause()

    def heal(self, amount):
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def status(self):
        print(f"\n  {self.name} | {self.cls} | Lv.{self.level}")
        print(f"  HP: {self.hp}/{self.max_hp}  MP: {self.mp}/{self.max_mp}")
        print(f"  ATK: {self.attack}  DEF: {self.defence}  MAG: {self.magic}")
        print(f"  Shards: {self.shards}/5  XP: {self.xp}/{self.xp_needed}")
        if self.inventory:
            print(f"  Inventory: {', '.join(self.inventory)}")
        print()

# ─────────────────────────────────────────────
#  Enemy
# ─────────────────────────────────────────────

class Enemy:
    def __init__(self, name, hp, attack, defence, xp_reward, lore=""):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.xp_reward = xp_reward
        self.lore = lore
        self.stunned = False
        self.stun_turns = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg - self.defence)
        self.hp = max(0, self.hp - actual)
        return actual

    def ai_attack(self, player):
        if self.stunned:
            self.stun_turns -= 1
            if self.stun_turns <= 0:
                self.stunned = False
            slow_type(f"  {self.name} is stunned and cannot act!")
            return

        roll = random.random()
        if roll < 0.2:
            dmg = int(self.attack * 1.8) + random.randint(0, 8)
            actual = max(1, dmg - player.defence)
            player.hp = max(0, player.hp - actual)
            slow_type(f"  {self.name} unleashes a HEAVY STRIKE for {actual} damage!")
        elif roll < 0.35 and player.hp < player.max_hp * 0.4:
            dmg = self.attack + random.randint(5, 15)
            actual = max(1, dmg - player.defence)
            player.hp = max(0, player.hp - actual)
            slow_type(f"  {self.name} senses weakness and lunges — {actual} damage!")
        else:
            dmg = self.attack + random.randint(-4, 4)
            actual = max(1, dmg - player.defence)
            player.hp = max(0, player.hp - actual)
            slow_type(f"  {self.name} attacks for {actual} damage!")

# ─────────────────────────────────────────────
#  Combat Engine
# ─────────────────────────────────────────────

def use_item(player, enemy):
    usable = [i for i in player.inventory if i in ["Health Potion", "Ether Vial", "Smoke Bomb"]]
    if not usable:
        slow_type("  You have no usable items!")
        return False
    choice = get_choice("Use which item?", usable + ["Cancel"])
    if choice == len(usable) + 1:
        return False
    item = usable[choice - 1]
    if item == "Health Potion":
        healed = player.heal(50)
        slow_type(f"  You drink a Health Potion and recover {healed} HP!")
        player.inventory.remove(item)
    elif item == "Ether Vial":
        gain = min(40, player.max_mp - player.mp)
        player.mp += gain
        slow_type(f"  You drink an Ether Vial and recover {gain} MP!")
        player.inventory.remove(item)
    elif item == "Smoke Bomb":
        slow_type("  You throw a Smoke Bomb and escape the battle!")
        player.inventory.remove(item)
        return "fled"
    return True

def player_turn(player, enemy):
    actions = ["Basic Attack"]
    mp_cost = 0
    if player.cls == "Arcanist":
        mp_cost = 30
        actions.append(f"Skill: {player.skill} (costs {mp_cost} MP)")
    else:
        actions.append(f"Skill: {player.skill}")
    actions += ["Use Item", "Check Status", "Flee (50% chance)"]

    choice = get_choice(f"\n{player.name}'s turn:", actions)

    if choice == 1:
        dmg = player.attack + random.randint(-4, 6)
        dealt = enemy.take_damage(dmg)
        slow_type(f"  {player.name} attacks {enemy.name} for {dealt} damage! ({enemy.name} HP: {enemy.hp})")

    elif choice == 2:
        # Skill
        if player.cls == "Knight of Ashenveil":
            healed = player.heal(25)
            player.attack += 5
            player.attack_boost = 5
            player.attack_boost_rounds = 3
            slow_type(f"  {player.name} raises a Rallying Cry! Healed {healed} HP, Attack +5 for 3 rounds!")
        elif player.cls == "Shadowblade":
            dmg = player.attack * 4
            dealt = enemy.take_damage(dmg)
            slow_type(f"  {player.name} uses Void Step — critical hit for {dealt} damage!")
        elif player.cls == "Arcanist":
            if player.mp < mp_cost:
                slow_type(f"  Not enough MP! ({player.mp}/{mp_cost} needed)")
                return player_turn(player, enemy)
            player.mp -= mp_cost
            dealt = enemy.take_damage(player.magic + 20)
            slow_type(f"  {player.name} calls down Starfall! {dealt} magic damage!")
        elif player.cls == "Warden of the Wild":
            dealt = enemy.take_damage(25)
            enemy.stunned = True
            enemy.stun_turns = 2
            slow_type(f"  {player.name} summons Nature's Wrath! {dealt} damage — {enemy.name} is rooted for 2 turns!")

    elif choice == 3:
        result = use_item(player, enemy)
        if result == "fled":
            return "fled"
        if not result:
            return player_turn(player, enemy)

    elif choice == 4:
        player.status()
        return player_turn(player, enemy)

    elif choice == 5:
        if random.random() < 0.5:
            slow_type("  You successfully fled!")
            return "fled"
        else:
            slow_type("  You couldn't escape!")

    # Tick attack boost
    if player.attack_boost_rounds > 0:
        player.attack_boost_rounds -= 1
        if player.attack_boost_rounds == 0:
            player.attack -= player.attack_boost
            player.attack_boost = 0
            slow_type("  Your attack boost fades.")

    return None

def combat(player, enemy):
    divider()
    if enemy.lore:
        slow_type(f"  {enemy.lore}")
        pause(0.5)
    slow_type(f"⚔  {enemy.name} stands before you!")
    slow_type(f"   HP: {enemy.hp}  ATK: {enemy.attack}  DEF: {enemy.defence}")
    pause()

    round_num = 1
    while player.is_alive() and enemy.is_alive():
        slow_type(f"\n--- Round {round_num} | Your HP: {player.hp}/{player.max_hp} ---")

        if player.stunned:
            slow_type(f"  {player.name} is stunned!")
            player.stunned = False
        else:
            result = player_turn(player, enemy)
            if result == "fled":
                return "fled"

        if enemy.is_alive():
            enemy.ai_attack(player)

        round_num += 1

    if player.is_alive():
        slow_type(f"\n✅  You defeated {enemy.name}!")
        player.gain_xp(enemy.xp_reward)
        return "win"
    else:
        return "lose"

# ─────────────────────────────────────────────
#  THE FIVE ACTS
# ─────────────────────────────────────────────

# ── ACT I: The Village of Ashfall ─────────────

def act_one(player):
    divider()
    slow_type("ACT I — THE VILLAGE OF ASHFALL")
    pause()
    typewriter_pause("You open your eyes to smoke and silence.")
    typewriter_pause("The village of Ashfall — where you were born — is burning.")
    typewriter_pause("Void Wraiths circle overhead. Villagers scatter.")
    typewriter_pause("An old woman grabs your arm. It is Elder Mara.")
    pause()
    slow_type('[Elder Mara]: "You — the prophecy child. I always knew this day would come."')
    slow_type('[Elder Mara]: "The first Shard is hidden beneath the old temple. You must claim it."')
    slow_type('[Elder Mara]: "But the Wraith Commander has already breached the gates. Go — now!"')
    pause()

    choice = get_choice("\nWhat do you do?", [
        "Rush to the temple immediately",
        "Help the villagers first",
        "Ask Elder Mara for more information",
    ])

    if choice == 1:
        typewriter_pause("You sprint through burning streets toward the temple.")
    elif choice == 2:
        typewriter_pause("You help villagers escape — they hand you a Health Potion in gratitude.")
        player.inventory.append("Health Potion")
        slow_type("  [Item acquired: Health Potion]")
        pause()
        typewriter_pause("Then you rush to the temple.")
    elif choice == 3:
        slow_type('[Elder Mara]: "Malachar shattered the five Shards one hundred years ago.')
        slow_type('  Each Shard is guarded by one of his Void Lords.')
        slow_type('  Collect all five and you can reforge the Crystal Crown — the only thing')
        slow_type('  that can end Malachar.')
        slow_type('  But beware — each Shard you claim, he will feel it."')
        pause()
        typewriter_pause("Wiser now, you rush to the temple.")

    divider()
    typewriter_pause("The temple is ancient — stone cracked by a century of void energy.")
    typewriter_pause("You descend into the crypt. In the darkness, something stirs.")
    pause()

    wraith_cmd = Enemy(
        name="Void Wraith Commander",
        hp=70, attack=14, defence=4, xp_reward=40,
        lore="A Wraith Commander — Malachar's foot soldier, towering and wreathed in smoke."
    )
    result = combat(player, wraith_cmd)
    if result == "lose":
        return "lose"

    divider()
    typewriter_pause("At the base of the crypt, a faint blue glow pulses in the darkness.")
    typewriter_pause("You reach out and touch it. Cold. Ancient. Alive.")
    typewriter_pause("The First Crystal Shard hums in your hand.")
    player.shards += 1
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("A voice echoes through the stone — Malachar's voice.")
    slow_type('  [Malachar]: "...Interesting. So the prophecy begins. Come, little dust-child."')
    slow_type('  [Malachar]: "I have been waiting a hundred years. I can wait a little longer."')
    pause()
    return "act_two"

# ── ACT II: The Iron City ─────────────────────

def act_two(player):
    divider()
    slow_type("ACT II — THE IRON CITY OF DUSKMAR")
    pause()
    typewriter_pause("You travel north to Duskmar — the last great city still standing.")
    typewriter_pause("Its walls are iron. Its people are tired. And its king has made a deal with Malachar.")
    pause()
    slow_type("  A guard stops you at the gate.")
    slow_type('  [Guard]: "State your business, traveller."')
    pause()

    choice = get_choice("How do you enter?", [
        "Tell the truth — you seek the Second Shard",
        "Claim to be a merchant",
        "Sneak through a side passage you spotted",
    ])

    if choice == 1:
        slow_type('  [Guard]: "The Shard?! You\'re one of THEM. Seize them!"')
        typewriter_pause("Two city guards attack!")
        g1 = Enemy("City Guard", hp=50, attack=12, defence=6, xp_reward=20)
        r = combat(player, g1)
        if r == "lose": return "lose"
        typewriter_pause("You enter the city — wanted, but inside.")
    elif choice == 2:
        slow_type('  [Guard]: "Move along then." He waves you through.')
        typewriter_pause("You slip into Duskmar unnoticed.")
    elif choice == 3:
        if random.random() < 0.65:
            typewriter_pause("You find a crumbling aqueduct passage and slip inside.")
            slow_type("  [You found a hidden Health Potion in the passage!]")
            player.inventory.append("Health Potion")
        else:
            typewriter_pause("A patrol spots you!")
            g1 = Enemy("City Patrol", hp=45, attack=13, defence=5, xp_reward=20)
            r = combat(player, g1)
            if r == "lose": return "lose"

    divider()
    typewriter_pause("Deep in Duskmar's undercity, you find a rebel hideout.")
    slow_type("  A scarred woman steps forward. Her name is Seraphine — former general of Eldoria.")
    pause()
    slow_type('  [Seraphine]: "I\'ve heard the whispers. You\'re the one the prophecy speaks of."')
    slow_type('  [Seraphine]: "The Second Shard is in the king\'s vault. I can get you inside."')
    slow_type('  [Seraphine]: "But the king\'s champion — the Iron Golem — guards it night and day."')
    pause()

    choice = get_choice("What do you say?", [
        "Accept Seraphine's help",
        "Go alone — you don't trust her yet",
    ])

    if choice == 1:
        typewriter_pause("Seraphine leads you through servant tunnels into the vault.")
        slow_type("  [Seraphine hands you an Ether Vial.]")
        player.inventory.append("Ether Vial")
    else:
        typewriter_pause("You find another way in — slower, but yours.")

    divider()
    typewriter_pause("The vault doors grind open. Inside, the Second Shard glows amber.")
    typewriter_pause("Then the floor shakes. Stone grinds. The Iron Golem awakens.")

    golem = Enemy(
        name="Iron Golem",
        hp=110, attack=18, defence=14, xp_reward=65,
        lore="A hulking construct of iron and void energy. It was built to never tire, never flinch, never fall."
    )
    result = combat(player, golem)
    if result == "lose": return "lose"

    divider()
    typewriter_pause("The Golem crumbles. The Shard is yours.")
    player.shards += 1
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("The king flees. Seraphine's rebels take the city.")
    slow_type('  [Seraphine]: "One step closer. The third Shard is said to be in the Sunken Ruins.')
    slow_type('  Far east. Past the Ashwood. And {player.name}... Malachar will send something worse now."')
    pause()
    return "act_three"

# ── ACT III: The Sunken Ruins ─────────────────

def act_three(player):
    divider()
    slow_type("ACT III — THE SUNKEN RUINS OF VAEL'SHAR")
    pause()
    typewriter_pause("The Ashwood is a dead forest. Black trees. Grey sky. No birdsong.")
    typewriter_pause("Halfway through, you are ambushed.")
    pause()

    bandit = Enemy("Void-Touched Bandit", hp=80, attack=17, defence=7, xp_reward=45,
                   lore="A man consumed by void energy — hollow-eyed, desperate, dangerous.")
    r = combat(player, bandit)
    if r == "lose": return "lose"

    divider()
    typewriter_pause("Beyond the Ashwood, the earth dips into ruins half-swallowed by dark water.")
    typewriter_pause("You wade in. The ruins speak to you — memories not your own flood your mind.")
    typewriter_pause("This was a temple of the old gods. Before Malachar silenced them.")
    pause()

    slow_type("  A spirit appears — translucent, ancient, sorrowful.")
    slow_type('  [Spirit of Vael\'shar]: "Child of prophecy. To claim the Shard you must prove your worth."')
    slow_type('  [Spirit]: "Answer me true: Why do you seek the Shards?"')
    pause()

    choice = get_choice("Why do you truly seek the Shards?", [
        "To save Eldoria and its people.",
        "For power — I want the strength Malachar has.",
        "Because I have no choice. The prophecy chose me.",
        "To end Malachar — for the people he took from me.",
    ])

    if choice == 1:
        slow_type('  [Spirit]: "Noble. The world needs more like you. Take the Shard — and my blessing."')
        player.defence += 3
        slow_type("  [Your defence permanently increased by 3!]")
    elif choice == 2:
        slow_type('  [Spirit]: "Honest, and dangerous. Power corrupts, child. Use it wisely."')
        player.attack += 4
        slow_type("  [Your attack permanently increased by 4!]")
    elif choice == 3:
        slow_type('  [Spirit]: "The reluctant hero. History\'s most common kind — and often the greatest."')
        player.max_hp += 20
        player.hp = min(player.hp + 20, player.max_hp)
        slow_type("  [Your max HP permanently increased by 20!]")
    elif choice == 4:
        slow_type('  [Spirit]: "Grief is a powerful fire. Let it forge you — do not let it consume you."')
        player.magic += 8
        slow_type("  [Your magic permanently increased by 8!]")

    pause()
    typewriter_pause("The spirit fades. At the heart of the ruins, the Third Shard rests on a sunken altar.")
    typewriter_pause("But as you reach for it — a Void Serpent erupts from the water.")

    serpent = Enemy(
        name="Void Serpent",
        hp=95, attack=20, defence=6, xp_reward=60,
        lore="An ancient creature warped by void energy — scales like obsidian, eyes like dying stars."
    )
    r = combat(player, serpent)
    if r == "lose": return "lose"

    divider()
    player.shards += 1
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    typewriter_pause("Three down. Two remain. The sky above Eldoria grows darker.")
    pause()
    return "act_four"

# ── ACT IV: The Arcane Spire ──────────────────

def act_four(player):
    divider()
    slow_type("ACT IV — THE ARCANE SPIRE")
    pause()
    typewriter_pause("The Arcane Spire rises from a mountaintop like a broken tooth.")
    typewriter_pause("Once the greatest school of magic in Eldoria. Now Malachar's tower.")
    typewriter_pause("His Void Lords command it. His experiments happen within its walls.")
    pause()
    typewriter_pause("You climb for two days. At the summit gate, a Void Lord waits.")
    pause()

    lord_one = Enemy(
        name="Void Lord Vareth",
        hp=130, attack=22, defence=10, xp_reward=90,
        lore="Lord Vareth — Malachar's second-in-command. Tall, cold, and utterly merciless."
    )
    r = combat(player, lord_one)
    if r == "lose": return "lose"

    divider()
    slow_type('  [Vareth, dying]: "You... you don\'t understand what Malachar truly is.')
    slow_type('  He isn\'t trying to destroy Eldoria. He is trying to... save it."')
    slow_type('  [Vareth]: "From something... far worse... than him..."')
    typewriter_pause("He goes still. The gate opens.")
    pause()

    choice = get_choice("Vareth's words linger. What do you do?", [
        "Push forward — it's a trick.",
        "Search Vareth's body for answers.",
        "Sit with the doubt. Maybe he's telling the truth.",
    ])

    if choice == 1:
        typewriter_pause("You push forward. Doubt has no place in a dying world.")
    elif choice == 2:
        typewriter_pause("You find a journal. Malachar's handwriting fills the pages.")
        slow_type("  The last entry reads: 'The Void beyond the Veil grows. If the Shards are reforged wrong,")
        slow_type("  they will open a door that cannot be closed. I shattered them to prevent it.")
        slow_type("  But the child of prophecy changes everything. Perhaps there is still a way.'")
        pause()
        slow_type("  [You found Malachar's Journal — the truth is more complicated than you thought.]")
        player.inventory.append("Malachar's Journal")
    elif choice == 3:
        typewriter_pause("You sit with it. A villain who believes he is saving the world.")
        typewriter_pause("You've heard that before. But something in his eyes wasn't lying.")
        pause()

    divider()
    typewriter_pause("Inside the Spire, the Fourth Shard pulses violet on the top floor.")
    typewriter_pause("As you reach for it — Malachar appears. Not in person. In vision.")
    pause()
    slow_type('  [Malachar]: "Stop."')
    slow_type('  [Malachar]: "You found the journal. Good. Then you know the risk."')
    slow_type('  [Malachar]: "I did not shatter the Shards out of hatred. I shattered them out of fear."')
    slow_type('  [Malachar]: "The Void beyond the Veil is not nothing. It is alive. It is hungry."')
    slow_type('  [Malachar]: "If you reforge the Crystal Crown incorrectly, you will feed it everything."')
    pause()

    choice = get_choice("How do you respond?", [
        '"Then tell me the right way to reforge them."',
        '"I don\'t believe you. This is a manipulation."',
        '"Why didn\'t you just tell someone? Why destroy Eldoria?"',
    ])

    if choice == 1:
        slow_type('  [Malachar]: "...Perhaps you are different from the others. Come to me.')
        slow_type('  Bring the Shards. I will show you the truth at the end of the world."')
    elif choice == 2:
        slow_type('  [Malachar]: "Believe what you wish. But when the door opens — remember this moment."')
    elif choice == 3:
        slow_type('  [Malachar]: "Because I am not... good at trust. I never have been.')
        slow_type('  I made choices in darkness when I should have sought light. I know that now."')
        slow_type('  [His voice cracks — just slightly.]')
        pause()

    typewriter_pause("The vision fades. You take the Fourth Shard.")
    player.shards += 1
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("One remains. The Fifth Shard is in Malachar's throne room.")
    typewriter_pause("At the end of the world.")
    pause()
    return "act_five"

# ── ACT V: The Throne of Ashes ────────────────

def act_five(player):
    divider()
    slow_type("ACT V — THE THRONE OF ASHES")
    pause()
    typewriter_pause("The Throne of Ashes rises at the edge of the known world.")
    typewriter_pause("Where the land ends and the Void begins.")
    typewriter_pause("The sky here is not black. It is nothing. An absence of sky.")
    typewriter_pause("You walk toward it alone.")
    pause()

    slow_type("  Malachar stands at the gate. No guards. No tricks.")
    slow_type("  He looks... older than you imagined. Tired. Sad.")
    pause()
    slow_type('  [Malachar]: "You made it. Four Shards. Almost there."')
    slow_type('  [Malachar]: "Now comes the choice the prophecy never told you about."')
    pause()

    # The choice depends on what the player knows
    has_journal = "Malachar's Journal" in player.inventory

    if has_journal:
        slow_type('  [Malachar]: "You read my journal. Then you know what reforging the Crown risks."')
        slow_type('  [Malachar]: "There is a way to seal the Void permanently — but it requires one life."')
        slow_type('  [Malachar]: "Mine. Or yours."')
        pause()
        choice = get_choice("What do you choose?", [
            "Fight Malachar and take the Fifth Shard by force.",
            "Let Malachar sacrifice himself to seal the Void.",
            "Offer your own life instead.",
            "Find a third way — together.",
        ])
    else:
        slow_type('  [Malachar]: "I could explain everything. But I think... you\'d rather fight."')
        slow_type('  [Malachar]: "And perhaps that is the only language the world understands anymore."')
        pause()
        choice = get_choice("What do you choose?", [
            "Fight Malachar.",
            "Demand answers before you fight.",
            "Lower your weapon. Talk.",
        ])

    divider()

    if choice == 1:
        typewriter_pause("You raise your weapon. Malachar closes his eyes.")
        slow_type('  [Malachar]: "Very well. Let it end this way."')
        pause()

        malachar = Enemy(
            name="Malachar, the Last Sorcerer",
            hp=180, attack=28, defence=12, xp_reward=150,
            lore="He is not a monster. He is a man who made terrible choices for reasons he believed were right. That makes him more dangerous."
        )
        r = combat(player, malachar)
        if r == "lose": return "lose"

        divider()
        typewriter_pause("Malachar falls. The Fifth Shard falls from his robes.")
        player.shards += 1
        slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
        pause()
        typewriter_pause("You hold all five Shards. The Crystal Crown is reforged in your hands.")
        typewriter_pause("You hold it above your head — and bring it down.")
        typewriter_pause("The Void screams. The sky returns. Eldoria breathes again.")
        pause()
        return "ending_victory_blood"

    elif choice == 2 and has_journal:
        typewriter_pause("You lower your weapon.")
        slow_type('  [Malachar]: "...Thank you."')
        slow_type('  [Malachar]: "I was never going to ask. But I hoped."')
        pause()
        typewriter_pause("Malachar takes the Shards. He walks to the edge of the Void.")
        typewriter_pause("He speaks words older than language. Light tears through the darkness.")
        typewriter_pause("The Void shrinks. And then is gone.")
        typewriter_pause("Malachar with it.")
        pause()
        player.shards = 5
        return "ending_redemption"

    elif choice == 3 and has_journal:
        typewriter_pause("Malachar stares at you for a long moment.")
        slow_type('  [Malachar]: "No. Absolutely not."')
        slow_type('  [Malachar]: "You have a future. I lost mine a century ago."')
        pause()
        typewriter_pause("He takes the Shards before you can stop him.")
        typewriter_pause("He walks into the Void. He does not look back.")
        player.shards = 5
        return "ending_redemption"

    else:
        # Talk / demand answers path
        slow_type('  [Malachar]: "The Void beyond the Veil is alive. It waits for the Crown to be reforged.')
        slow_type('  When five Shards unite, a door opens — and what is on the other side makes me')
        slow_type('  look like a summer storm."')
        pause()
        slow_type('  [Malachar]: "I shattered the Shards to keep that door closed. For one hundred years,')
        slow_type('  I have kept it closed. Alone."')
        pause()
        slow_type('  [Malachar]: "But the prophecy says you can seal it permanently. Not just hold it."')
        slow_type('  [Malachar]: "Together, we can end this. But it will cost one of us everything."')
        pause()

        choice2 = get_choice("Your answer:", [
            "Fight him anyway — you can\'t trust him.",
            "Work with him. Seal the Void together.",
        ])

        if choice2 == 1:
            malachar = Enemy(
                name="Malachar, the Last Sorcerer",
                hp=180, attack=28, defence=12, xp_reward=150,
                lore="Even now, he holds back. He does not want to hurt you."
            )
            r = combat(player, malachar)
            if r == "lose": return "lose"
            player.shards = 5
            return "ending_victory_blood"
        else:
            typewriter_pause("You and Malachar stand at the edge of the Void. Together.")
            typewriter_pause("He speaks the sealing words. You pour every Shard's power into the ritual.")
            typewriter_pause("The Void screams. It fights back. It nearly takes you both.")
            typewriter_pause("But it closes.")
            pause()
            player.shards = 5
            return "ending_alliance"

# ─────────────────────────────────────────────
#  Endings
# ─────────────────────────────────────────────

def ending_victory_blood(player):
    divider()
    slow_type("ENDING: THE WARRIOR'S CROWN")
    pause()
    slow_type("You stood alone against the darkness and won.")
    slow_type("Malachar is dead. The Crystal Crown is reforged. Eldoria will heal.")
    slow_type("They will sing songs about you for a thousand years.")
    pause()
    slow_type("But sometimes, in the quiet, you wonder if he was telling the truth.")
    slow_type("And whether the door is truly closed.")
    slow_type("Or just... waiting.")
    divider()
    slow_type(f"  {player.name} the {player.cls} — Level {player.level}")
    slow_type(f"  Shards collected: {player.shards}/5")
    slow_type("  Ending: THE WARRIOR'S CROWN")
    divider()

def ending_redemption(player):
    divider()
    slow_type("ENDING: THE PRICE OF MERCY")
    pause()
    slow_type("You gave a broken man the chance to become something better.")
    slow_type("In his final act, Malachar sealed the Void — and atoned for a century of darkness.")
    slow_type("Eldoria will never know his name was whispered in kindness at the end.")
    slow_type("But you know. And that is enough.")
    divider()
    slow_type(f"  {player.name} the {player.cls} — Level {player.level}")
    slow_type(f"  Shards collected: {player.shards}/5")
    slow_type("  Ending: THE PRICE OF MERCY")
    divider()

def ending_alliance(player):
    divider()
    slow_type("ENDING: THE UNLIKELY ALLIANCE")
    pause()
    slow_type("You chose trust when distrust would have been easier.")
    slow_type("Together, you and Malachar sealed the Void.")
    slow_type("He survived — barely. Changed. Not good, not yet.")
    slow_type("But no longer lost.")
    slow_type("Eldoria begins to rebuild. For the first time in a century,")
    slow_type("the sun rises without shadows.")
    divider()
    slow_type(f"  {player.name} the {player.cls} — Level {player.level}")
    slow_type(f"  Shards collected: {player.shards}/5")
    slow_type("  Ending: THE UNLIKELY ALLIANCE")
    divider()

def ending_lose(player):
    divider()
    slow_type("The darkness takes you.")
    pause()
    slow_type("The Void does not gloat. It simply... absorbs.")
    slow_type(f"  {player.name} the {player.cls} fell before the world could be saved.")
    slow_type("  The story is not over. But your part in it is.")
    divider()

# ─────────────────────────────────────────────
#  Name Entry
# ─────────────────────────────────────────────

def get_name():
    verified = False
    name = ""
    while not verified:
        name = input("\nWhat is your name, traveller? ").strip().capitalize()
        pause(0.4)
        print(f"\n  {name}\n")
        confirm = input("Is that your name? (yes / no): ").strip().lower()
        if confirm in ("yes", "y"):
            verified = True
    return name

# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    slow_type("╔══════════════════════════════════════════════════╗")
    slow_type("║          E L D O R I A   C H R O N I C L E S    ║")
    slow_type("║          A Story of Shards, Shadows & Sacrifice  ║")
    slow_type("╚══════════════════════════════════════════════════╝")
    pause()

    while True:
        mode = get_choice("\nMain Menu", ["New Game", "Quit"])
        if mode == 2:
            slow_type("Until next time, traveller.")
            break

        # Intro
        divider()
        slow_type("PROLOGUE — THE WORLD BEFORE\n")
        for line in LORE_INTRO:
            slow_type(line)
            pause(0.6)

        # Character creation
        name = get_name()
        cls_name, stats = pick_class()
        player = Player(name, cls_name, stats)

        divider()
        slow_type(f'  "{player.lore}"')
        pause()
        slow_type(f"  Your name is {player.name}.")
        slow_type(f"  You are a {player.cls}.")
        slow_type("  And the world is ending.")
        pause(1.5)

        # Run acts
        acts = [act_one, act_two, act_three, act_four, act_five]
        state = None
        for act_fn in acts:
            state = act_fn(player)
            if state == "lose":
                break

        # Endings
        if state == "lose":
            ending_lose(player)
        elif state == "ending_victory_blood":
            ending_victory_blood(player)
        elif state == "ending_redemption":
            ending_redemption(player)
        elif state == "ending_alliance":
            ending_alliance(player)

        again = get_choice("\nPlay again?", ["Yes", "No"])
        if again == 2:
            slow_type("May your next journey be a worthy one. Farewell.")
            break

if __name__ == "__main__":
    main()
