import time
import os
import random
import json

# ═══════════════════════════════════════════════════════
#  ELDORIA CHRONICLES — EXPANDED EDITION
#  Features: 8 classes, save/load, crafting, companions,
#  world map, 8 side quests, 5 acts, 5 endings, bestiary,
#  weather system, class-specific dialogue, titles & achievements
# ═══════════════════════════════════════════════════════

SAVE_FILE = "eldoria_save.json"

# ─────────────────────────────────────────────
#  Utility
# ─────────────────────────────────────────────

def slow_type(text, delay=0.04):
    for char in str(text):
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def pause(sec=1.0):
    time.sleep(sec)

def divider():
    print("\n" + "═" * 52 + "\n")

def mini_divider():
    print("  " + "─" * 40)

def get_choice(prompt, options):
    while True:
        if prompt:
            slow_type(prompt)
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        choice = input("\n> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        slow_type("  Please enter a valid number.")

def typewriter_pause(text, delay=0.04, after=0.8):
    slow_type(text, delay)
    pause(after)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────
#  LORE
# ─────────────────────────────────────────────

LORE_INTRO = [
    "In the beginning, there was light.",
    "Five Crystal Shards — each holding a fragment of creation\n  floated above the realm of Eldoria.",
    "They gave warmth to the fields of Greenhollow,\n  strength to the warriors of Ironpeak,\n  wisdom to the mages of the Arcane Spire,\n  and hope to every soul beneath the sky.",
    "Then came Malachar.",
    "Once the greatest sorcerer who ever lived.\n  Now something far older. Far darker.",
    "He shattered the Shards in a single night.\n  The sky turned black. The oceans boiled.\n  The gods... fell silent.",
    "That was one hundred years ago.",
    "You were born into the ash.",
    "You have nothing — no army, no crown, no power.\n  Only a name. And a prophecy that will not let you rest.",
    "The Throne of Ashes speaks:\n  'One soul from the dust shall rise —\n   and either save the world, or become its end.'",
    "That soul is you.",
    "The question is: what kind of soul are you?",
]

# ─────────────────────────────────────────────
#  WEATHER SYSTEM
# ─────────────────────────────────────────────

WEATHERS = [
    ("Clear skies", "The sun is pale but present.", 0, 0),
    ("Heavy rain", "Rain hammers the earth. Visibility drops.", -2, 0),
    ("Ash storm", "Void ash fills the air — your lungs burn.", -3, -2),
    ("Eerie fog", "Thick fog clings to everything. Your senses sharpen.", 0, 2),
    ("Blood moon", "A crimson moon hangs low. Enemies are more aggressive.", 0, 5),
    ("Gentle wind", "A warm breeze carries the scent of old flowers.", 2, 0),
    ("Lightning storm", "Lightning cracks overhead. Magic crackles.", 5, 0),
]

def get_weather():
    return random.choice(WEATHERS)

def announce_weather(weather):
    name, desc, magic_bonus, enemy_bonus = weather
    slow_type(f"\n  [Weather: {name}]")
    slow_type(f"  {desc}")
    if magic_bonus != 0:
        slow_type(f"  Your magic is {'boosted' if magic_bonus > 0 else 'weakened'} by {abs(magic_bonus)} in this weather.")
    if enemy_bonus != 0:
        slow_type(f"  Enemies are {'stronger' if enemy_bonus > 0 else 'weaker'} by {abs(enemy_bonus)} in this weather.")

# ─────────────────────────────────────────────
#  BESTIARY
# ─────────────────────────────────────────────

BESTIARY = {}

def record_kill(player, enemy_name):
    if not hasattr(player, 'bestiary'):
        player.bestiary = {}
    player.bestiary[enemy_name] = player.bestiary.get(enemy_name, 0) + 1

def show_bestiary(player):
    divider()
    slow_type("BESTIARY — Creatures Slain\n")
    if not hasattr(player, 'bestiary') or not player.bestiary:
        slow_type("  You have not slain any notable creatures yet.")
    else:
        for name, count in sorted(player.bestiary.items()):
            print(f"  {name}: {count} defeated")
    pause(1)

# ─────────────────────────────────────────────
#  CRAFTING SYSTEM
# ─────────────────────────────────────────────

RECIPES = {
    "Mega Potion": {
        "ingredients": {"Health Potion": 2},
        "description": "Restores 120 HP",
        "result": "Mega Potion"
    },
    "Arcane Brew": {
        "ingredients": {"Ether Vial": 2},
        "description": "Restores full MP",
        "result": "Arcane Brew"
    },
    "Void Flask": {
        "ingredients": {"Health Potion": 1, "Ether Vial": 1},
        "description": "Restores 60 HP and 30 MP",
        "result": "Void Flask"
    },
    "Elixir of Fortitude": {
        "ingredients": {"Mega Potion": 1, "Arcane Brew": 1},
        "description": "Fully restores HP and MP",
        "result": "Elixir of Fortitude"
    },
    "Shadow Oil": {
        "ingredients": {"Smoke Bomb": 1, "Ether Vial": 1},
        "description": "Next attack deals double damage (one use)",
        "result": "Shadow Oil"
    },
}

def crafting_menu(player):
    divider()
    slow_type("CRAFTING — Combine items to create new ones\n")
    slow_type(f"  Your inventory: {', '.join(player.inventory) if player.inventory else 'Empty'}\n")

    available = []
    for name, recipe in RECIPES.items():
        can_craft = True
        for ing, qty in recipe["ingredients"].items():
            if player.inventory.count(ing) < qty:
                can_craft = False
                break
        status = "✓" if can_craft else "✗"
        ings = ", ".join(f"{v}x {k}" for k, v in recipe["ingredients"].items())
        available.append((name, recipe, can_craft, status, ings))

    options = [f"{s} {n} ({ings}) → {r['description']}" for n, r, _, s, ings in available]
    options.append("Leave crafting bench")
    choice = get_choice("", options)
    if choice == len(options):
        return
    name, recipe, can_craft, _, _ = available[choice - 1]
    if not can_craft:
        slow_type("  You don't have the required ingredients.")
        return
    for ing, qty in recipe["ingredients"].items():
        for _ in range(qty):
            player.inventory.remove(ing)
    player.inventory.append(recipe["result"])
    slow_type(f"  You crafted a {recipe['result']}!")

# ─────────────────────────────────────────────
#  COMPANION SYSTEM
# ─────────────────────────────────────────────

class Companion:
    def __init__(self, name, role, attack, heal_power, dialogue):
        self.name = name
        self.role = role
        self.attack = attack
        self.heal_power = heal_power
        self.dialogue = dialogue
        self.cooldown = 0

    def act(self, player, enemy):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        roll = random.random()
        if roll < 0.4:
            dmg = max(1, self.attack + random.randint(-3, 3) - enemy.defence)
            enemy.hp = max(0, enemy.hp - dmg)
            slow_type(f"  [{self.name}] attacks {enemy.name} for {dmg} damage!")
        elif roll < 0.6 and player.hp < player.max_hp * 0.5:
            healed = player.heal(self.heal_power)
            slow_type(f"  [{self.name}] heals you for {healed} HP!")
        else:
            slow_type(f"  [{self.name}]: \"{random.choice(self.dialogue)}\"")
        self.cooldown = random.randint(1, 2)

COMPANIONS_POOL = [
    Companion("Seraphine", "Warrior", attack=18, heal_power=0, dialogue=[
        "Hold the line!", "I've fought worse than this.", "For Eldoria!"
    ]),
    Companion("Elder Mara", "Healer", attack=5, heal_power=30, dialogue=[
        "Stay strong, child.", "The prophecy holds true.", "I believe in you."
    ]),
    Companion("Kael", "Rogue", attack=25, heal_power=0, dialogue=[
        "I had worse odds last Tuesday.", "Shadow and silence.", "Don't blink."
    ]),
    Companion("Lyra", "Mage", attack=30, heal_power=0, dialogue=[
        "Arcane energies surge!", "The stars align!", "Feel the power of the Spire!"
    ]),
]

# ─────────────────────────────────────────────
#  ACHIEVEMENTS
# ─────────────────────────────────────────────

ACHIEVEMENTS = {
    "first_blood":      ("First Blood",        "Win your first combat."),
    "pacifist":         ("Pacifist",           "Complete a full act without fleeing or losing."),
    "hoarder":          ("Hoarder",            "Carry 6+ items at once."),
    "rich":             ("Merchant Prince",    "Accumulate 100+ gold."),
    "crafter":          ("Alchemist",          "Craft your first item."),
    "max_level":        ("Legend",             "Reach level 10."),
    "secret_ending":    ("The Sixth Shard",    "Unlock the secret ending."),
    "all_quests":       ("True Hero",          "Complete all 4 side quests."),
    "high_rep":         ("Saint of Eldoria",   "Reach reputation 8+."),
    "bestiary_master":  ("Monster Hunter",     "Slay 10+ different enemy types."),
}

def unlock_achievement(player, key):
    if not hasattr(player, 'achievements'):
        player.achievements = set()
    if key not in player.achievements:
        player.achievements.add(key)
        name, desc = ACHIEVEMENTS[key]
        slow_type(f"\n  ★ ACHIEVEMENT UNLOCKED: {name} — {desc}")
        pause(0.5)

def show_achievements(player):
    divider()
    slow_type("ACHIEVEMENTS\n")
    ach = getattr(player, 'achievements', set())
    for key, (name, desc) in ACHIEVEMENTS.items():
        status = "★" if key in ach else "○"
        print(f"  {status} {name}: {desc}")
    pause(1)

# ─────────────────────────────────────────────
#  TITLES SYSTEM
# ─────────────────────────────────────────────

def get_title(player):
    rep = player.reputation
    level = player.level
    quests = player.quests_completed
    if rep >= 8:
        return "the Beloved"
    if rep <= -4:
        return "the Ruthless"
    if level >= 10:
        return "the Legendary"
    if quests >= 4:
        return "the True Hero"
    if player.shards >= 3:
        return "the Shard-Bearer"
    if level >= 5:
        return "the Seasoned"
    return "the Wanderer"

# ─────────────────────────────────────────────
#  SAVE / LOAD
# ─────────────────────────────────────────────

def save_game(player, act_name):
    data = {
        "name": player.name,
        "cls": player.cls,
        "hp": player.hp,
        "max_hp": player.max_hp,
        "mp": player.mp,
        "max_mp": player.max_mp,
        "attack": player.attack,
        "base_attack": player.base_attack,
        "defence": player.defence,
        "magic": player.magic,
        "skill": player.skill,
        "skill_desc": player.skill_desc,
        "lore": player.lore,
        "shards": player.shards,
        "inventory": player.inventory,
        "gold": player.gold,
        "level": player.level,
        "xp": player.xp,
        "xp_needed": player.xp_needed,
        "quests_completed": player.quests_completed,
        "reputation": player.reputation,
        "achievements": list(getattr(player, 'achievements', set())),
        "bestiary": getattr(player, 'bestiary', {}),
        "companions": [c.name for c in getattr(player, 'companions', [])],
        "act": act_name,
        "attack_boost": player.attack_boost,
        "attack_boost_rounds": player.attack_boost_rounds,
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    slow_type("  [Game saved.]")

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None, None
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        stats = {
            "hp": data["max_hp"], "mp": data["max_mp"],
            "attack": data["base_attack"], "defence": data["defence"],
            "magic": data["magic"], "skill": data["skill"],
            "skill_desc": data["skill_desc"], "lore": data["lore"],
        }
        player = Player(data["name"], data["cls"], stats)
        player.hp = data["hp"]
        player.mp = data["mp"]
        player.attack = data["attack"]
        player.shards = data["shards"]
        player.inventory = data["inventory"]
        player.gold = data["gold"]
        player.level = data["level"]
        player.xp = data["xp"]
        player.xp_needed = data["xp_needed"]
        player.quests_completed = data["quests_completed"]
        player.reputation = data["reputation"]
        player.achievements = set(data.get("achievements", []))
        player.bestiary = data.get("bestiary", {})
        player.attack_boost = data.get("attack_boost", 0)
        player.attack_boost_rounds = data.get("attack_boost_rounds", 0)
        # Restore companions by name
        comp_names = data.get("companions", [])
        player.companions = [c for c in COMPANIONS_POOL if c.name in comp_names]
        act = data.get("act", "act_one")
        return player, act
    except Exception as e:
        slow_type(f"  [Save file corrupted: {e}]")
        return None, None

# ─────────────────────────────────────────────
#  CHARACTER CLASSES (8 total)
# ─────────────────────────────────────────────

CLASSES = {
    "Knight of Ashenveil": {
        "description": "Battle-hardened warrior. High HP and defence.",
        "hp": 140, "mp": 30, "attack": 22, "defence": 12, "magic": 5,
        "skill": "Rallying Cry",
        "skill_desc": "Restores 25 HP and raises attack by 5 for 3 rounds.",
        "lore": "The Knights of Ashenveil were once Eldoria's greatest guard. You are the last.",
    },
    "Shadowblade": {
        "description": "Rogue who strikes from darkness. High attack, low defence.",
        "hp": 100, "mp": 50, "attack": 35, "defence": 6, "magic": 10,
        "skill": "Void Step",
        "skill_desc": "Guaranteed critical hit dealing 4x damage.",
        "lore": "You learned to survive in the gutters of Malachar's empire. Shadows are your home.",
    },
    "Arcanist": {
        "description": "Spellweaver of forbidden magic. Fragile but devastating.",
        "hp": 85, "mp": 120, "attack": 12, "defence": 4, "magic": 45,
        "skill": "Starfall",
        "skill_desc": "Summons meteors for 60 magic damage. Costs 30 MP.",
        "lore": "You survived the burning of the Arcane Spire. Magic flows through your blood like grief.",
    },
    "Warden of the Wild": {
        "description": "Nature guardian bonded to beasts. Balanced with crowd control.",
        "hp": 115, "mp": 80, "attack": 18, "defence": 9, "magic": 20,
        "skill": "Nature's Wrath",
        "skill_desc": "Roots enemy for 2 turns and deals 25 damage.",
        "lore": "The forests of Eldoria still live. You speak for them.",
    },
    "Paladin of the Eternal Flame": {
        "description": "Holy warrior. Smites enemies and heals simultaneously.",
        "hp": 130, "mp": 70, "attack": 20, "defence": 11, "magic": 25,
        "skill": "Divine Smite",
        "skill_desc": "3x magic damage as holy light AND heals 20 HP.",
        "lore": "The gods are silent — but their fire lives in you. You carry their last ember.",
    },
    "Necromancer": {
        "description": "Dark mage with lifesteal. Drains life to sustain yourself.",
        "hp": 90, "mp": 100, "attack": 15, "defence": 5, "magic": 40,
        "skill": "Soul Drain",
        "skill_desc": "Drains 45 magic damage and restores half as HP.",
        "lore": "Death is not an end. You learned that the hard way. Now you use it as a weapon.",
    },
    "Beastcaller": {
        "description": "Summons wild beasts to fight alongside you. Unique summoning mechanic.",
        "hp": 110, "mp": 90, "attack": 16, "defence": 8, "magic": 18,
        "skill": "Summon Pack",
        "skill_desc": "Summons a wolf companion that attacks every round for 3 rounds (15 dmg/round).",
        "lore": "You were raised by the creatures of the Blackwood. Civilisation is a foreign language.",
    },
    "Runeblade": {
        "description": "Warrior who inscribes runes mid-battle. Versatile and unpredictable.",
        "hp": 120, "mp": 60, "attack": 24, "defence": 10, "magic": 22,
        "skill": "Runic Surge",
        "skill_desc": "Inscribes a random rune — Fire (35 dmg), Ice (stun + 20 dmg), or Thunder (25 dmg + weaken).",
        "lore": "You carved your first rune at age seven. By twelve, you'd carved a hundred. By now, you've lost count.",
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
    choice = get_choice("Choose your class:", names)
    chosen = names[choice - 1]
    return chosen, dict(CLASSES[chosen])

# ─────────────────────────────────────────────
#  PLAYER
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
        self.lore = stats.get("lore", "")
        self.stunned = False
        self.attack_boost = 0
        self.attack_boost_rounds = 0
        self.shards = 0
        self.inventory = []
        self.gold = 15
        self.level = 1
        self.xp = 0
        self.xp_needed = 50
        self.quests_completed = 0
        self.reputation = 0
        self.achievements = set()
        self.bestiary = {}
        self.companions = []
        self.wolf_summon_rounds = 0
        self.enemy_weakened = False
        self.skill_used = False

    def is_alive(self):
        return self.hp > 0

    def gain_xp(self, amount):
        self.xp += amount
        slow_type(f"  [+{amount} XP — Total: {self.xp}/{self.xp_needed}]")
        if self.xp >= self.xp_needed:
            self.level_up()
        if self.level >= 10:
            unlock_achievement(self, "max_level")

    def gain_gold(self, amount):
        self.gold += amount
        slow_type(f"  [+{amount} gold — Total: {self.gold}]")
        if self.gold >= 100:
            unlock_achievement(self, "rich")

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_needed
        self.xp_needed = int(self.xp_needed * 1.6)
        hp_gain = random.randint(10, 20)
        atk_gain = random.randint(2, 5)
        mp_gain = random.randint(5, 12)
        self.max_hp += hp_gain
        self.hp = min(self.hp + hp_gain, self.max_hp)
        self.max_mp += mp_gain
        self.attack += atk_gain
        self.base_attack = self.attack
        divider()
        slow_type(f"✨ LEVEL UP! You are now Level {self.level}!")
        slow_type(f"  HP +{hp_gain}  |  ATK +{atk_gain}  |  MP +{mp_gain}")
        pause()

    def heal(self, amount):
        healed = min(amount, self.max_hp - self.hp)
        self.hp += healed
        return healed

    def status(self):
        title = get_title(self)
        print(f"\n  {self.name} {title} | {self.cls} | Lv.{self.level}")
        print(f"  HP: {self.hp}/{self.max_hp}  MP: {self.mp}/{self.max_mp}")
        print(f"  ATK: {self.attack}  DEF: {self.defence}  MAG: {self.magic}")
        print(f"  Shards: {self.shards}/5  Gold: {self.gold}  Reputation: {self.reputation}")
        print(f"  XP: {self.xp}/{self.xp_needed}  Quests: {self.quests_completed}")
        if self.companions:
            print(f"  Companions: {', '.join(c.name for c in self.companions)}")
        if self.inventory:
            print(f"  Inventory: {', '.join(self.inventory)}")
        print()

# ─────────────────────────────────────────────
#  ENEMY
# ─────────────────────────────────────────────

class Enemy:
    def __init__(self, name, hp, attack, defence, xp_reward, gold_drop=0, lore="", abilities=None):
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
        self.abilities = abilities or []
        self.weakened = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, dmg):
        actual = max(1, dmg - (0 if self.weakened else self.defence))
        self.hp = max(0, self.hp - actual)
        return actual

    def ai_attack(self, player, weather_enemy_bonus=0):
        if self.stunned:
            self.stun_turns -= 1
            if self.stun_turns <= 0:
                self.stunned = False
            slow_type(f"  {self.name} is stunned and cannot act!")
            return
        base = self.attack + weather_enemy_bonus
        roll = random.random()
        # Special abilities
        if self.abilities and roll < 0.25:
            ability = random.choice(self.abilities)
            if ability == "poison":
                dmg = max(1, base // 2 - player.defence)
                player.hp = max(0, player.hp - dmg)
                slow_type(f"  {self.name} poisons you for {dmg} damage! (Effect lingers...)")
            elif ability == "drain":
                dmg = max(1, base - player.defence)
                player.hp = max(0, player.hp - dmg)
                self.hp = min(self.max_hp, self.hp + dmg // 2)
                slow_type(f"  {self.name} drains your life! {dmg} damage, heals {dmg//2}.")
            elif ability == "shield":
                self.defence += 3
                slow_type(f"  {self.name} raises a void shield! Defence +3.")
            elif ability == "berserk":
                self.attack += 4
                slow_type(f"  {self.name} enters a berserker rage! Attack +4.")
            elif ability == "summon":
                slow_type(f"  {self.name} summons a Void Sprite to assist!")
                dmg = max(1, 8 - player.defence)
                player.hp = max(0, player.hp - dmg)
                slow_type(f"  Void Sprite attacks for {dmg} damage!")
        elif roll < 0.2:
            dmg = max(1, int(base * 1.8) + random.randint(0, 8) - player.defence)
            player.hp = max(0, player.hp - dmg)
            slow_type(f"  {self.name} unleashes a HEAVY STRIKE for {dmg} damage!")
        elif roll < 0.35 and player.hp < player.max_hp * 0.4:
            dmg = max(1, base + random.randint(5, 15) - player.defence)
            player.hp = max(0, player.hp - dmg)
            slow_type(f"  {self.name} senses weakness and lunges — {dmg} damage!")
        else:
            dmg = max(1, base + random.randint(-4, 4) - player.defence)
            player.hp = max(0, player.hp - dmg)
            slow_type(f"  {self.name} attacks for {dmg} damage!")

# ─────────────────────────────────────────────
#  COMBAT ENGINE
# ─────────────────────────────────────────────

def use_item(player, enemy):
    usable = [i for i in player.inventory if i in [
        "Health Potion", "Ether Vial", "Smoke Bomb",
        "Elixir of Fortitude", "Mega Potion", "Arcane Brew",
        "Void Flask", "Shadow Oil"
    ]]
    if not usable:
        slow_type("  You have no usable items!")
        return False
    choice = get_choice("Use which item?", usable + ["Cancel"])
    if choice == len(usable) + 1:
        return False
    item = usable[choice - 1]
    player.inventory.remove(item)
    if item == "Health Potion":
        slow_type(f"  You drink a Health Potion — recovered {player.heal(50)} HP!")
    elif item == "Mega Potion":
        slow_type(f"  You drink a Mega Potion — recovered {player.heal(120)} HP!")
    elif item == "Ether Vial":
        gain = min(40, player.max_mp - player.mp)
        player.mp += gain
        slow_type(f"  You drink an Ether Vial — restored {gain} MP!")
    elif item == "Arcane Brew":
        gain = player.max_mp - player.mp
        player.mp = player.max_mp
        slow_type(f"  You drink an Arcane Brew — full MP restored! (+{gain})")
    elif item == "Void Flask":
        h = player.heal(60)
        m = min(30, player.max_mp - player.mp)
        player.mp += m
        slow_type(f"  Void Flask: +{h} HP, +{m} MP!")
    elif item == "Smoke Bomb":
        slow_type("  You hurl a Smoke Bomb and escape!")
        return "fled"
    elif item == "Elixir of Fortitude":
        player.hp = player.max_hp
        player.mp = player.max_mp
        slow_type("  Elixir of Fortitude — fully restored!")
    elif item == "Shadow Oil":
        player._shadow_oil_active = True
        slow_type("  Shadow Oil applied — your next attack deals double damage!")
    if len(player.inventory) >= 6:
        unlock_achievement(player, "hoarder")
    return True

def player_turn(player, enemy, weather):
    _, _, magic_bonus, _ = weather
    actions = ["Basic Attack", f"Skill: {player.skill}", "Use Item", "Check Status", "Flee (50%)"]
    choice = get_choice(f"\n{player.name}'s turn:", actions)

    if choice == 1:
        dmg = player.attack + random.randint(-4, 6)
        if getattr(player, '_shadow_oil_active', False):
            dmg *= 2
            player._shadow_oil_active = False
            slow_type("  Shadow Oil activates — DOUBLE DAMAGE!")
        dealt = enemy.take_damage(dmg)
        slow_type(f"  {player.name} attacks for {dealt} damage! ({enemy.name} HP: {enemy.hp})")

    elif choice == 2:
        # Skills per class
        if player.cls == "Knight of Ashenveil":
            healed = player.heal(25)
            player.attack += 5
            player.attack_boost = 5
            player.attack_boost_rounds = 3
            slow_type(f"  Rallying Cry! +{healed} HP, Attack +5 for 3 rounds!")

        elif player.cls == "Shadowblade":
            dmg = player.attack * 4
            dealt = enemy.take_damage(dmg)
            slow_type(f"  Void Step — critical hit for {dealt} damage!")

        elif player.cls == "Arcanist":
            cost = 30
            if player.mp < cost:
                slow_type(f"  Not enough MP! ({player.mp}/{cost})")
                return player_turn(player, enemy, weather)
            player.mp -= cost
            dealt = enemy.take_damage(player.magic + magic_bonus + 20)
            slow_type(f"  Starfall! {dealt} magic damage!")

        elif player.cls == "Warden of the Wild":
            dealt = enemy.take_damage(25)
            enemy.stunned = True
            enemy.stun_turns = 2
            slow_type(f"  Nature's Wrath! {dealt} damage — {enemy.name} rooted for 2 turns!")

        elif player.cls == "Paladin of the Eternal Flame":
            dealt = enemy.take_damage((player.magic + magic_bonus) * 3)
            healed = player.heal(20)
            slow_type(f"  Divine Smite! {dealt} holy damage, +{healed} HP restored!")

        elif player.cls == "Necromancer":
            dealt = enemy.take_damage(45 + magic_bonus)
            restored = player.heal(dealt // 2)
            slow_type(f"  Soul Drain! {dealt} damage — absorbed {restored} HP!")

        elif player.cls == "Beastcaller":
            player.wolf_summon_rounds = 3
            slow_type("  Summon Pack! A wolf joins the fight for 3 rounds!")

        elif player.cls == "Runeblade":
            rune = random.choice(["Fire", "Ice", "Thunder"])
            if rune == "Fire":
                dealt = enemy.take_damage(35 + magic_bonus)
                slow_type(f"  Fire Rune blazes! {dealt} fire damage!")
            elif rune == "Ice":
                dealt = enemy.take_damage(20)
                enemy.stunned = True
                enemy.stun_turns = 1
                slow_type(f"  Ice Rune! {dealt} damage — {enemy.name} frozen for 1 turn!")
            else:
                dealt = enemy.take_damage(25)
                enemy.weakened = True
                slow_type(f"  Thunder Rune! {dealt} damage — {enemy.name} is weakened (defence ignored)!")

    elif choice == 3:
        result = use_item(player, enemy)
        if result == "fled":
            return "fled"
        if not result:
            return player_turn(player, enemy, weather)

    elif choice == 4:
        player.status()
        return player_turn(player, enemy, weather)

    elif choice == 5:
        if random.random() < 0.5:
            slow_type("  You successfully fled!")
            return "fled"
        slow_type("  You couldn't escape!")

    # Wolf summon (Beastcaller)
    if player.wolf_summon_rounds > 0 and enemy.is_alive():
        dmg = max(1, 15 - enemy.defence)
        enemy.hp = max(0, enemy.hp - dmg)
        player.wolf_summon_rounds -= 1
        slow_type(f"  [Wolf] lunges at {enemy.name} for {dmg} damage! ({player.wolf_summon_rounds} rounds left)")

    # Companions act
    for comp in getattr(player, 'companions', []):
        if enemy.is_alive():
            comp.act(player, enemy)

    # Tick attack boost
    if player.attack_boost_rounds > 0:
        player.attack_boost_rounds -= 1
        if player.attack_boost_rounds == 0:
            player.attack -= player.attack_boost
            player.attack_boost = 0
            slow_type("  Your attack boost fades.")

    return None

def combat(player, enemy, weather=None):
    if weather is None:
        weather = get_weather()
    _, _, magic_bonus, enemy_bonus = weather
    enemy.attack += enemy_bonus

    divider()
    announce_weather(weather)
    if enemy.lore:
        slow_type(f"\n  {enemy.lore}")
        pause(0.5)
    slow_type(f"\n⚔  {enemy.name} stands before you!")
    slow_type(f"   HP: {enemy.hp}  ATK: {enemy.attack}  DEF: {enemy.defence}")
    pause()

    round_num = 1
    while player.is_alive() and enemy.is_alive():
        slow_type(f"\n--- Round {round_num} | HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp} ---")
        if player.stunned:
            slow_type(f"  {player.name} is stunned and loses this turn!")
            player.stunned = False
        else:
            result = player_turn(player, enemy, weather)
            if result == "fled":
                return "fled"
        if enemy.is_alive():
            enemy.ai_attack(player, weather_enemy_bonus=0)
        round_num += 1

    if player.is_alive():
        slow_type(f"\n✅  {enemy.name} defeated!")
        record_kill(player, enemy.name)
        player.gain_xp(enemy.xp_reward)
        if enemy.gold_drop > 0:
            player.gain_gold(random.randint(max(1, enemy.gold_drop // 2), enemy.gold_drop))
        unlock_achievement(player, "first_blood")
        if len(player.bestiary) >= 10:
            unlock_achievement(player, "bestiary_master")
        return "win"
    return "lose"

# ─────────────────────────────────────────────
#  RANDOM TRAVEL ENCOUNTERS
# ─────────────────────────────────────────────

TRAVEL_EVENTS = [
    "abandoned_camp", "wounded_traveller", "void_ambush",
    "ancient_shrine", "merchant_cart", "strange_fog",
    "ruined_library", "companion_encounter", "crafting_bench",
    "cursed_chest", "old_soldier", "starfall_crater",
]

def travel_event(player):
    if random.random() > 0.65:
        return None
    event = random.choice(TRAVEL_EVENTS)
    divider()
    slow_type(f"  — A chance encounter on the road —\n")

    if event == "abandoned_camp":
        slow_type("You find an abandoned camp. A fire still smoulders.")
        choice = get_choice("Search the pack?", ["Yes", "Leave it"])
        if choice == 1:
            roll = random.random()
            if roll < 0.4:
                player.inventory.append("Health Potion")
                slow_type("  You find a Health Potion!")
            elif roll < 0.7:
                g = random.randint(4, 10)
                player.gain_gold(g)
            else:
                slow_type("  Trap! A Void Sprite lunges!")
                e = Enemy("Void Sprite", hp=35, attack=10, defence=2, xp_reward=15, gold_drop=4)
                combat(player, e)

    elif event == "wounded_traveller":
        slow_type("A wounded traveller leans against a tree.")
        slow_type('  "Please... I just want to go home."')
        choice = get_choice("What do you do?", [
            "Give a Health Potion (if you have one)",
            "Give 5 gold",
            "Walk past"
        ])
        if choice == 1 and "Health Potion" in player.inventory:
            player.inventory.remove("Health Potion")
            player.inventory.append("Smoke Bomb")
            slow_type('  [Traveller]: "Bless you. Take my smoke bomb."')
            player.reputation += 1
        elif choice == 2 and player.gold >= 5:
            player.gold -= 5
            player.reputation += 1
            slow_type("  [+1 Reputation]")
        else:
            player.reputation -= 1
            slow_type("  You walk on. The silence follows you.")

    elif event == "void_ambush":
        slow_type("Shadows converge. Wraiths — drawn to the Shard's glow!")
        e1 = Enemy("Void Wraith", hp=55, attack=13, defence=3, xp_reward=25, gold_drop=6)
        r = combat(player, e1)
        if r == "lose": return "lose"
        if player.is_alive() and random.random() < 0.5:
            e2 = Enemy("Void Wraith", hp=45, attack=11, defence=3, xp_reward=20, gold_drop=4)
            combat(player, e2)

    elif event == "ancient_shrine":
        slow_type("A shrine glows in the undergrowth.")
        slow_type('  "Offer gold. Receive blessing."')
        choice = get_choice("Offer how much?", ["10 gold", "20 gold", "Steal the offering bowl", "Walk on"])
        if choice == 1 and player.gold >= 10:
            player.gold -= 10
            _shrine_bless(player, minor=True)
        elif choice == 2 and player.gold >= 20:
            player.gold -= 20
            _shrine_bless(player, minor=False)
        elif choice == 3:
            player.gain_gold(random.randint(5, 15))
            player.reputation -= 2
            slow_type("  Something in the air feels wrong now.")
        else:
            slow_type("  You pass it by.")

    elif event == "merchant_cart":
        _visit_merchant(player)

    elif event == "strange_fog":
        slow_type("Silver fog rolls in. A voice speaks:")
        slow_type('  "You are not ready. But you never will be. Go anyway."')
        boost = random.choice(["xp", "heal", "mp", "stat"])
        if boost == "xp":
            player.gain_xp(35)
        elif boost == "heal":
            slow_type(f"  You feel restored — {player.heal(45)} HP recovered.")
        elif boost == "mp":
            gain = min(35, player.max_mp - player.mp)
            player.mp += gain
            slow_type(f"  Your mind sharpens — {gain} MP restored.")
        else:
            player.attack += 2
            slow_type("  Your strikes feel crisper — Attack +2!")

    elif event == "ruined_library":
        slow_type("You find a ruined library — shelves of ashen books.")
        slow_type("One tome survives. Its cover reads: 'The Void — A Treatise'.")
        choice = get_choice("Read it?", ["Yes, study it carefully", "Take it and move on", "Leave it"])
        if choice == 1:
            slow_type("  Hours pass. The knowledge is dense — and disturbing.")
            slow_type("  But you emerge wiser.")
            player.magic += 5
            player.xp += 20
            slow_type("  [Magic +5, +20 XP]")
            player.reputation += 1
        elif choice == 2:
            player.inventory.append("Void Tome")
            slow_type("  [Item added: Void Tome — sell for 20 gold or study later]")

    elif event == "companion_encounter":
        available = [c for c in COMPANIONS_POOL if c not in player.companions]
        if not available:
            slow_type("  A familiar face nods at you from afar. The road provides.")
            return None
        comp = random.choice(available)
        slow_type(f"  You encounter {comp.name} — {comp.role}.")
        slow_type(f'  [{comp.name}]: "{random.choice(comp.dialogue)}"')
        choice = get_choice(f"Ask {comp.name} to travel with you?", ["Yes", "No"])
        if choice == 1:
            player.companions.append(comp)
            slow_type(f"  {comp.name} joins you! They will assist in combat.")

    elif event == "crafting_bench":
        slow_type("You find an abandoned alchemist's bench — still functional.")
        crafting_menu(player)
        unlock_achievement(player, "crafter")

    elif event == "cursed_chest":
        slow_type("A chest sits in the middle of the road. Unlocked. Waiting.")
        choice = get_choice("Open it?", ["Yes — take the risk", "No"])
        if choice == 1:
            roll = random.random()
            if roll < 0.4:
                item = random.choice(["Health Potion", "Ether Vial", "Smoke Bomb", "Shadow Oil"])
                player.inventory.append(item)
                slow_type(f"  You find a {item}!")
            elif roll < 0.65:
                g = random.randint(10, 25)
                player.gain_gold(g)
                slow_type(f"  {g} gold coins inside!")
            else:
                slow_type("  A curse! Your max HP drops by 10.")
                player.max_hp = max(20, player.max_hp - 10)
                player.hp = min(player.hp, player.max_hp)

    elif event == "old_soldier":
        slow_type("An old soldier sits by the road, sharpening a blade he'll never use again.")
        slow_type('  "I fought in the Shard Wars. Before Malachar. We thought we\'d won."')
        slow_type('  He looks at you. "Don\'t make the same mistakes we did."')
        choice = get_choice("Ask him about the Shard Wars?", ["Yes", "No time"])
        if choice == 1:
            slow_type('  "The Shards amplify whoever holds them. Good intentions aren\'t enough."')
            slow_type('  "Be careful what you want when you pick them up."')
            player.defence += 2
            slow_type("  His words ground you — Defence +2.")

    elif event == "starfall_crater":
        slow_type("A fresh crater smokes in the earth — a piece of void rock, still warm.")
        choice = get_choice("Touch it?", ["Yes", "No"])
        if choice == 1:
            if random.random() < 0.6:
                player.magic += 6
                slow_type("  Void energy surges through you — Magic +6!")
            else:
                dmg = random.randint(10, 25)
                player.hp = max(1, player.hp - dmg)
                slow_type(f"  The void energy burns you for {dmg} damage!")

    return None

def _shrine_bless(player, minor):
    boost = random.choice(["hp", "atk", "def", "mag"])
    if minor:
        amounts = {"hp": 15, "atk": 3, "def": 2, "mag": 4}
    else:
        amounts = {"hp": 25, "atk": 5, "def": 4, "mag": 7}
    amt = amounts[boost]
    if boost == "hp":
        player.max_hp += amt; player.hp = min(player.hp + amt, player.max_hp)
        slow_type(f"  The shrine glows — Max HP +{amt}!")
    elif boost == "atk":
        player.attack += amt; player.base_attack = player.attack
        slow_type(f"  The shrine glows — Attack +{amt}!")
    elif boost == "def":
        player.defence += amt
        slow_type(f"  The shrine glows — Defence +{amt}!")
    else:
        player.magic += amt
        slow_type(f"  The shrine glows — Magic +{amt}!")

def _visit_merchant(player):
    slow_type(f"  A travelling merchant grins at you.")
    slow_type(f"  Your gold: {player.gold}")
    shopping = True
    while shopping:
        options = [
            f"Health Potion — 8g (restore 50 HP)",
            f"Ether Vial — 10g (restore 40 MP)",
            f"Smoke Bomb — 6g (flee any battle)",
            f"Elixir of Fortitude — 25g (full restore)",
            f"Iron Charm — 15g (Defence +3 permanent)",
            f"War Sigil — 18g (Attack +4 permanent)",
            f"Arcane Crystal — 20g (Magic +5 permanent)",
            f"Leave",
        ]
        prices  = [8, 10, 6, 25, 15, 18, 20]
        items   = ["Health Potion","Ether Vial","Smoke Bomb","Elixir of Fortitude",None,None,None]
        choice = get_choice(f"Gold: {player.gold}", options)
        if choice == 8:
            shopping = False
        elif choice <= 4:
            cost = prices[choice-1]
            item = items[choice-1]
            if player.gold >= cost:
                player.gold -= cost
                player.inventory.append(item)
                slow_type(f"  Bought {item}! Gold: {player.gold}")
            else:
                slow_type("  Not enough gold.")
        elif choice == 5:
            if player.gold >= 15:
                player.gold -= 15; player.defence += 3
                slow_type(f"  Iron Charm equipped — Defence +3! (Now: {player.defence})")
            else:
                slow_type("  Not enough gold.")
        elif choice == 6:
            if player.gold >= 18:
                player.gold -= 18; player.attack += 4; player.base_attack = player.attack
                slow_type(f"  War Sigil etched — Attack +4! (Now: {player.attack})")
            else:
                slow_type("  Not enough gold.")
        elif choice == 7:
            if player.gold >= 20:
                player.gold -= 20; player.magic += 5
                slow_type(f"  Arcane Crystal absorbed — Magic +5! (Now: {player.magic})")
            else:
                slow_type("  Not enough gold.")

# ─────────────────────────────────────────────
#  SHOP BETWEEN ACTS
# ─────────────────────────────────────────────

def visit_shop(player, act_num):
    divider()
    slow_type(f"  Before Act {act_num} — a quiet moment to rest and resupply.")
    choice = get_choice("", ["Visit the trader", "Visit the crafting bench", "Check status & achievements", "Continue"])
    if choice == 1:
        _visit_merchant(player)
    elif choice == 2:
        crafting_menu(player)
        unlock_achievement(player, "crafter")
    elif choice == 3:
        player.status()
        show_achievements(player)
        show_bestiary(player)
    # Save checkpoint
    save_game(player, f"act_{act_num}")

# ─────────────────────────────────────────────
#  SIDE QUESTS (8 total)
# ─────────────────────────────────────────────

def sidequest_lost_child(player):
    divider()
    slow_type("SIDE QUEST: The Lost Child")
    slow_type("An old man grabs your sleeve. 'My granddaughter ran back inside!'")
    slow_type("He points to a burning house. You hear coughing within.")
    choice = get_choice("What do you do?", ["Rush inside to save her", "It's too dangerous — move on"])
    if choice == 1:
        slow_type("You sprint through smoke and find the girl huddled under a table.")
        slow_type("You carry her out.")
        slow_type('  [Grandfather]: "My father\'s blade — take it. Please."')
        player.attack += 6; player.base_attack = player.attack
        player.reputation += 2; player.quests_completed += 1
        slow_type("  [Attack +6, Reputation +2, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    else:
        slow_type("You walk past. The coughing fades.")
        player.reputation -= 1

def sidequest_forgotten_grave(player):
    divider()
    slow_type("SIDE QUEST: The Forgotten Grave")
    slow_type("A ghost flickers in the undercity corner.")
    slow_type('  [Ghost]: "My body was never buried. Will you help me rest?"')
    choice = get_choice("Do you help?", ["Yes — travel to the quarry", "No"])
    if choice == 2:
        slow_type("  The ghost fades. The undercity grows colder.")
        return None
    typewriter_pause("You travel to the old quarry and find the bones half-buried in rubble.")
    typewriter_pause("You dig carefully. You say the old words.")
    slow_type("  The ghost smiles, then fades.")
    slow_type('  [Ghost]: "Bless you. What I hid here — it\'s yours."')
    player.inventory.append("Elixir of Fortitude")
    player.reputation += 2; player.quests_completed += 1
    slow_type("  [Elixir of Fortitude obtained! Reputation +2, Quest complete!]")
    unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    slow_type("  But a Bone Golem stirs — the quarry had a guardian.")
    golem = Enemy("Bone Golem", hp=75, attack=16, defence=8, xp_reward=40, gold_drop=8,
                  lore="Ancient bones animated by residual void energy.", abilities=["shield"])
    r = combat(player, golem)
    if r == "lose": return "lose"
    return None

def sidequest_the_deserter(player):
    divider()
    slow_type("SIDE QUEST: The Deserter")
    slow_type("A soldier in Void Army armour steps out — hands raised.")
    slow_type('  "I deserted. I know where the next patrol will be. Let me go."')
    choice = get_choice("What do you do?", [
        "Let him go — take the information",
        "Bring him to justice",
        "Let him go — no conditions",
    ])
    if choice == 1:
        player.defence += 2
        player.quests_completed += 1; player.reputation += 1
        slow_type("  He tells you the patrol route. You avoid two ambushes. Defence +2.")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 2:
        slow_type("  He fights back.")
        d = Enemy("Void Deserter", hp=60, attack=14, defence=5, xp_reward=30, gold_drop=10)
        r = combat(player, d)
        if r == "lose": return "lose"
        player.reputation -= 1
    else:
        slow_type('  "...Thank you. Truly."')
        player.reputation += 3; player.quests_completed += 1
        slow_type("  [Reputation +3, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    return None

def sidequest_the_oracle(player):
    divider()
    slow_type("SIDE QUEST: The Oracle of Ironpeak")
    slow_type("An oracle lives in the ruined watchtower. She will speak only to you.")
    choice = get_choice("Seek her out?", ["Yes", "No — keep moving"])
    if choice == 2:
        return None
    typewriter_pause("You climb the tower. She sits with eyes closed.")
    slow_type('  [Oracle]: "I have waited for you. I will show you one truth."')
    choice = get_choice("What do you ask?", [
        "What is Malachar's greatest weakness?",
        "What is MY greatest weakness?",
        "Is there truly a way to save everyone?",
    ])
    if choice == 1:
        slow_type('  [Oracle]: "His grief. He loved this world. He still does."')
        player.attack += 5
        slow_type("  [Attack +5]")
    elif choice == 2:
        slow_type('  [Oracle]: "You move too fast. Knowing it may save you."')
        player.defence += 4
        slow_type("  [Defence +4]")
    else:
        slow_type('  [Oracle]: "Yes. But only if you believe it is possible."')
        player.max_hp += 20; player.hp = min(player.hp + 20, player.max_hp)
        slow_type("  [Max HP +20]")
    player.quests_completed += 1; player.reputation += 1
    slow_type("  [Reputation +1, Quest complete!]")
    unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    return None

def sidequest_the_twin_blades(player):
    """New Act II side quest — two rival mercenaries need arbitration."""
    divider()
    slow_type("SIDE QUEST: The Twin Blades")
    slow_type("Two mercenaries are arguing in the street — swords half-drawn.")
    slow_type('  [Renna]: "He owes me payment for the Duskmar job!"')
    slow_type('  [Tomas]: "She abandoned me mid-contract — I owe her nothing!"')
    choice = get_choice("How do you handle this?", [
        "Side with Renna — she was owed payment",
        "Side with Tomas — she broke the contract first",
        "Make them split the difference",
        "Walk away",
    ])
    if choice == 1:
        slow_type("  Tomas grudgingly pays. Renna thanks you and shares her intel.")
        player.attack += 3
        slow_type("  [Renna's tip sharpens your combat instincts — Attack +3]")
        player.quests_completed += 1; player.reputation += 1
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 2:
        slow_type("  Renna glares but accepts it. Tomas gives you a cut.")
        player.gain_gold(12)
        player.quests_completed += 1
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 3:
        slow_type("  Both mutter but agree. They shake hands — barely.")
        slow_type("  Both thank you in their own reluctant way.")
        player.gain_gold(6); player.reputation += 2; player.quests_completed += 1
        slow_type("  [Gold +6, Reputation +2, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    else:
        slow_type("  You walk away. Steel rings behind you. You don't look back.")

def sidequest_the_lighthouse(player):
    """New Act III side quest — a lighthouse keeper signals for help."""
    divider()
    slow_type("SIDE QUEST: The Lighthouse of Vaelcoast")
    slow_type("A lighthouse flickers on the shore — it shouldn't still be lit.")
    slow_type("A half-mad keeper greets you at the door.")
    slow_type('  [Keeper]: "Something\'s in the water. It\'s been circling for weeks."')
    choice = get_choice("What do you do?", [
        "Investigate the shore with him",
        "Search the lighthouse alone",
        "Tell him to leave — it's not safe",
    ])
    if choice == 1:
        slow_type("  You find a Void Leviathan carcass beached below — and survivors clinging to wreckage.")
        slow_type("  You help pull them in.")
        player.reputation += 2; player.quests_completed += 1
        slow_type("  [Reputation +2, Quest complete!]")
        player.inventory.append("Health Potion")
        player.inventory.append("Ether Vial")
        slow_type("  [The survivors share their supplies: Health Potion + Ether Vial]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 2:
        slow_type("  In the lamp room — a Void Shade has nested.")
        shade = Enemy("Void Shade", hp=65, attack=15, defence=6, xp_reward=35, gold_drop=10,
                      lore="A void creature drawn to light sources.", abilities=["drain"])
        r = combat(player, shade)
        if r == "lose": return "lose"
        player.quests_completed += 1; player.reputation += 1
        slow_type("  [Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    else:
        slow_type("  He nods, gathers his things, and goes.")
        slow_type("  You never learn what was in the water.")

def sidequest_the_arena(player):
    """New Act IV side quest — a hidden underground arena."""
    divider()
    slow_type("SIDE QUEST: The Arena of Broken Kings")
    slow_type("Word spreads of an underground arena in the Spire's lower levels.")
    slow_type("Fighters enter for glory. Or gold. Or both.")
    choice = get_choice("Do you enter?", ["Yes — fight for glory", "Yes — fight for the prize money", "No"])
    if choice == 3:
        return None

    slow_type("  Three bouts. Increasing difficulty.")
    rounds_won = 0

    opponents = [
        Enemy("Arena Grunt", hp=70, attack=16, defence=6, xp_reward=30, gold_drop=10),
        Enemy("Ironclad Champion", hp=100, attack=22, defence=12, xp_reward=50, gold_drop=20,
              lore="Undefeated in forty bouts. Until now, maybe.", abilities=["berserk"]),
        Enemy("The Warden", hp=140, attack=26, defence=15, xp_reward=80, gold_drop=40,
              lore="Nobody has beaten the Warden in three years.", abilities=["shield", "berserk"]),
    ]
    for opp in opponents:
        if not player.is_alive():
            break
        slow_type(f"\n  Next challenger: {opp.name}!")
        r = combat(player, opp)
        if r == "win":
            rounds_won += 1
        else:
            slow_type("  You have been defeated in the arena. You are carried out.")
            break

    if rounds_won == 3:
        slow_type("\n  The crowd erupts. You are undefeated.")
        prize = 50
        player.gain_gold(prize)
        player.attack += 4; player.base_attack = player.attack
        player.quests_completed += 1; player.reputation += 2
        slow_type(f"  [Arena Champion! Gold +{prize}, Attack +4, Reputation +2, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif rounds_won > 0:
        partial = rounds_won * 10
        player.gain_gold(partial)
        slow_type(f"  [{rounds_won} bouts won. Gold +{partial}]")

def sidequest_malachars_apprentice(player):
    """New Act V side quest — Malachar had a hidden apprentice who wants redemption."""
    divider()
    slow_type("SIDE QUEST: The Apprentice")
    slow_type("Outside the Throne of Ashes, a young woman in Void robes approaches.")
    slow_type('  "I was his apprentice. For twenty years."')
    slow_type('  "I never hurt anyone. I was a child when he found me. I had nowhere else to go."')
    slow_type('  "Please. I just want it to be over."')
    choice = get_choice("What do you say?", [
        '"Stand down. You\'re free."',
        '"Prove it — fight by my side against him."',
        '"I can\'t trust you. Leave."',
        '"Kneel. You answer for what he did."',
    ])
    if choice == 1:
        slow_type("  She exhales — years of tension leaving her at once.")
        slow_type("  She slips away into the grey. You hope she finds something better.")
        player.reputation += 2; player.quests_completed += 1
        slow_type("  [Reputation +2, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 2:
        slow_type("  She nods. In the final battle, she fights alongside you.")
        player.companions.append(Companion("Lyra", "Mage", attack=30, heal_power=0,
                                            dialogue=["For redemption!", "This is my choice!", "I am not him."]))
        player.quests_completed += 1; player.reputation += 1
        slow_type("  [Lyra joins as companion, Reputation +1, Quest complete!]")
        unlock_achievement(player, "all_quests") if player.quests_completed >= 4 else None
    elif choice == 3:
        slow_type("  She nods and walks away. You'll never know if you were right.")
    elif choice == 4:
        slow_type("  Her eyes go cold.")
        slow_type("  'I knew that was coming.'")
        app = Enemy("Void Apprentice", hp=90, attack=20, defence=8, xp_reward=55, gold_drop=15,
                    lore="She didn't want this. But you left her no choice.", abilities=["drain"])
        combat(player, app)

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

    sidequest_lost_child(player)

    typewriter_pause("Elder Mara grabs your arm.")
    slow_type('[Elder Mara]: "The prophecy child. The first Shard is beneath the temple."')
    slow_type('[Elder Mara]: "The Wraith Commander has already breached the gates. Go!"')
    pause()

    choice = get_choice("What do you do?", [
        "Rush to the temple",
        "Help the villagers first",
        "Ask Elder Mara about the Shards",
    ])
    if choice == 2:
        player.inventory.append("Health Potion")
        slow_type("  Grateful villagers hand you a Health Potion.")
    elif choice == 3:
        slow_type('[Elder Mara]: "Five Shards. Five Void Lords. Collect them all.')
        slow_type('  Reforge the Crystal Crown. End this. But beware — each Shard Malachar will feel."')
    pause()

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    divider()
    typewriter_pause("The temple crypt. Something stirs.")

    wc = Enemy("Void Wraith Commander", hp=70, attack=14, defence=4, xp_reward=40, gold_drop=8,
               lore="A Wraith Commander — towering, wreathed in smoke, absolutely ruthless.",
               abilities=["summon"])
    r = combat(player, wc)
    if r == "lose": return "lose"

    divider()
    typewriter_pause("At the base of the crypt — a faint blue glow.")
    typewriter_pause("The First Crystal Shard hums in your hand.")
    player.shards += 1; player.gain_gold(5)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    slow_type('[Malachar — distant]: "...Interesting. Come then, dust-child."')
    pause()

    visit_shop(player, 2)
    return "act_two"

def act_two(player):
    divider()
    slow_type("ACT II — THE IRON CITY OF DUSKMAR")
    pause()
    typewriter_pause("Duskmar. Iron walls. Tired people. A king who made a deal with darkness.")

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    choice = get_choice("How do you enter Duskmar?", [
        "Tell the truth — you seek the Shard",
        "Pose as a merchant",
        "Sneak through a side passage",
    ])
    if choice == 1:
        slow_type('  [Guard]: "The Shard?! Seize them!"')
        g = Enemy("City Guard", hp=50, attack=12, defence=6, xp_reward=20, gold_drop=6)
        if combat(player, g) == "lose": return "lose"
    elif choice == 3:
        if random.random() < 0.65:
            player.inventory.append("Health Potion")
            slow_type("  You find a Health Potion in the passage.")
        else:
            g = Enemy("City Patrol", hp=45, attack=13, defence=5, xp_reward=20, gold_drop=5)
            if combat(player, g) == "lose": return "lose"

    r = sidequest_forgotten_grave(player)
    if r == "lose" or not player.is_alive(): return "lose"

    sidequest_the_twin_blades(player)
    if not player.is_alive(): return "lose"

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    divider()
    slow_type("  Seraphine finds you in the undercity.")
    slow_type('[Seraphine]: "The Second Shard is in the king\'s vault. The Iron Golem guards it."')

    choice = get_choice("", ["Accept her help", "Go alone"])
    if choice == 1:
        player.inventory.append("Ether Vial")
        slow_type("  [Seraphine gives you an Ether Vial]")

    divider()
    typewriter_pause("The vault. The Shard glows amber. The floor shakes.")

    golem = Enemy("Iron Golem", hp=115, attack=18, defence=14, xp_reward=65, gold_drop=15,
                  lore="Built to never tire. Never flinch. Never fall.", abilities=["shield"])
    if combat(player, golem) == "lose": return "lose"

    player.shards += 1; player.gain_gold(8)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    slow_type('[Seraphine]: "Two down. Third Shard — the Sunken Ruins. East."')
    pause()

    visit_shop(player, 3)
    return "act_three"

def act_three(player):
    divider()
    slow_type("ACT III — THE SUNKEN RUINS OF VAEL'SHAR")
    pause()
    typewriter_pause("The Ashwood. Dead trees, grey sky, no birdsong.")

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    bandit = Enemy("Void-Touched Bandit", hp=80, attack=17, defence=7, xp_reward=45, gold_drop=10,
                   lore="A man consumed by void energy — hollow, desperate.", abilities=["poison"])
    if combat(player, bandit) == "lose": return "lose"

    r = sidequest_the_deserter(player)
    if r == "lose" or not player.is_alive(): return "lose"

    sidequest_the_lighthouse(player)
    if not player.is_alive(): return "lose"

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    divider()
    typewriter_pause("The Sunken Ruins. You wade into dark water.")
    typewriter_pause("A spirit appears — ancient, sorrowful.")
    slow_type('[Spirit of Vael\'shar]: "Answer me true: Why do you seek the Shards?"')

    choice = get_choice("", [
        "To save Eldoria and its people.",
        "For power.",
        "Because the prophecy chose me.",
        "To avenge those Malachar took from me.",
    ])
    if choice == 1:
        player.defence += 3; slow_type("[Defence +3]")
    elif choice == 2:
        player.attack += 4; slow_type("[Attack +4]")
    elif choice == 3:
        player.max_hp += 20; player.hp = min(player.hp+20, player.max_hp)
        slow_type("[Max HP +20]")
    else:
        player.magic += 8; slow_type("[Magic +8]")
    pause()

    typewriter_pause("A Void Serpent erupts from the water.")
    serpent = Enemy("Void Serpent", hp=100, attack=20, defence=6, xp_reward=60, gold_drop=12,
                    lore="Scales like obsidian, eyes like dying stars.", abilities=["poison", "drain"])
    if combat(player, serpent) == "lose": return "lose"

    player.shards += 1; player.gain_gold(10)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    typewriter_pause("Three down. The sky above Eldoria grows darker.")
    pause()

    visit_shop(player, 4)
    return "act_four"

def act_four(player):
    divider()
    slow_type("ACT IV — THE ARCANE SPIRE")
    pause()
    typewriter_pause("The Arcane Spire. A broken tooth on a mountaintop. Now Malachar's tower.")

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    r = sidequest_the_oracle(player)
    if r == "lose" or not player.is_alive(): return "lose"

    r = sidequest_the_arena(player)
    if r == "lose" or not player.is_alive(): return "lose"

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    typewriter_pause("At the summit gate — Void Lord Vareth waits.")
    vareth = Enemy("Void Lord Vareth", hp=135, attack=22, defence=10, xp_reward=90, gold_drop=20,
                   lore="Malachar's second-in-command. Tall, cold, utterly merciless.",
                   abilities=["berserk", "shield"])
    if combat(player, vareth) == "lose": return "lose"

    divider()
    slow_type('[Vareth, dying]: "You don\'t understand Malachar. He isn\'t destroying Eldoria.')
    slow_type('  He is trying... to save it. From something far worse."')
    typewriter_pause("He goes still. The gate opens.")

    choice = get_choice("What do you do?", [
        "Push forward — it's a trick.",
        "Search his body for answers.",
        "Sit with the doubt.",
    ])
    if choice == 2:
        slow_type("[You find Malachar's Journal]")
        player.inventory.append("Malachar's Journal")
        slow_type('  Entry: "The Void beyond the Veil is alive. If the Shards are reforged wrong,')
        slow_type('  they open a door that cannot be closed. I shattered them to keep it shut."')

    divider()
    typewriter_pause("The Fourth Shard pulses violet at the top of the Spire.")
    typewriter_pause("Malachar appears — in vision.")
    slow_type('[Malachar]: "The Void beyond the Veil is not nothing. It is alive. And hungry."')
    slow_type('[Malachar]: "If you reforge the Crown incorrectly, you feed it everything."')
    pause()

    choice = get_choice("How do you respond?", [
        '"Then show me the right way."',
        '"I don\'t believe you."',
        '"Why didn\'t you just tell someone?"',
    ])
    if choice == 3:
        slow_type('[Malachar]: "Because I am not good at trust. I never have been. I know that now."')
        slow_type("[His voice cracks — just slightly.]")

    typewriter_pause("The vision fades. You claim the Fourth Shard.")
    player.shards += 1; player.gain_gold(12)
    slow_type(f"  [Crystal Shard obtained — {player.shards}/5]")
    typewriter_pause("One remains. Malachar's throne room. The end of the world.")
    pause()

    visit_shop(player, 5)
    return "act_five"

def act_five(player):
    divider()
    slow_type("ACT V — THE THRONE OF ASHES")
    pause()
    typewriter_pause("The Throne of Ashes. Where the land ends and the Void begins.")
    typewriter_pause("The sky here is not black. It is nothing.")

    r = travel_event(player)
    if r == "lose" or not player.is_alive(): return "lose"

    sidequest_malachars_apprentice(player)
    if not player.is_alive(): return "lose"

    typewriter_pause("You walk toward the gate. Alone.")
    slow_type("  Malachar stands there. No guards. No tricks. He looks tired.")
    pause()
    slow_type('[Malachar]: "You made it. Four Shards. Almost there."')
    slow_type('[Malachar]: "Now comes the choice the prophecy never told you about."')
    pause()

    has_journal = "Malachar's Journal" in player.inventory
    is_hero = player.reputation >= 5 and player.quests_completed >= 3

    if is_hero:
        slow_type("[Malachar]: ...You're different. I can feel it in your choices.")
        slow_type("  Maybe there's a third way. One I never considered.")
        choice = get_choice("What do you do?", [
            "Fight Malachar by force.",
            "Let Malachar sacrifice himself.",
            "Offer your own life.",
            "Forge a new Shard together from your shared will.",
        ])
    elif has_journal:
        slow_type('[Malachar]: "You read the journal. Then you know the cost."')
        slow_type('[Malachar]: "One life. Mine. Or yours."')
        choice = get_choice("What do you choose?", [
            "Fight Malachar by force.",
            "Let Malachar sacrifice himself.",
            "Offer your own life.",
            "Find a way together.",
        ])
    else:
        slow_type('[Malachar]: "I think you\'d rather fight. So let\'s end it."')
        choice = get_choice("What do you do?", [
            "Fight Malachar.",
            "Demand answers first.",
            "Lower your weapon. Talk.",
        ])

    divider()

    if choice == 1:
        slow_type('[Malachar]: "Very well."')
        boss = Enemy("Malachar, the Last Sorcerer", hp=200, attack=28, defence=12,
                     xp_reward=200, gold_drop=0,
                     lore="He is not a monster. He is a man who made terrible choices for reasons he believed were right. That makes him more dangerous.",
                     abilities=["drain", "shield", "berserk"])
        if combat(player, boss) == "lose": return "lose"
        player.shards = 5
        return "ending_victory_blood"

    elif choice == 2 and (has_journal or is_hero):
        slow_type('[Malachar]: "...Thank you. I hoped."')
        typewriter_pause("He walks to the edge of the Void. He speaks words older than language.")
        typewriter_pause("The Void closes. Malachar with it.")
        player.shards = 5
        return "ending_redemption"

    elif choice == 3 and (has_journal or is_hero):
        slow_type('[Malachar]: "No. Absolutely not. You have a future. I lost mine a century ago."')
        typewriter_pause("He takes the Shards before you can stop him.")
        typewriter_pause("He walks into the Void. He does not look back.")
        player.shards = 5
        return "ending_redemption"

    elif choice == 4 and is_hero:
        typewriter_pause("Malachar stares — genuinely stunned.")
        slow_type('[Malachar]: "A new Shard... forged from will? That\'s not... possible."')
        slow_type('[Malachar]: "...Is it?"')
        typewriter_pause("You place your hand over his. The four Shards glow between you.")
        typewriter_pause("Every person you helped. Every choice toward light. It becomes real.")
        typewriter_pause("A Sixth Shard — born not from the old world, but from this one.")
        slow_type('[Malachar]: "I never believed this was possible. I do now."')
        player.shards = 5
        unlock_achievement(player, "secret_ending")
        return "ending_transcendence"

    else:
        slow_type('[Malachar]: "The Void is alive. It waits for the Crown to be reforged wrong."')
        slow_type('[Malachar]: "I shattered the Shards to keep it closed. For one hundred years. Alone."')
        choice2 = get_choice("", ["Fight him.", "Work with him."])
        if choice2 == 1:
            boss = Enemy("Malachar, the Last Sorcerer", hp=200, attack=28, defence=12,
                         xp_reward=200, gold_drop=0,
                         lore="Even now, he holds back.",
                         abilities=["drain", "shield"])
            if combat(player, boss) == "lose": return "lose"
            player.shards = 5
            return "ending_victory_blood"
        else:
            typewriter_pause("You stand at the edge of the Void. Together.")
            typewriter_pause("The Void screams. It nearly takes you both. But it closes.")
            player.shards = 5
            return "ending_alliance"

# ─────────────────────────────────────────────
#  ENDINGS (5 total)
# ─────────────────────────────────────────────

def ending_victory_blood(player):
    divider()
    slow_type("ENDING I: THE WARRIOR'S CROWN")
    pause()
    slow_type("You stood alone against the darkness and won.")
    slow_type("Malachar is dead. Eldoria will heal.")
    slow_type("They will sing songs about you for a thousand years.")
    pause()
    slow_type("But sometimes, in the quiet, you wonder.")
    slow_type("Whether the door is truly closed. Or just... waiting.")
    _final_stats(player, "THE WARRIOR'S CROWN")

def ending_redemption(player):
    divider()
    slow_type("ENDING II: THE PRICE OF MERCY")
    pause()
    slow_type("You gave a broken man the chance to become something better.")
    slow_type("In his final act, Malachar sealed the Void — and atoned for a century of darkness.")
    slow_type("Eldoria will never know his name was whispered in kindness at the end.")
    slow_type("But you know. And that is enough.")
    _final_stats(player, "THE PRICE OF MERCY")

def ending_alliance(player):
    divider()
    slow_type("ENDING III: THE UNLIKELY ALLIANCE")
    pause()
    slow_type("You chose trust when distrust would have been easier.")
    slow_type("Together, you and Malachar sealed the Void.")
    slow_type("He survived — barely. Changed. Not good, not yet. But no longer lost.")
    slow_type("The sun rises over Eldoria without shadows. For the first time in a century.")
    _final_stats(player, "THE UNLIKELY ALLIANCE")

def ending_transcendence(player):
    divider()
    slow_type("ENDING IV: THE SIXTH SHARD  ★ SECRET ENDING ★")
    pause()
    slow_type("You didn't just save the world.")
    slow_type("You changed what the world believes is possible.")
    pause()
    slow_type("The Sixth Shard — born from human will and compassion — now floats above Eldoria.")
    slow_type("It belongs to no one. It belongs to everyone.")
    pause()
    slow_type("Malachar lived. Seraphine rebuilt Duskmar.")
    slow_type("The ghost rested. The deserter went home.")
    slow_type("All of them — because you chose, again and again, to care.")
    slow_type("That is not a small thing. That is everything.")
    _final_stats(player, "THE SIXTH SHARD  ★ SECRET ENDING ★")

def ending_dark(player):
    """Only reached if the player consistently chose cruel options."""
    divider()
    slow_type("ENDING V: THE VOID KING  ★ DARK ENDING ★")
    pause()
    slow_type("You took the Shards. All of them.")
    slow_type("You did not reforge the Crown. You held them — all five — and felt the door open.")
    pause()
    slow_type("The Void did not take you. It recognised you.")
    slow_type("A century from now, someone will be born into your ash.")
    slow_type("They will read a prophecy carved into a throne. Your throne.")
    slow_type("And they will wonder what kind of soul rises to face you.")
    _final_stats(player, "THE VOID KING  ★ DARK ENDING ★")

def _final_stats(player, ending_name):
    title = get_title(player)
    divider()
    slow_type(f"  {player.name} {title} | {player.cls} | Level {player.level}")
    slow_type(f"  Shards: {player.shards}/5  |  Quests: {player.quests_completed}  |  Reputation: {player.reputation}")
    ach = getattr(player, 'achievements', set())
    slow_type(f"  Achievements: {len(ach)}/{len(ACHIEVEMENTS)}")
    slow_type(f"  Ending: {ending_name}")
    divider()

def ending_lose(player):
    divider()
    slow_type("The darkness takes you.")
    pause()
    slow_type("The Void does not gloat. It simply... absorbs.")
    slow_type(f"  {player.name} the {player.cls} fell before the world could be saved.")
    slow_type("  The story is not over. But your part in it is.")
    slow_type("\n  [Your save file is still here — you can load and try again.]")
    divider()

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
#  MAIN MENU
# ─────────────────────────────────────────────

def main():
    clear()
    slow_type("╔════════════════════════════════════════════════════╗")
    slow_type("║        E L D O R I A   C H R O N I C L E S        ║")
    slow_type("║        A Story of Shards, Shadows & Sacrifice      ║")
    slow_type("║                  — Expanded Edition —              ║")
    slow_type("╚════════════════════════════════════════════════════╝")
    pause()

    while True:
        options = ["New Game", "Load Game", "View Achievements (last run)", "Quit"]
        mode = get_choice("\nMain Menu", options)

        if mode == 4:
            slow_type("Until next time, traveller.")
            break

        elif mode == 2:
            player, act = load_game()
            if not player:
                slow_type("  No save file found. Starting a new game.")
                mode = 1
            else:
                slow_type(f"  Loaded: {player.name} the {player.cls}, Level {player.level}, Act {act}")
                pause()

        elif mode == 3:
            if os.path.exists(SAVE_FILE):
                p, _ = load_game()
                if p:
                    show_achievements(p)
                    show_bestiary(p)
            else:
                slow_type("  No save data found.")
            continue

        if mode == 1:
            divider()
            slow_type("PROLOGUE — THE WORLD BEFORE\n")
            for line in LORE_INTRO:
                slow_type(line)
                pause(0.5)

            name = get_name()
            cls_name, stats = pick_class()
            player = Player(name, cls_name, stats)
            act = "act_one"

            divider()
            slow_type(f'  "{player.lore}"')
            pause()
            slow_type(f"  Your name is {player.name}.")
            slow_type(f"  You are a {player.cls}.")
            slow_type("  And the world is ending.")
            pause(1.5)

        # Run from current act
        act_map = {
            "act_one": act_one,
            "act_two": act_two,
            "act_three": act_three,
            "act_four": act_four,
            "act_five": act_five,
        }
        act_order = ["act_one", "act_two", "act_three", "act_four", "act_five"]
        start_index = act_order.index(act) if act in act_order else 0

        state = None
        for act_key in act_order[start_index:]:
            state = act_map[act_key](player)
            if state == "lose" or not player.is_alive():
                state = "lose"
                break

        # Dark ending check
        if state not in ("lose",) and player.reputation <= -5:
            state = "ending_dark"

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
        elif state == "ending_dark":
            ending_dark(player)

        # Final achievement checks
        if player.reputation >= 8:
            unlock_achievement(player, "high_rep")
        if player.quests_completed >= 4:
            unlock_achievement(player, "all_quests")

        again = get_choice("\nPlay again?", ["Yes", "No"])
        if again == 2:
            slow_type("May your next journey be a worthy one. Farewell.")
            break

if __name__ == "__main__":
    main()
