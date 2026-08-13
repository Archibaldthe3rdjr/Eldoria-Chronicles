import json
import os
import random
import tempfile
import time
from copy import deepcopy

# ELDORIA CHRONICLES — STABLE EDITION
# Standard-library only.
# Fixes: safe saves, robust loading, non-stacking temporary buffs,
# cloned companions, multi-level XP, consistent achievements, and cleaner input.

SAVE_FILE = "eldoria_save.json"
SAVE_VERSION = 2


def slow_type(text, delay=0.04):
    for char in str(text):
        print(char, end="", flush=True)
        if delay:
            time.sleep(delay)
    print()


def pause(seconds=1.0):
    if seconds:
        time.sleep(seconds)


def divider():
    print("\n" + "═" * 52 + "\n")


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def get_choice(prompt, options):
    while True:
        if prompt:
            slow_type(prompt)
        for number, option in enumerate(options, 1):
            print(f"  {number}. {option}")
        answer = input("\n> ").strip()
        if answer.isdigit():
            choice = int(answer)
            if 1 <= choice <= len(options):
                return choice
        slow_type("  Please enter a valid number.")


def typewriter_pause(text, delay=0.04, after=0.8):
    slow_type(text, delay)
    pause(after)


WEATHERS = [
    ("Clear skies", "The sun is pale but present.", 0, 0),
    ("Heavy rain", "Rain hammers the earth. Visibility drops.", -2, 0),
    ("Ash storm", "Void ash fills the air.", -3, -2),
    ("Eerie fog", "Thick fog clings to everything.", 0, 2),
    ("Blood moon", "A crimson moon hangs low.", 0, 5),
    ("Gentle wind", "A warm breeze carries old flowers.", 2, 0),
    ("Lightning storm", "Magic crackles in the air.", 5, 0),
]


def get_weather():
    return random.choice(WEATHERS)


def announce_weather(weather):
    name, description, magic_bonus, enemy_bonus = weather
    slow_type(f"\n  [Weather: {name}]")
    slow_type(f"  {description}")
    if magic_bonus:
        slow_type(f"  Magic is {'boosted' if magic_bonus > 0 else 'weakened'} by {abs(magic_bonus)}.")
    if enemy_bonus:
        slow_type(f"  Enemies are {'stronger' if enemy_bonus > 0 else 'weaker'} by {abs(enemy_bonus)}.")


RECIPES = {
    "Mega Potion": ({"Health Potion": 2}, "Restores 120 HP"),
    "Arcane Brew": ({"Ether Vial": 2}, "Restores full MP"),
    "Void Flask": ({"Health Potion": 1, "Ether Vial": 1}, "Restores 60 HP and 30 MP"),
    "Elixir of Fortitude": ({"Mega Potion": 1, "Arcane Brew": 1}, "Fully restores HP and MP"),
    "Shadow Oil": ({"Smoke Bomb": 1, "Ether Vial": 1}, "Next attack deals double damage"),
}

ACHIEVEMENTS = {
    "first_blood": ("First Blood", "Win your first combat."),
    "pacifist": ("Pacifist", "Complete an act without fleeing or losing."),
    "hoarder": ("Hoarder", "Carry 6+ items at once."),
    "rich": ("Merchant Prince", "Accumulate 100+ gold."),
    "crafter": ("Alchemist", "Craft your first item."),
    "max_level": ("Legend", "Reach level 10."),
    "secret_ending": ("The Sixth Shard", "Unlock the secret ending."),
    "all_quests": ("True Hero", "Complete all 8 side quests."),
    "high_rep": ("Saint of Eldoria", "Reach reputation 8+."),
    "bestiary_master": ("Monster Hunter", "Defeat 10 different enemy types."),
}

LORE_INTRO = [
    "In the beginning, there was light.",
    "Five Crystal Shards — each holding a fragment of creation — floated above Eldoria.",
    "Then came Malachar, once the greatest sorcerer who ever lived.",
    "He shattered the Shards one hundred years ago.",
    "You were born into the ash.",
    "A prophecy says one soul from the dust shall rise — and either save the world, or end it.",
    "That soul is you.",
]

