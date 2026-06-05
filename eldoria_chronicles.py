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
#  LORE
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
#  Character Classes (6 total)
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
    "Paladin of the Eternal Flame": {
        "description": "A holy warrior who fights with divine power. Can smite and heal simultaneously.",
        "hp": 130, "mp": 70, "attack": 20, "defence": 11, "magic": 25,
        "skill": "Divine Smite",
        "skill_desc": "Deals 3x magic damage as holy light AND heals yourself for 20 HP.",
        "lore": "The gods are silent — but their fire lives in you. You carry their last ember.",
    },
    "Necromancer": {
        "description": "A dark mage who drains life and raises the fallen. Unique lifesteal mechanic.",
        "hp": 90, "mp": 100, "attack": 15, "defence": 5, "magic": 40,
        "skill": "Soul Drain",
        "skill_desc": "Drains 45 magic damage from enemy and restores half as HP to yourself.",
        "lore": "Death is not an end. You learned that the hard way. Now you use it as a weapon.",
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
        self.shards = 0
        self.inventory = []
        self.gold = 10
        self.level = 1
        self.xp = 0
        self.xp_needed = 50
        self.quests_completed = 0   # track for secret ending
        self.reputation = 0         # rises with kind choices, falls with ruthless ones

    def is_alive(self):
        return self.hp > 0

    def gain_xp(self, amount):
        self.xp += amount
        slow_type(f"  [+{amount} XP — Total: {self.xp}/{self.xp_needed}]")
        if self.xp >= self.xp_needed:
            self.level_up()

    def gain_gold(self, amount):
        self.gold += amount
        slow_type(f"  [+{amount} gold — Total: {self.gold}]")

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
        print(f"  Shards: {self.shards}/5  Gold: {self.gold}  XP: {self.xp}/{self.xp_needed}")
        print(f"  Quests done: {self.quests_completed}  Reputation: {self.reputation}")
        if self.inventory:
            print(f"  Inventory: {', '.join(self.inventory)}")
        print()

# ─────────────────────────────────────────────
#  Enemy
# ─────────────────────────────────────────────

class Enemy:
    def __init__(self, name, hp, attack, defence, xp_reward, gold_drop=0, lore=""):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.xp_reward = xp_reward
        self.gold_drop = gold_drop
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
    usable = [i for i in player.inventory if i in ["Health Potion", "Ether Vial", "Smoke Bomb", "Elixir of Fortitude"]]
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
    elif item == "Elixir of Fortitude":
        healed = player.heal(player.max_hp)
        player.mp = player.max_mp
        slow_type(f"  You drink the Elixir of Fortitude — fully restored!")
        player.inventory.remove(item)
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
            slow_type(f"  {player.name} summons Nature's Wrath! {dealt} damage — {enemy.name} rooted for 2 turns!")
        elif player.cls == "Paladin of the Eternal Flame":
            dealt = enemy.take_damage(player.magic * 3)
            healed = player.heal(20)
            slow_type(f"  {player.name} calls Divine Smite! {dealt} holy damage dealt, {healed} HP restored!")
        elif player.cls == "Necromancer":
            drain = 45
            dealt = enemy.take_damage(drain)
            restore = player.heal(drain // 2)
            slow_type(f"  {player.name} uses Soul Drain! {dealt} damage — absorbed {restore} HP!")

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
        if enemy.gold_drop > 0:
            drop = random.randint(enemy.gold_drop // 2, enemy.gold_drop)
            player.gain_gold(drop)
        return "win"
    else:
        return "lose"

# ─────────────────────────────────────────────
#  Random Travel Encounters
# ─────────────────────────────────────────────

TRAVEL_EVENTS = [
    "abandoned_camp",
    "wounded_traveller",
    "void_ambush",
    "ancient_shrine",
    "merchant_cart",
    "strange_fog",
]

def travel_event(player):
    """Fires randomly between locations — 60% chance."""
    if random.random() > 0.6:
        return
    event = random.choice(TRAVEL_EVENTS)
    divider()

    if event == "abandoned_camp":
        slow_type("You stumble upon an abandoned camp. A fire still smoulders.")
        slow_type("A pack sits by the embers — untouched.")
        choice = get_choice("What do you do?", ["Search the pack", "Leave it alone"])
        if choice == 1:
            roll = random.random()
            if roll < 0.5:
                slow_type("  You find a Health Potion!")
                player.inventory.append("Health Potion")
            elif roll < 0.8:
                gold = random.randint(3, 8)
                player.gain_gold(gold)
                slow_type(f"  You find {gold} gold coins.")
            else:
                slow_type("  A trap! A void sprite lunges from the pack!")
                sprite = Enemy("Void Sprite", hp=35, attack=10, defence=2, xp_reward=15, gold_drop=3)
                combat(player, sprite)

    elif event == "wounded_traveller":
        slow_type("A wounded traveller sits against a tree. He looks up at you — afraid.")
        slow_type('  "Please... don\'t hurt me. I just want to get home."')
        choice = get_choice("What do you do?", ["Give him a Health Potion if you have one", "Give him 5 gold", "Walk past"])
        if choice == 1:
            if "Health Potion" in player.inventory:
                player.inventory.remove("Health Potion")
                slow_type('  [Traveller]: "Gods bless you. Take this — it\'s all I have."')
                player.inventory.append("Smoke Bomb")
                slow_type("  [Item received: Smoke Bomb]")
                player.reputation += 1
            else:
                slow_type("  You have no potion to give. He manages a weak smile anyway.")
        elif choice == 2:
            if player.gold >= 5:
                player.gold -= 5
                slow_type('  [Traveller]: "You\'re a good soul. Here — take my last torch."')
                slow_type("  [+1 Reputation]")
                player.reputation += 1
            else:
                slow_type("  You don't have enough gold.")
        else:
            slow_type("  You walk past. He says nothing. You feel his eyes on your back.")
            player.reputation -= 1

    elif event == "void_ambush":
        slow_type("The air goes cold. The shadows move.")
        slow_type("Two Void Wraiths materialise from the darkness — they saw the Shard's glow.")
        wraith = Enemy("Void Wraith", hp=55, attack=13, defence=3, xp_reward=25, gold_drop=5,
                       lore="Wraiths are drawn to Crystal energy like moths to flame.")
        result = combat(player, wraith)
        if result == "lose":
            return "lose"
        if player.is_alive():
            wraith2 = Enemy("Void Wraith", hp=45, attack=11, defence=3, xp_reward=20, gold_drop=4)
            result = combat(player, wraith2)
            if result == "lose":
                return "lose"

    elif event == "ancient_shrine":
        slow_type("Hidden by vines, an ancient shrine glows faintly.")
        slow_type("The inscription reads: 'Offer gold. Receive blessing.'")
        choice = get_choice("What do you do?", ["Offer 10 gold", "Offer 20 gold", "Take the offering bowl (steal)", "Walk on"])
        if choice == 1 and player.gold >= 10:
            player.gold -= 10
            boost = random.choice(["hp", "atk", "def"])
            if boost == "hp":
                player.max_hp += 15; player.hp = min(player.hp + 15, player.max_hp)
                slow_type("  The shrine glows — your max HP increases by 15!")
            elif boost == "atk":
                player.attack += 3
                slow_type("  The shrine glows — your attack increases by 3!")
            else:
                player.defence += 2
                slow_type("  The shrine glows — your defence increases by 2!")
        elif choice == 2 and player.gold >= 20:
            player.gold -= 20
            player.max_hp += 25; player.hp = min(player.hp + 25, player.max_hp)
            player.attack += 4
            slow_type("  The shrine blazes! Max HP +25 and Attack +4!")
        elif choice == 3:
            gold_found = random.randint(5, 15)
            player.gain_gold(gold_found)
            player.reputation -= 2
            slow_type(f"  You take {gold_found} gold. But something in the air feels... wrong.")
        else:
            slow_type("  You leave the shrine undisturbed. The glow fades as you pass.")

    elif event == "merchant_cart":
        slow_type("A travelling merchant has set up a small cart by the road.")
        slow_type(f'  [Merchant]: "Aye traveller — I\'ve got goods. You\'ve got gold. Let\'s talk."')
        slow_type(f"  Your gold: {player.gold}")
        choice = get_choice("What will you buy?", [
            "Health Potion (8 gold)",
            "Ether Vial (10 gold)",
            "Smoke Bomb (6 gold)",
            "Elixir of Fortitude (25 gold) — fully restores HP and MP",
            "Nothing, move on",
        ])
        prices = [8, 10, 6, 25]
        items = ["Health Potion", "Ether Vial", "Smoke Bomb", "Elixir of Fortitude"]
        if choice <= 4:
            item = items[choice - 1]
            cost = prices[choice - 1]
            if player.gold >= cost:
                player.gold -= cost
                player.inventory.append(item)
                slow_type(f"  You bought a {item}. Gold remaining: {player.gold}")
            else:
                slow_type(f"  You can't afford that. (Need {cost}, have {player.gold})")
        else:
            slow_type("  You move on.")

    elif event == "strange_fog":
        slow_type("A thick silver fog rolls in. You feel dizzy.")
        slow_type("Shapes move in the mist — memories, or visions?")
        slow_type("A voice speaks: 'You are not ready. But you never will be. Go anyway.'")
        pause()
        boost = random.choice(["xp", "heal", "mp"])
        if boost == "xp":
            player.gain_xp(30)
            slow_type("  The fog clears. You feel strangely wiser.")
        elif boost == "heal":
            healed = player.heal(40)
            slow_type(f"  The fog clears. You feel restored — {healed} HP recovered.")
        else:
            gain = min(30, player.max_mp - player.mp)
            player.mp += gain
            slow_type(f"  The fog clears. Your mind feels sharp — {gain} MP restored.")

    return None

# ─────────────────────────────────────────────
#  Shop Between Acts
# ─────────────────────────────────────────────

def visit_shop(player, act_num):
    divider()
    slow_type(f"  Before Act {act_num}, you find a moment to rest and resupply.")
    slow_type(f'  A quiet trader offers her wares. Your gold: {player.gold}')
    pause(0.5)

    shopping = True
    while shopping:
        slow_type("\nWhat will you buy?")
        options = [
            f"Health Potion — 8 gold (restores 50 HP)",
            f"Ether Vial — 10 gold (restores 40 MP)",
            f"Smoke Bomb — 6 gold (flee any battle)",
            f"Elixir of Fortitude — 25 gold (full HP + MP restore)",
            f"Iron Charm — 15 gold (permanently +3 defence)",
            f"War Sigil — 18 gold (permanently +4 attack)",
            f"Leave the shop",
        ]
        prices = [8, 10, 6, 25, 15, 18]
        choice = get_choice(f"Gold: {player.gold}", options)

        if choice == 7:
            slow_type('  [Trader]: "Safe travels."')
            shopping = False
        elif choice <= 4:
            names = ["Health Potion", "Ether Vial", "Smoke Bomb", "Elixir of Fortitude"]
            item = names[choice - 1]
            cost = prices[choice - 1]
            if player.gold >= cost:
                player.gold -= cost
                player.inventory.append(item)
                slow_type(f"  Bought {item}. Gold: {player.gold}")
            else:
                slow_type(f"  Not enough gold. (Need {cost}, have {player.gold})")
        elif choice == 5:
            if player.gold >= 15:
                player.gold -= 15
                player.defence += 3
                slow_type(f"  You equip the Iron Charm. Defence permanently +3! (Now: {player.defence})")
            else:
                slow_type("  Not enough gold.")
        elif choice == 6:
            if player.gold >= 18:
                player.gold -= 18
                player.attack += 4
                player.base_attack = player.attack
                slow_type(f"  You etch the War Sigil into your weapon. Attack permanently +4! (Now: {player.attack})")
            else:
                slow_type("  Not enough gold.")

# ─────────────────────────────────────────────
#  Side Quests
# ─────────────────────────────────────────────

def sidequest_lost_child(player):
    """Act I side quest — find a lost child in the burning village."""
    divider()
    slow_type("SIDE QUEST: The Lost Child")
    slow_type("An elderly man grabs your sleeve. 'My granddaughter — she ran back inside!'")
    slow_type("He points to a burning house. You can hear coughing from within.")
    pause()
    choice = get_choice("What do you do?", [
        "Rush inside to save her",
        "It's too dangerous — keep moving",
    ])
    if choice == 1:
        slow_type("You sprint into the smoke. The heat is overwhelming.")
        slow_type("You find the girl huddled under a table and carry her out.")
        pause()
        slow_type('  [Grandfather]: "I have nothing to give you but this — my father\'s blade."')
        player.attack += 6
        player.base_attack = player.attack
        player.reputation += 2
        player.quests_completed += 1
        slow_type(f"  [Attack permanently +6! Reputation +2]")
    else:
        slow_type("You walk past. The coughing fades. You tell yourself it was the smoke.")
        player.reputation -= 1
    pause()

def sidequest_forgotten_grave(player):
    """Act II side quest — a ghost in Duskmar's undercity."""
    divider()
    slow_type("SIDE QUEST: The Forgotten Grave")
    slow_type("In the undercity, a ghost flickers in the corner of your vision.")
    slow_type('  [Ghost]: "Please... my body was never buried. I cannot rest."')
    slow_type('  [Ghost]: "I am in the old quarry — east of the city. Will you help me?"')
    pause()
    choice = get_choice("Do you help?", [
        "Yes — travel to the quarry",
        "No — you have no time",
    ])
    if choice == 1:
        typewriter_pause("You travel to the quarry. You find bones half-buried in rubble.")
        typewriter_pause("You dig carefully and arrange them properly. You say the old words.")
        slow_type("  The ghost appears one last time — smiling.")
        slow_type('  [Ghost]: "Bless you. Take what I hid nearby."')
        player.inventory.append("Elixir of Fortitude")
        player.reputation += 2
        player.quests_completed += 1
        slow_type("  [Item received: Elixir of Fortitude! Reputation +2]")
        # But first — the quarry has a guardian
        slow_type("\n  A Bone Golem stirs in the rubble. It did not want you here.")
        golem = Enemy("Bone Golem", hp=75, attack=16, defence=8, xp_reward=40, gold_drop=8,
                      lore="Ancient bones animated by residual void energy.")
        result = combat(player, golem)
        if result == "lose":
            return "lose"
    else:
        slow_type("  The ghost fades. The undercity feels colder somehow.")
    pause()
    return None

def sidequest_the_deserter(player):
    """Act III side quest — a Void Lord's former soldier wants out."""
    divider()
    slow_type("SIDE QUEST: The Deserter")
    slow_type("A man in Void Army armour steps out of the trees — hands raised.")
    slow_type('  "Don\'t attack. Please. I deserted. I can\'t do this anymore."')
    slow_type('  "I know where Malachar\'s next patrol will be. I\'ll tell you — if you let me go."')
    pause()
    choice = get_choice("What do you do?", [
        "Let him go — take the information",
        "Bring him to justice",
        "Let him go — no conditions",
    ])
    if choice == 1:
        slow_type("  He tells you the patrol route. You avoid two ambushes.")
        slow_type("  [Defence +2 from tactical advantage — you're better prepared now]")
        player.defence += 2
        player.quests_completed += 1
        player.reputation += 1
    elif choice == 2:
        slow_type("  He fights back desperately.")
        deserter = Enemy("Void Deserter", hp=60, attack=14, defence=5, xp_reward=30, gold_drop=10)
        result = combat(player, deserter)
        if result == "lose":
            return "lose"
        slow_type("  You turned him in. Justice, maybe. But it sits uneasy.")
        player.reputation -= 1
    else:
        slow_type("  He stares at you for a long moment.")
        slow_type('  "...Thank you. Truly."')
        slow_type("  He disappears into the trees. Somewhere, someone gets their father back.")
        player.reputation += 3
        player.quests_completed += 1
        slow_type("  [Reputation +3]")
    pause()
    return None

def sidequest_the_oracle(player):
    """Act IV side quest — an oracle offers a glimpse of truth."""
    divider()
    slow_type("SIDE QUEST: The Oracle of Ironpeak")
    slow_type("Word reaches you of an oracle living in the ruins of Ironpeak's watchtower.")
    slow_type("She has not spoken to anyone in forty years. But she will speak to you.")
    pause()
    choice = get_choice("Do you seek her out?", ["Yes", "No — keep moving"])
    if choice == 2:
        return None
    typewriter_pause("You climb the watchtower. A very old woman sits at the top, eyes closed.")
    slow_type('  [Oracle]: "I have waited for you."')
    slow_type('  [Oracle]: "I will show you one truth. Choose wisely."')
    pause()
    choice = get_choice("What do you ask?", [
        "What is Malachar's greatest weakness?",
        "What is MY greatest weakness?",
        "Is there really a way to save everyone?",
    ])
    if choice == 1:
        slow_type('  [Oracle]: "His grief. He loved this world once. He still does."')
        slow_type('  [Oracle]: "He cannot bring himself to kill the last of the prophecy line."')
        slow_type('  [Oracle]: "Use that. Or don\'t. It is your choice."')
        player.attack += 5
        slow_type("  [Your understanding sharpens — Attack +5]")
    elif choice == 2:
        slow_type('  [Oracle]: "You move too fast. You act before you think."')
        slow_type('  [Oracle]: "One day that will cost you everything."')
        slow_type('  [Oracle]: "But today — knowing it may save you."')
        player.defence += 4
        slow_type("  [Your awareness deepens — Defence +4]")
    else:
        slow_type('  [Oracle]: "Yes. But only if you choose to believe it is possible."')
        slow_type('  [Oracle]: "The world is not saved by the strong. It is saved by the stubborn."')
        player.max_hp += 20
        player.hp = min(player.hp + 20, player.max_hp)
        slow_type("  [Your resolve hardens — Max HP +20]")
    player.quests_completed += 1
    player.reputation += 1
    pause()
    return None

# ─────────────────────────────────────────────
#  THE FIVE ACTS
# ─────────────────────────────────────────────

def act_one(player):
    divider()
    slow_type("ACT I — THE VILLAGE OF ASHFALL")
    pause()
    typewriter_pause("You open your eyes to smoke and silence.")
    typewriter_pause("The village of Ashfall — where you were born — is burning.")
    typewriter_pause("Void Wraiths circle overhead. Villagers scatter.")

    # Side quest opportunity
    sidequest_lost_child(player)

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
        slow_type('  Collect all five and you can reforge the Crystal Crown.')
        slow_type('  But beware — each Shard you claim, he will feel it."')
        pause()
        typewriter_pause("Wiser now, you rush to the temple.")

    # Random travel event
    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    divider()
    typewriter_pause("The temple is ancient — stone cracked by a century of void energy.")
    typewriter_pause("You descend into the crypt. In the darkness, something stirs.")
    pause()

    wraith_cmd = Enemy(
        name="Void Wraith Commander",
        hp=70, attack=14, defence=4, xp_reward=40, gold_drop=8,
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
    player.gain_gold(5)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("A voice echoes through the stone — Malachar's voice.")
    slow_type('  [Malachar]: "...Interesting. So the prophecy begins. Come, little dust-child."')
    slow_type('  [Malachar]: "I have been waiting a century. I can wait a little longer."')
    pause()

    visit_shop(player, act_num=2)
    return "act_two"

def act_two(player):
    divider()
    slow_type("ACT II — THE IRON CITY OF DUSKMAR")
    pause()
    typewriter_pause("You travel north to Duskmar — the last great city still standing.")
    typewriter_pause("Its walls are iron. Its people are tired. Its king has made a deal with Malachar.")

    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

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
        g1 = Enemy("City Guard", hp=50, attack=12, defence=6, xp_reward=20, gold_drop=6)
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
            g1 = Enemy("City Patrol", hp=45, attack=13, defence=5, xp_reward=20, gold_drop=5)
            r = combat(player, g1)
            if r == "lose": return "lose"

    # Side quest in Duskmar
    result = sidequest_forgotten_grave(player)
    if result == "lose" or not player.is_alive():
        return "lose"

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
    typewriter_pause("The vault doors grind open. The Second Shard glows amber.")
    typewriter_pause("Then the floor shakes. The Iron Golem awakens.")

    golem = Enemy(
        name="Iron Golem",
        hp=110, attack=18, defence=14, xp_reward=65, gold_drop=15,
        lore="A hulking construct of iron and void energy — built to never tire, never flinch, never fall."
    )
    result = combat(player, golem)
    if result == "lose": return "lose"

    divider()
    typewriter_pause("The Golem crumbles. The Shard is yours.")
    player.shards += 1
    player.gain_gold(8)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("The king flees. Seraphine's rebels take the city.")
    slow_type('  [Seraphine]: "Two down. The third Shard is in the Sunken Ruins — far east."')
    slow_type('  [Seraphine]: "Malachar will send something worse now. Be ready."')
    pause()

    visit_shop(player, act_num=3)
    return "act_three"

def act_three(player):
    divider()
    slow_type("ACT III — THE SUNKEN RUINS OF VAEL'SHAR")
    pause()
    typewriter_pause("The Ashwood is a dead forest. Black trees. Grey sky. No birdsong.")

    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    typewriter_pause("Halfway through, you are ambushed.")
    pause()

    bandit = Enemy("Void-Touched Bandit", hp=80, attack=17, defence=7, xp_reward=45, gold_drop=10,
                   lore="A man consumed by void energy — hollow-eyed, desperate, dangerous.")
    r = combat(player, bandit)
    if r == "lose": return "lose"

    # Side quest
    result = sidequest_the_deserter(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

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
        slow_type("  [Defence permanently +3]")
    elif choice == 2:
        slow_type('  [Spirit]: "Honest, and dangerous. Power corrupts, child. Use it wisely."')
        player.attack += 4
        slow_type("  [Attack permanently +4]")
    elif choice == 3:
        slow_type('  [Spirit]: "The reluctant hero — history\'s most common kind, and often its greatest."')
        player.max_hp += 20; player.hp = min(player.hp + 20, player.max_hp)
        slow_type("  [Max HP permanently +20]")
    elif choice == 4:
        slow_type('  [Spirit]: "Grief is a powerful fire. Let it forge you — not consume you."')
        player.magic += 8
        slow_type("  [Magic permanently +8]")

    pause()
    typewriter_pause("The spirit fades. At the heart of the ruins, the Third Shard rests on a sunken altar.")
    typewriter_pause("But as you reach for it — a Void Serpent erupts from the water.")

    serpent = Enemy(
        name="Void Serpent",
        hp=95, attack=20, defence=6, xp_reward=60, gold_drop=12,
        lore="An ancient creature warped by void energy — scales like obsidian, eyes like dying stars."
    )
    r = combat(player, serpent)
    if r == "lose": return "lose"

    divider()
    player.shards += 1
    player.gain_gold(10)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    typewriter_pause("Three down. Two remain. The sky above Eldoria grows darker.")
    pause()

    visit_shop(player, act_num=4)
    return "act_four"

def act_four(player):
    divider()
    slow_type("ACT IV — THE ARCANE SPIRE")
    pause()
    typewriter_pause("The Arcane Spire rises from a mountaintop like a broken tooth.")
    typewriter_pause("Once the greatest school of magic in Eldoria. Now Malachar's tower.")

    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    # Side quest
    result = sidequest_the_oracle(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    typewriter_pause("You climb for two days. At the summit gate, a Void Lord waits.")
    pause()

    lord_one = Enemy(
        name="Void Lord Vareth",
        hp=130, attack=22, defence=10, xp_reward=90, gold_drop=20,
        lore="Lord Vareth — Malachar's second-in-command. Tall, cold, and utterly merciless."
    )
    r = combat(player, lord_one)
    if r == "lose": return "lose"

    divider()
    slow_type('  [Vareth, dying]: "You... don\'t understand what Malachar truly is.')
    slow_type('  He isn\'t trying to destroy Eldoria. He is trying to save it."')
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
        slow_type("  [You found Malachar's Journal]")
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
    slow_type('  [Malachar]: "If you reforge the Crystal Crown incorrectly — you will feed it everything."')
    pause()

    choice = get_choice("How do you respond?", [
        '"Then tell me the right way to reforge them."',
        '"I don\'t believe you. This is a manipulation."',
        '"Why didn\'t you just tell someone? Why destroy Eldoria?"',
    ])
    if choice == 1:
        slow_type('  [Malachar]: "...Perhaps you are different. Come to me.')
        slow_type('  Bring the Shards. I will show you the truth at the end of the world."')
    elif choice == 2:
        slow_type('  [Malachar]: "Believe what you wish. But when the door opens — remember this moment."')
    elif choice == 3:
        slow_type('  [Malachar]: "Because I am not good at trust. I never have been.')
        slow_type('  I made choices in darkness when I should have sought light. I know that now."')
        slow_type('  [His voice cracks — just slightly.]')
        pause()

    typewriter_pause("The vision fades. You take the Fourth Shard.")
    player.shards += 1
    player.gain_gold(12)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    pause()
    typewriter_pause("One remains. The Fifth Shard is in Malachar's throne room.")
    typewriter_pause("At the end of the world.")
    pause()

    visit_shop(player, act_num=5)
    return "act_five"

def act_five(player):
    divider()
    slow_type("ACT V — THE THRONE OF ASHES")
    pause()
    typewriter_pause("The Throne of Ashes rises at the edge of the known world.")
    typewriter_pause("Where the land ends and the Void begins.")
    typewriter_pause("The sky here is not black. It is nothing. An absence of sky.")

    result = travel_event(player)
    if result == "lose" or not player.is_alive():
        return "lose"

    typewriter_pause("You walk toward it alone.")
    pause()

    slow_type("  Malachar stands at the gate. No guards. No tricks.")
    slow_type("  He looks older than you imagined. Tired. Sad.")
    pause()
    slow_type('  [Malachar]: "You made it. Four Shards. Almost there."')
    slow_type('  [Malachar]: "Now comes the choice the prophecy never told you about."')
    pause()

    has_journal = "Malachar's Journal" in player.inventory
    is_hero = player.reputation >= 5 and player.quests_completed >= 3  # secret ending condition

    if is_hero:
        slow_type('  [Malachar]: "...You\'re different from the others who\'ve come before."')
        slow_type('  [Malachar]: "I can feel it. Your choices. The people you helped."')
        slow_type('  [Malachar]: "Maybe... maybe there IS a third way. One I never considered."')
        pause()
        choice = get_choice("What do you do?", [
            "Fight Malachar and take the Fifth Shard by force.",
            "Let Malachar sacrifice himself to seal the Void.",
            "Offer your own life instead.",
            "Propose the third way — forge a new Shard together from your shared will.",
        ])
    elif has_journal:
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
            hp=180, attack=28, defence=12, xp_reward=150, gold_drop=0,
            lore="He is not a monster. He is a man who made terrible choices for reasons he believed were right."
        )
        r = combat(player, malachar)
        if r == "lose": return "lose"
        divider()
        typewriter_pause("Malachar falls. The Fifth Shard falls from his robes.")
        player.shards += 1
        slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
        pause()
        typewriter_pause("The Crystal Crown is reforged in your hands.")
        typewriter_pause("You hold it above your head — and bring it down.")
        typewriter_pause("The Void screams. The sky returns. Eldoria breathes again.")
        pause()
        return "ending_victory_blood"

    elif choice == 2 and (has_journal or is_hero):
        typewriter_pause("You lower your weapon.")
        slow_type('  [Malachar]: "...Thank you."')
        slow_type('  [Malachar]: "I was never going to ask. But I hoped."')
        pause()
        typewriter_pause("Malachar takes the Shards. He walks to the edge of the Void.")
        typewriter_pause("He speaks words older than language. Light tears through the darkness.")
        typewriter_pause("The Void shrinks. And then is gone. Malachar with it.")
        pause()
        player.shards = 5
        return "ending_redemption"

    elif choice == 3 and (has_journal or is_hero):
        typewriter_pause("Malachar stares at you for a long moment.")
        slow_type('  [Malachar]: "No. Absolutely not."')
        slow_type('  [Malachar]: "You have a future. I lost mine a century ago."')
        pause()
        typewriter_pause("He takes the Shards before you can stop him.")
        typewriter_pause("He walks into the Void. He does not look back.")
        player.shards = 5
        return "ending_redemption"

    elif choice == 4 and is_hero:
        # SECRET ENDING — only unlocked with high reputation AND 3+ quests completed
        typewriter_pause("Malachar stares at you — genuinely stunned.")
        slow_type('  [Malachar]: "A... new Shard? Forged from will? That\'s not possible."')
        slow_type('  [Malachar]: "...Is it?"')
        pause()
        typewriter_pause("You place your hand over his. The four Shards glow between you.")
        typewriter_pause("Every person you helped. Every choice you made toward light.")
        typewriter_pause("It becomes something real.")
        typewriter_pause("A Sixth Shard — born not from the old world, but from this one.")
        pause()
        typewriter_pause("The Crystal Crown reforges itself — six Shards instead of five.")
        typewriter_pause("Malachar looks at it. Then at you.")
        slow_type('  [Malachar]: "I never believed a thing like this was possible."')
        slow_type('  [Malachar]: "I do now."')
        player.shards = 5
        return "ending_transcendence"

    else:
        # Talk / demand answers path
        slow_type('  [Malachar]: "The Void beyond the Veil is alive. It waits for the Crown to be reforged.')
        slow_type('  When five Shards unite incorrectly, a door opens — and what is behind it makes me')
        slow_type('  look like a summer storm."')
        pause()
        slow_type('  [Malachar]: "I shattered the Shards to keep that door closed. For a century. Alone."')
        pause()
        choice2 = get_choice("Your answer:", [
            "Fight him anyway.",
            "Work with him. Seal the Void together.",
        ])
        if choice2 == 1:
            malachar = Enemy(
                name="Malachar, the Last Sorcerer",
                hp=180, attack=28, defence=12, xp_reward=150, gold_drop=0,
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
#  Endings (4 total)
# ─────────────────────────────────────────────

def ending_victory_blood(player):
    divider()
    slow_type("ENDING I: THE WARRIOR'S CROWN")
    pause()
    slow_type("You stood alone against the darkness and won.")
    slow_type("Malachar is dead. The Crystal Crown is reforged. Eldoria will heal.")
    slow_type("They will sing songs about you for a thousand years.")
    pause()
    slow_type("But sometimes, in the quiet, you wonder if he was telling the truth.")
    slow_type("And whether the door is truly closed. Or just... waiting.")
    _show_final_stats(player, "THE WARRIOR'S CROWN")

def ending_redemption(player):
    divider()
    slow_type("ENDING II: THE PRICE OF MERCY")
    pause()
    slow_type("You gave a broken man the chance to become something better.")
    slow_type("In his final act, Malachar sealed the Void — and atoned for a century of darkness.")
    slow_type("Eldoria will never know his name was whispered in kindness at the end.")
    slow_type("But you know. And that is enough.")
    _show_final_stats(player, "THE PRICE OF MERCY")

def ending_alliance(player):
    divider()
    slow_type("ENDING III: THE UNLIKELY ALLIANCE")
    pause()
    slow_type("You chose trust when distrust would have been easier.")
    slow_type("Together, you and Malachar sealed the Void.")
    slow_type("He survived — barely. Changed. Not good, not yet.")
    slow_type("But no longer lost.")
    slow_type("Eldoria begins to rebuild. For the first time in a century,")
    slow_type("the sun rises without shadows.")
    _show_final_stats(player, "THE UNLIKELY ALLIANCE")

def ending_transcendence(player):
    divider()
    slow_type("ENDING IV: THE SIXTH SHARD  ★ SECRET ENDING ★")
    pause()
    slow_type("You didn't just save the world.")
    slow_type("You changed what the world believes is possible.")
    pause()
    slow_type("The Sixth Shard — born from human will and compassion — now floats above Eldoria.")
    slow_type("It does not belong to anyone. It belongs to everyone.")
    pause()
    slow_type("Malachar lived. Seraphine rebuilt Duskmar. The oracle smiled for the first time in decades.")
    slow_type("The ghost rested. The deserter went home. The lost child grew up.")
    pause()
    slow_type("All of them — because you chose, again and again, to care.")
    slow_type("That is not a small thing. That is everything.")
    _show_final_stats(player, "THE SIXTH SHARD  ★ SECRET ENDING ★")

def _show_final_stats(player, ending_name):
    divider()
    slow_type(f"  {player.name} the {player.cls} — Level {player.level}")
    slow_type(f"  Shards: {player.shards}/5  |  Quests: {player.quests_completed}  |  Reputation: {player.reputation}")
    slow_type(f"  Ending: {ending_name}")
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

        divider()
        slow_type("PROLOGUE — THE WORLD BEFORE\n")
        for line in LORE_INTRO:
            slow_type(line)
            pause(0.6)

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

        acts = [act_one, act_two, act_three, act_four, act_five]
        state = None
        for act_fn in acts:
            state = act_fn(player)
            if state == "lose" or not player.is_alive():
                state = "lose"
                break

        if state == "lose":
            ending_lose(player)
        elif state == "ending_victory_blood":
            ending_victory_blood(player)
        elif state == "ending_redemption":
            ending_redemption(player)
        elif state == "ending_alliance":
            ending_alliance(player)
        elif state == "ending_transcendence":
            ending_transcendence(player)

        again = get_choice("\nPlay again?", ["Yes", "No"])
        if again == 2:
            slow_type("May your next journey be a worthy one. Farewell.")
            break

if __name__ == "__main__":
    main()