CLASSES = {
    "Knight of Ashenveil": {"hp": 140, "mp": 30, "attack": 22, "defence": 12, "magic": 5,
        "skill": "Rallying Cry", "skill_desc": "Heal 25 HP and gain +5 Attack for 3 rounds.",
        "lore": "The last knight of Ashenveil."},
    "Shadowblade": {"hp": 100, "mp": 50, "attack": 35, "defence": 6, "magic": 10,
        "skill": "Void Step", "skill_desc": "A guaranteed critical hit.",
        "lore": "Shadows are your home."},
    "Arcanist": {"hp": 85, "mp": 120, "attack": 12, "defence": 4, "magic": 45,
        "skill": "Starfall", "skill_desc": "Powerful magic attack costing 30 MP.",
        "lore": "Magic flows through your blood."},
    "Warden of the Wild": {"hp": 115, "mp": 80, "attack": 18, "defence": 9, "magic": 20,
        "skill": "Nature's Wrath", "skill_desc": "Damage and stun an enemy for 2 turns.",
        "lore": "The forests still live. You speak for them."},
    "Paladin of the Eternal Flame": {"hp": 130, "mp": 70, "attack": 20, "defence": 11, "magic": 25,
        "skill": "Divine Smite", "skill_desc": "Triple magic damage and heal 20 HP.",
        "lore": "You carry the gods' last ember."},
    "Necromancer": {"hp": 90, "mp": 100, "attack": 15, "defence": 5, "magic": 40,
        "skill": "Soul Drain", "skill_desc": "Deal magic damage and heal for half the damage.",
        "lore": "Death is a weapon you understand."},
    "Beastcaller": {"hp": 110, "mp": 90, "attack": 16, "defence": 8, "magic": 18,
        "skill": "Summon Pack", "skill_desc": "Summon a wolf for 3 rounds.",
        "lore": "Civilisation is a foreign language."},
    "Runeblade": {"hp": 120, "mp": 60, "attack": 24, "defence": 10, "magic": 22,
        "skill": "Runic Surge", "skill_desc": "Random fire, ice, or thunder effect.",
        "lore": "You have carved runes since childhood."},
}


class Companion:
    def __init__(self, name, role, attack, heal_power, dialogue):
        self.name = name
        self.role = role
        self.attack = attack
        self.heal_power = heal_power
        self.dialogue = list(dialogue)
        self.cooldown = 0

    def clone(self):
        return Companion(self.name, self.role, self.attack, self.heal_power, self.dialogue)

    def act(self, player, enemy):
        if self.cooldown:
            self.cooldown -= 1
            return
        roll = random.random()
        if roll < 0.4:
            damage = max(1, self.attack + random.randint(-3, 3) - enemy.defence)
            enemy.hp = max(0, enemy.hp - damage)
            slow_type(f"  [{self.name}] attacks for {damage} damage!")
        elif roll < 0.6 and self.heal_power and player.hp < player.max_hp * 0.5:
            healed = player.heal(self.heal_power)
            slow_type(f"  [{self.name}] heals you for {healed} HP!")
        else:
            slow_type(f'  [{self.name}]: "{random.choice(self.dialogue)}"')
        self.cooldown = random.randint(1, 2)


COMPANIONS_POOL = [
    Companion("Seraphine", "Warrior", 18, 0, ["Hold the line!", "For Eldoria!"]),
    Companion("Elder Mara", "Healer", 5, 30, ["Stay strong, child.", "I believe in you."]),
    Companion("Kael", "Rogue", 25, 0, ["Shadow and silence.", "Don't blink."]),
    Companion("Lyra", "Mage", 30, 0, ["The stars align!", "Feel the power of the Spire!"]),
]


def companion_by_name(name):
    for companion in COMPANIONS_POOL:
        if companion.name == name:
            return companion.clone()
    return None


class Player:
    def __init__(self, name, cls_name, stats):
        self.name = name
        self.cls = cls_name
        self.max_hp = stats["hp"]
        self.hp = self.max_hp
        self.max_mp = stats["mp"]
        self.mp = self.max_mp
        self.attack = stats["attack"]
        self.base_attack = self.attack
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
        self.shadow_oil_active = False

    def is_alive(self):
        return self.hp > 0

    def heal(self, amount):
        healed = min(max(0, amount), self.max_hp - self.hp)
        self.hp += healed
        return healed

    def gain_gold(self, amount):
        self.gold += amount
        if self.gold >= 100:
            unlock_achievement(self, "rich")

    def gain_xp(self, amount):
        self.xp += amount
        slow_type(f"  [+{amount} XP — {self.xp}/{self.xp_needed}]")
        while self.xp >= self.xp_needed and self.level < 10:
            self.xp -= self.xp_needed
            self.level_up()
        if self.level >= 10:
            unlock_achievement(self, "max_level")

    def level_up(self):
        self.level += 1
        self.xp_needed = int(self.xp_needed * 1.6)
        hp_gain = random.randint(10, 20)
        atk_gain = random.randint(2, 5)
        mp_gain = random.randint(5, 12)
        self.max_hp += hp_gain
        self.hp += hp_gain
        self.max_mp += mp_gain
        self.mp += mp_gain
        self.base_attack += atk_gain
        self.attack += atk_gain
        divider()
        slow_type(f"LEVEL UP! You are now Level {self.level}!")
        slow_type(f"  HP +{hp_gain} | ATK +{atk_gain} | MP +{mp_gain}")

    def status(self):
        print(f"\n  {self.name} the {get_title(self)} | {self.cls} | Lv.{self.level}")
        print(f"  HP {self.hp}/{self.max_hp} | MP {self.mp}/{self.max_mp}")
        print(f"  ATK {self.attack} | DEF {self.defence} | MAG {self.magic}")
        print(f"  Shards {self.shards}/5 | Gold {self.gold} | Reputation {self.reputation}")
        print(f"  XP {self.xp}/{self.xp_needed} | Quests {self.quests_completed}/8")
        if self.companions:
            print("  Companions: " + ", ".join(c.name for c in self.companions))
        if self.inventory:
            print("  Inventory: " + ", ".join(self.inventory))


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
        self.abilities = list(abilities or [])
        self.weakened = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        actual = max(1, damage - (0 if self.weakened else self.defence))
        self.hp = max(0, self.hp - actual)
        return actual

    def ai_attack(self, player):
        if self.stunned:
            self.stun_turns -= 1
            if self.stun_turns <= 0:
                self.stunned = False
            slow_type(f"  {self.name} is stunned and cannot act!")
            return
        base = self.attack
        roll = random.random()
        if self.abilities and roll < 0.25:
            ability = random.choice(self.abilities)
            if ability == "poison":
                damage = max(1, base // 2 - player.defence)
                player.hp = max(0, player.hp - damage)
                slow_type(f"  {self.name} hits with a lingering effect for {damage} damage!")
            elif ability == "drain":
                damage = max(1, base - player.defence)
                player.hp = max(0, player.hp - damage)
                self.hp = min(self.max_hp, self.hp + damage // 2)
                slow_type(f"  {self.name} drains {damage} HP and restores {damage // 2}!")
            elif ability == "shield":
                self.defence += 3
                slow_type(f"  {self.name} raises a shield. Defence +3!")
            elif ability == "berserk":
                self.attack += 4
                slow_type(f"  {self.name} becomes enraged. Attack +4!")
            elif ability == "summon":
                damage = max(1, 8 - player.defence)
                player.hp = max(0, player.hp - damage)
                slow_type(f"  {self.name} calls a helper. You take {damage} damage!")
        elif roll < 0.2:
            damage = max(1, int(base * 1.8) + random.randint(0, 8) - player.defence)
            player.hp = max(0, player.hp - damage)
            slow_type(f"  {self.name} lands a heavy strike for {damage}!")
        else:
            damage = max(1, base + random.randint(-4, 4) - player.defence)
            player.hp = max(0, player.hp - damage)
            slow_type(f"  {self.name} attacks for {damage} damage!")


def unlock_achievement(player, key):
    if key not in ACHIEVEMENTS or key in player.achievements:
        return
    player.achievements.add(key)
    name, description = ACHIEVEMENTS[key]
    slow_type(f"\n  ★ ACHIEVEMENT: {name} — {description}")


def record_kill(player, enemy_name):
    player.bestiary[enemy_name] = player.bestiary.get(enemy_name, 0) + 1


def get_title(player):
    if player.reputation >= 8:
        return "the Beloved"
    if player.reputation <= -4:
        return "the Ruthless"
    if player.level >= 10:
        return "the Legendary"
    if player.quests_completed >= 8:
        return "the True Hero"
    if player.shards >= 3:
        return "the Shard-Bearer"
    if player.level >= 5:
        return "the Seasoned"
    return "the Wanderer"


def save_game(player, act_name):
    data = {
        "version": SAVE_VERSION,
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
        "inventory": list(player.inventory),
        "gold": player.gold,
        "level": player.level,
        "xp": player.xp,
        "xp_needed": player.xp_needed,
        "quests_completed": player.quests_completed,
        "reputation": player.reputation,
        "achievements": sorted(player.achievements),
        "bestiary": dict(player.bestiary),
        "companions": [c.name for c in player.companions],
        "act": act_name,
        "attack_boost": player.attack_boost,
        "attack_boost_rounds": player.attack_boost_rounds,
        "wolf_summon_rounds": player.wolf_summon_rounds,
        "shadow_oil_active": player.shadow_oil_active,
    }
    directory = os.path.dirname(os.path.abspath(SAVE_FILE)) or "."
    fd, temp_path = tempfile.mkstemp(prefix="eldoria_", suffix=".tmp", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, SAVE_FILE)
        slow_type("  [Game saved.]" )
    except OSError as exc:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        slow_type(f"  [Could not save game: {exc}]")


def load_game():
    if not os.path.exists(SAVE_FILE):
        return None, None
    try:
        with open(SAVE_FILE, encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict):
            raise ValueError("save data is not an object")
        cls_name = data["cls"]
        stats = dict(CLASSES.get(cls_name, {}))
        if not stats:
            stats = {"hp": data["max_hp"], "mp": data["max_mp"], "attack": data["base_attack"],
                     "defence": data["defence"], "magic": data["magic"], "skill": data["skill"],
                     "skill_desc": data["skill_desc"], "lore": data.get("lore", "")}
        player = Player(data["name"], cls_name, stats)
        for attr in ("hp", "max_hp", "mp", "max_mp", "attack", "base_attack", "defence", "magic",
                     "shards", "gold", "level", "xp", "xp_needed", "quests_completed", "reputation",
                     "attack_boost", "attack_boost_rounds", "wolf_summon_rounds"):
            if attr in data:
                setattr(player, attr, data[attr])
        player.inventory = list(data.get("inventory", []))
        player.achievements = set(data.get("achievements", [])) & set(ACHIEVEMENTS)
        player.bestiary = dict(data.get("bestiary", {}))
        player.shadow_oil_active = bool(data.get("shadow_oil_active", False))
        player.companions = []
        for name in data.get("companions", []):
            companion = companion_by_name(name)
            if companion:
                player.companions.append(companion)
        act = data.get("act", "act_one")
        if act not in {"act_one", "act_two", "act_three", "act_four", "act_five"}:
            act = "act_one"
        return player, act
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        slow_type(f"  [Save file could not be loaded: {exc}]")
        return None, None


def use_item(player, enemy):
    usable_names = {"Health Potion", "Ether Vial", "Smoke Bomb", "Elixir of Fortitude",
                    "Mega Potion", "Arcane Brew", "Void Flask", "Shadow Oil"}
    usable = [item for item in player.inventory if item in usable_names]
    if not usable:
        slow_type("  You have no usable items!")
        return False
    choice = get_choice("Use which item?", usable + ["Cancel"])
    if choice == len(usable) + 1:
        return False
    item = usable[choice - 1]
    player.inventory.remove(item)
    if item == "Health Potion":
        slow_type(f"  +{player.heal(50)} HP")
    elif item == "Mega Potion":
        slow_type(f"  +{player.heal(120)} HP")
    elif item == "Ether Vial":
        gain = min(40, player.max_mp - player.mp)
        player.mp += gain
        slow_type(f"  +{gain} MP")
    elif item == "Arcane Brew":
        gain = player.max_mp - player.mp
        player.mp = player.max_mp
        slow_type(f"  Full MP restored (+{gain}).")
    elif item == "Void Flask":
        hp = player.heal(60)
        mp = min(30, player.max_mp - player.mp)
        player.mp += mp
        slow_type(f"  +{hp} HP, +{mp} MP")
    elif item == "Smoke Bomb":
        slow_type("  You escape safely!")
        return "fled"
    elif item == "Elixir of Fortitude":
        player.hp = player.max_hp
        player.mp = player.max_mp
        slow_type("  Fully restored!")
    elif item == "Shadow Oil":
        player.shadow_oil_active = True
        slow_type("  Your next basic attack deals double damage!")
    if len(player.inventory) >= 6:
        unlock_achievement(player, "hoarder")
    return True


def player_turn(player, enemy, weather):
    _, _, magic_bonus, _ = weather
    actions = ["Basic Attack", f"Skill: {player.skill}", "Use Item", "Check Status", "Flee (50%)"]
    choice = get_choice(f"\n{player.name}'s turn:", actions)
    if choice == 1:
        damage = player.attack + random.randint(-4, 6)
        if player.shadow_oil_active:
            damage *= 2
            player.shadow_oil_active = False
            slow_type("  Shadow Oil activates — DOUBLE DAMAGE!")
        dealt = enemy.take_damage(damage)
        slow_type(f"  You deal {dealt} damage. Enemy HP: {enemy.hp}")
    elif choice == 2:
        if player.cls == "Knight of Ashenveil":
            player.hp = min(player.max_hp, player.hp + 25)
            # Recalculate the temporary attack bonus from base_attack so it cannot stack.
            player.attack = player.base_attack + 5
            player.attack_boost = 5
            player.attack_boost_rounds = 3
            slow_type("  Rallying Cry! +25 HP and +5 Attack for 3 rounds.")
        elif player.cls == "Shadowblade":
            dealt = enemy.take_damage(player.attack * 4)
            slow_type(f"  Void Step deals {dealt} damage!")
        elif player.cls == "Arcanist":
            if player.mp < 30:
                slow_type("  Not enough MP.")
                return None
            player.mp -= 30
            dealt = enemy.take_damage(player.magic + magic_bonus + 20)
            slow_type(f"  Starfall deals {dealt} damage!")
        elif player.cls == "Warden of the Wild":
            dealt = enemy.take_damage(25)
            enemy.stunned = True
            enemy.stun_turns = 2
            slow_type(f"  Nature's Wrath deals {dealt} damage and roots the enemy!")
        elif player.cls == "Paladin of the Eternal Flame":
            dealt = enemy.take_damage((player.magic + magic_bonus) * 3)
            slow_type(f"  Divine Smite deals {dealt} damage and heals {player.heal(20)} HP!")
        elif player.cls == "Necromancer":
            dealt = enemy.take_damage(45 + magic_bonus)
            slow_type(f"  Soul Drain deals {dealt} damage and heals {player.heal(dealt // 2)} HP!")
        elif player.cls == "Beastcaller":
            player.wolf_summon_rounds = max(player.wolf_summon_rounds, 3)
            slow_type("  A wolf joins the fight for 3 rounds!")
        elif player.cls == "Runeblade":
            rune = random.choice(("Fire", "Ice", "Thunder"))
            if rune == "Fire":
                slow_type(f"  Fire Rune deals {enemy.take_damage(35 + magic_bonus)} damage!")
            elif rune == "Ice":
                dealt = enemy.take_damage(20)
                enemy.stunned = True
                enemy.stun_turns = 1
                slow_type(f"  Ice Rune deals {dealt} damage and stuns!")
            else:
                dealt = enemy.take_damage(25)
                enemy.weakened = True
                slow_type(f"  Thunder Rune deals {dealt} damage and weakens defence!")
    elif choice == 3:
        result = use_item(player, enemy)
        if result == "fled":
            return "fled"
        if not result:
            return None
    elif choice == 4:
        player.status()
        return None
    else:
        if random.random() < 0.5:
            slow_type("  You escaped!")
            return "fled"
        slow_type("  You could not escape!")

    if player.wolf_summon_rounds > 0 and enemy.is_alive():
        damage = max(1, 15 - enemy.defence)
        enemy.hp = max(0, enemy.hp - damage)
        player.wolf_summon_rounds -= 1
        slow_type(f"  [Wolf] deals {damage} damage!")

    for companion in player.companions:
        if enemy.is_alive():
            companion.act(player, enemy)

    if player.attack_boost_rounds > 0:
        player.attack_boost_rounds -= 1
        if player.attack_boost_rounds == 0:
            player.attack = player.base_attack
            player.attack_boost = 0
            slow_type("  Rallying Cry fades.")
    return None


def combat(player, enemy, weather=None):
    weather = weather or get_weather()
    _, _, _, enemy_bonus = weather
    original_attack = enemy.attack
    enemy.attack = original_attack + enemy_bonus
    divider()
    announce_weather(weather)
    if enemy.lore:
        slow_type(f"\n  {enemy.lore}")
    slow_type(f"\n⚔ {enemy.name} | HP {enemy.hp} | ATK {enemy.attack} | DEF {enemy.defence}")
    round_number = 1
    try:
        while player.is_alive() and enemy.is_alive():
            slow_type(f"\n--- Round {round_number} | HP {player.hp}/{player.max_hp} | MP {player.mp}/{player.max_mp} ---")
            if player.stunned:
                player.stunned = False
                slow_type("  You are stunned and lose this turn!")
            else:
                result = player_turn(player, enemy, weather)
                if result == "fled":
                    return "fled"
            if enemy.is_alive():
                enemy.ai_attack(player)
            round_number += 1
    finally:
        enemy.attack = original_attack
    if player.is_alive():
        slow_type(f"\n✓ {enemy.name} defeated!")
        record_kill(player, enemy.name)
        player.gain_xp(enemy.xp_reward)
        if enemy.gold_drop:
            player.gain_gold(random.randint(max(1, enemy.gold_drop // 2), enemy.gold_drop))
        unlock_achievement(player, "first_blood")
        if len(player.bestiary) >= 10:
            unlock_achievement(player, "bestiary_master")
        return "win"
    return "lose"


def crafting_menu(player):
    divider()
    slow_type("CRAFTING")
    entries = list(RECIPES.items())
    options = []
    for name, (ingredients, description) in entries:
        can_craft = all(player.inventory.count(item) >= amount for item, amount in ingredients.items())
        mark = "✓" if can_craft else "✗"
        req = ", ".join(f"{amount}x {item}" for item, amount in ingredients.items())
        options.append(f"{mark} {name} ({req}) — {description}")
    options.append("Leave")
    choice = get_choice("", options)
    if choice == len(options):
        return
    name, (ingredients, _) = entries[choice - 1]
    if not all(player.inventory.count(item) >= amount for item, amount in ingredients.items()):
        slow_type("  Missing ingredients.")
        return
    for item, amount in ingredients.items():
        for _ in range(amount):
            player.inventory.remove(item)
    player.inventory.append(name)
    unlock_achievement(player, "crafter")
    slow_type(f"  Crafted {name}!")


def _shrine_bless(player, minor):
    amounts = {"hp": (15, 25), "atk": (3, 5), "def": (2, 4), "mag": (4, 7)}
    stat = random.choice(tuple(amounts))
    amount = amounts[stat][0 if minor else 1]
    if stat == "hp":
        player.max_hp += amount
        player.hp += amount
    elif stat == "atk":
        player.base_attack += amount
        player.attack += amount
    elif stat == "def":
        player.defence += amount
    else:
        player.magic += amount
    slow_type(f"  Shrine blessing: {stat.upper()} +{amount}.")


def merchant(player):
    while True:
        options = [
            "Health Potion — 8g", "Ether Vial — 10g", "Smoke Bomb — 6g",
            "Elixir of Fortitude — 25g", "Iron Charm — 15g", "War Sigil — 18g",
            "Arcane Crystal — 20g", "Leave"
        ]
        choice = get_choice(f"Gold: {player.gold}", options)
        if choice == 8:
            return
        prices = [8, 10, 6, 25, 15, 18, 20]
        if player.gold < prices[choice - 1]:
            slow_type("  Not enough gold.")
            continue
        player.gold -= prices[choice - 1]
        if choice <= 4:
            player.inventory.append(["Health Potion", "Ether Vial", "Smoke Bomb", "Elixir of Fortitude"][choice - 1])
        elif choice == 5:
            player.defence += 3
        elif choice == 6:
            player.base_attack += 4
            player.attack += 4
        else:
            player.magic += 5
        slow_type("  Purchase complete.")


def travel_event(player):
    if random.random() > 0.65:
        return None
    divider()
    event = random.choice(("camp", "traveller", "ambush", "shrine", "merchant", "fog", "library", "companion", "crafting", "chest", "soldier", "crater"))
    if event == "camp":
        choice = get_choice("You find an abandoned camp. Search it?", ["Yes", "No"])
        if choice == 1:
            roll = random.random()
            if roll < 0.4:
                player.inventory.append("Health Potion")
                slow_type("  You find a Health Potion!")
            elif roll < 0.7:
                player.gain_gold(random.randint(4, 10))
            else:
                combat(player, Enemy("Void Sprite", 35, 10, 2, 15, 4))
    elif event == "traveller":
        options = ["Give a Health Potion", "Give 5 gold", "Walk past"]
        if "Health Potion" not in player.inventory:
            options[0] = "Offer help without a potion"
        choice = get_choice("A wounded traveller asks for help.", options)
        if choice == 1 and "Health Potion" in player.inventory:
            player.inventory.remove("Health Potion")
            player.inventory.append("Smoke Bomb")
            player.reputation += 1
        elif choice == 2 and player.gold >= 5:
            player.gold -= 5
            player.reputation += 1
        elif choice == 3:
            player.reputation -= 1
    elif event == "ambush":
        result = combat(player, Enemy("Void Wraith", 55, 13, 3, 25, 6))
        if result == "lose": return "lose"
    elif event == "shrine":
        choice = get_choice("A shrine offers a blessing.", ["10 gold", "20 gold", "Take the offering", "Leave"])
        if choice == 1 and player.gold >= 10:
            player.gold -= 10; _shrine_bless(player, True)
        elif choice == 2 and player.gold >= 20:
            player.gold -= 20; _shrine_bless(player, False)
        elif choice == 3:
            player.gain_gold(random.randint(5, 15)); player.reputation -= 2
    elif event == "merchant":
        merchant(player)
    elif event == "fog":
        effect = random.choice(("xp", "heal", "mp", "stat"))
        if effect == "xp": player.gain_xp(35)
        elif effect == "heal": slow_type(f"  +{player.heal(45)} HP")
        elif effect == "mp":
            gain = min(35, player.max_mp - player.mp); player.mp += gain; slow_type(f"  +{gain} MP")
        else: player.base_attack += 2; player.attack += 2; slow_type("  Attack +2")
    elif event == "library":
        choice = get_choice("A surviving tome catches your eye.", ["Study it", "Take it", "Leave it"])
        if choice == 1:
            player.magic += 5; player.gain_xp(20); player.reputation += 1
        elif choice == 2:
            player.inventory.append("Void Tome")
    elif event == "companion":
        available = [c for c in COMPANIONS_POOL if c.name not in {x.name for x in player.companions}]
        if available:
            template = random.choice(available)
            if get_choice(f"{template.name} offers to travel with you.", ["Accept", "Decline"]) == 1:
                player.companions.append(template.clone())
    elif event == "crafting":
        crafting_menu(player)
    elif event == "chest":
        if get_choice("An unlocked chest waits.", ["Open", "Leave"]) == 1:
            roll = random.random()
            if roll < 0.4: player.inventory.append(random.choice(("Health Potion", "Ether Vial", "Smoke Bomb", "Shadow Oil")))
            elif roll < 0.65: player.gain_gold(random.randint(10, 25))
            else:
                player.max_hp = max(20, player.max_hp - 10); player.hp = min(player.hp, player.max_hp)
    elif event == "soldier":
        if get_choice("An old soldier offers advice.", ["Listen", "Move on"]) == 1:
            player.defence += 2
    elif event == "crater":
        if get_choice("A warm piece of void rock lies in a crater.", ["Touch it", "Leave it"]) == 1:
            if random.random() < 0.6: player.magic += 6
            else: player.hp = max(1, player.hp - random.randint(10, 25))
    return None


def sidequest(player, name, reward_rep=1, reward_attack=0, reward_defence=0, reward_item=None):
    divider()
    slow_type(f"SIDE QUEST: {name}")
    choice = get_choice("How do you respond?", ["Help", "Walk away"])
    if choice == 2:
        return None
    player.quests_completed += 1
    player.reputation += reward_rep
    player.attack += reward_attack; player.base_attack += reward_attack
    player.defence += reward_defence
    if reward_item: player.inventory.append(reward_item)
    slow_type("  Quest complete!")
    if player.quests_completed >= 8:
        unlock_achievement(player, "all_quests")
    return None


def visit_shop(player, act_num):
    divider()
    choice = get_choice(f"Before Act {act_num}, prepare yourself.", ["Trader", "Crafting", "Status", "Continue"])
    if choice == 1: merchant(player)
    elif choice == 2: crafting_menu(player)
    elif choice == 3: player.status(); show_achievements(player)
    save_game(player, f"act_{act_num}")


def act_one(player):
    divider(); slow_type("ACT I — ASHFALL")
    sidequest(player, "The Lost Child", 2, 6, reward_item="Health Potion")
    slow_type("Elder Mara tells you the first Shard lies beneath the temple.")
    travel_event(player)
    result = combat(player, Enemy("Void Wraith Commander", 70, 14, 4, 40, 8, abilities=["summon"]))
    if result == "lose": return "lose"
    player.shards += 1; player.gain_gold(5)
    visit_shop(player, 2)
    return "act_two"


def act_two(player):
    divider(); slow_type("ACT II — DUSKMAR")
    travel_event(player)
    if get_choice("How do you enter Duskmar?", ["Tell the truth", "Pose as a merchant", "Use a side passage"]) == 1:
        if combat(player, Enemy("City Guard", 50, 12, 6, 20, 6)) == "lose": return "lose"
    sidequest(player, "The Forgotten Grave", 2, reward_item="Elixir of Fortitude")
    if combat(player, Enemy("Bone Golem", 75, 16, 8, 40, 8, abilities=["shield"])) == "lose": return "lose"
    sidequest(player, "The Twin Blades", 1, reward_attack=3)
    travel_event(player)
    if combat(player, Enemy("Iron Golem", 115, 18, 14, 65, 15, abilities=["shield"])) == "lose": return "lose"
    player.shards += 1; player.gain_gold(8)
    visit_shop(player, 3)
    return "act_three"


def act_three(player):
    divider(); slow_type("ACT III — THE SUNKEN RUINS")
    travel_event(player)
    if combat(player, Enemy("Void-Touched Bandit", 80, 17, 7, 45, 10, abilities=["poison"])) == "lose": return "lose"
    sidequest(player, "The Deserter", 1, reward_defence=2)
    sidequest(player, "The Lighthouse", 2, reward_item="Ether Vial")
    travel_event(player)
    choice = get_choice("Why do you seek the Shards?", ["To save Eldoria", "For power", "Because of prophecy", "For revenge"])
    if choice == 1: player.defence += 3
    elif choice == 2: player.attack += 4; player.base_attack += 4
    elif choice == 3: player.max_hp += 20; player.hp += 20
    else: player.magic += 8
    if combat(player, Enemy("Void Serpent", 100, 20, 6, 60, 12, abilities=["poison", "drain"])) == "lose": return "lose"
    player.shards += 1; player.gain_gold(10)
    visit_shop(player, 4)
    return "act_four"


def act_four(player):
    divider(); slow_type("ACT IV — THE ARCANE SPIRE")
    travel_event(player)
    sidequest(player, "The Oracle", 1, reward_attack=5)
    sidequest(player, "The Arena", 2, reward_attack=4)
    for enemy in [
        Enemy("Arena Champion", 100, 22, 12, 50, 20, abilities=["berserk"]),
        Enemy("Void Lord Vareth", 135, 22, 10, 90, 20, abilities=["berserk", "shield"]),
    ]:
        if combat(player, enemy) == "lose": return "lose"
    if get_choice("Search Vareth for answers?", ["Yes", "No"]) == 1:
        player.inventory.append("Malachar's Journal")
    player.shards += 1; player.gain_gold(12)
    visit_shop(player, 5)
    return "act_five"


def act_five(player):
    divider(); slow_type("ACT V — THE THRONE OF ASHES")
    travel_event(player)
    sidequest(player, "Malachar's Apprentice", 2, reward_item="Ether Vial")
    has_journal = "Malachar's Journal" in player.inventory
    hero = player.reputation >= 5 and player.quests_completed >= 3
    if hero:
        choice = get_choice("Malachar offers another path.", ["Fight", "Let him sacrifice himself", "Find a way together"])
        if choice == 1:
            result = combat(player, Enemy("Malachar, the Last Sorcerer", 200, 28, 12, 200, 0, abilities=["drain", "shield", "berserk"]))
            if result == "lose": return "lose"
            player.shards = 5; return "ending_victory_blood"
        if choice == 2:
            player.shards = 5; return "ending_redemption"
        player.shards = 5; unlock_achievement(player, "secret_ending"); return "ending_transcendence"
    if has_journal:
        choice = get_choice("You know the cost. What do you choose?", ["Fight", "Let Malachar sacrifice himself", "Work together"])
        if choice == 1:
            if combat(player, Enemy("Malachar, the Last Sorcerer", 200, 28, 12, 200, 0, abilities=["drain", "shield"])) == "lose": return "lose"
            player.shards = 5; return "ending_victory_blood"
        player.shards = 5
        return "ending_redemption" if choice == 2 else "ending_alliance"
    choice = get_choice("Malachar stands before you.", ["Fight", "Demand answers", "Talk"])
    if choice == 1:
        if combat(player, Enemy("Malachar, the Last Sorcerer", 200, 28, 12, 200, 0, abilities=["drain", "shield"])) == "lose": return "lose"
        player.shards = 5; return "ending_victory_blood"
    if get_choice("He tells you the Void is alive.", ["Fight", "Work with him"]) == 1:
        if combat(player, Enemy("Malachar, the Last Sorcerer", 200, 28, 12, 200, 0, abilities=["drain", "shield"])) == "lose": return "lose"
        player.shards = 5; return "ending_victory_blood"
    player.shards = 5
    return "ending_alliance"


def show_achievements(player):
    divider(); slow_type("ACHIEVEMENTS")
    for key, (name, description) in ACHIEVEMENTS.items():
        mark = "★" if key in player.achievements else "○"
        print(f"  {mark} {name}: {description}")


def ending_victory_blood(player):
    divider(); slow_type("ENDING I — THE WARRIOR'S CROWN")
    slow_type("You defeated Malachar. Eldoria will heal.")


def ending_redemption(player):
    divider(); slow_type("ENDING II — THE PRICE OF MERCY")
    slow_type("Malachar seals the Void and pays the final price.")


def ending_alliance(player):
    divider(); slow_type("ENDING III — THE UNLIKELY ALLIANCE")
    slow_type("You and Malachar seal the Void together.")


def ending_transcendence(player):
    divider(); slow_type("ENDING IV — THE SIXTH SHARD ★ SECRET ENDING ★")
    slow_type("A new Shard is born from the choices you made.")


def ending_dark(player):
    divider(); slow_type("ENDING V — THE VOID KING ★ DARK ENDING ★")
    slow_type("The Void recognises you, and Eldoria falls beneath your shadow.")


def ending_lose(player):
    divider(); slow_type("The darkness takes you.")
    slow_type("Your save remains available so you can try again.")


def pick_class():
    names = list(CLASSES)
    options = []
    for name in names:
        stats = CLASSES[name]
        options.append(f"{name} — HP {stats['hp']} / MP {stats['mp']} / ATK {stats['attack']} / DEF {stats['defence']} / MAG {stats['magic']}")
    choice = get_choice("Choose your class:", options)
    name = names[choice - 1]
    return name, dict(CLASSES[name])


def get_name():
    while True:
        name = input("\nWhat is your name, traveller? ").strip()
        if not name:
            slow_type("  Please enter a name.")
            continue
        name = name.capitalize()
        if get_choice(f"Use the name '{name}'?", ["Yes", "No"]) == 1:
            return name


def main():
    clear()
    slow_type("╔════════════════════════════════════════════════════╗")
    slow_type("║        E L D O R I A   C H R O N I C L E S        ║")
    slow_type("║              STABLE EDITION                       ║")
    slow_type("╚════════════════════════════════════════════════════╝")
    while True:
        mode = get_choice("\nMain Menu", ["New Game", "Load Game", "View Achievements", "Quit"])
        if mode == 4:
            slow_type("Until next time, traveller.")
            return
        if mode == 3:
            player, _ = load_game()
            if player: show_achievements(player)
            else: slow_type("  No valid save found.")
            continue
        if mode == 2:
            player, act = load_game()
            if not player:
                slow_type("  No valid save found. Starting a new game.")
                mode = 1
        if mode == 1:
            divider(); slow_type("PROLOGUE")
            for line in LORE_INTRO:
                slow_type(line); pause(0.25)
            name = get_name()
            cls_name, stats = pick_class()
            player = Player(name, cls_name, stats)
            act = "act_one"
        act_map = {"act_one": act_one, "act_two": act_two, "act_three": act_three, "act_four": act_four, "act_five": act_five}
        order = list(act_map)
        try:
            start = order.index(act)
        except ValueError:
            start = 0
        state = None
        for act_name in order[start:]:
            state = act_map[act_name](player)
            if state == "lose" or not player.is_alive():
                state = "lose"
                break
        if state != "lose" and player.reputation <= -5:
            state = "ending_dark"
        endings = {
            "ending_victory_blood": ending_victory_blood,
            "ending_redemption": ending_redemption,
            "ending_alliance": ending_alliance,
            "ending_transcendence": ending_transcendence,
            "ending_dark": ending_dark,
            "lose": ending_lose,
        }
        endings.get(state, ending_lose)(player)
        if player.reputation >= 8: unlock_achievement(player, "high_rep")
        if player.quests_completed >= 8: unlock_achievement(player, "all_quests")
        save_game(player, state or "completed")
        if get_choice("Play again?", ["Yes", "No"]) == 2:
            return


if __name__ == "__main__":
    main()
