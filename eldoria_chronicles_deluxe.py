"""Eldoria Chronicles — Deluxe Campaign.

Runs the original five-act game while adding a much longer optional campaign,
extra choices, lore, rewards, save checkpoints, and a fully described caravan
shop. The original source remains intact.
"""

import random
import eldoria_chronicles as game


DELUXE_GOODS = [
    ("Health Potion", 8, "A bitter crimson tonic brewed from moonroot. Restores up to 50 HP."),
    ("Ether Vial", 10, "Shimmering blue essence in a glass vial. Restores up to 40 MP."),
    ("Elixir of Fortitude", 25, "A rare golden draught that completely restores HP and MP."),
    ("Iron Charm", 15, "An old Ironpeak charm that permanently increases Defence by 3."),
    ("Arcane Crystal", 20, "A humming shard of crystallised mana that permanently increases Magic by 5."),
    ("Traveller's Rations", 5, "Dried fruit, bread and spiced roots. Restores up to 20 HP."),
    ("Moonleaf Tea", 7, "Fragrant silver-green tea. Restores up to 20 MP."),
    ("Explorer's Map", 12, "A hand-drawn map of forgotten roads. Studying it grants 30 XP."),
    ("Lucky Coin", 16, "An ancient coin said to attract fortunate discoveries."),
    ("Void Tome", 20, "A sealed scholarly book containing unsettling lore about the Void."),
    ("Starlight Lantern", 22, "A crystal lantern that reveals hidden writing. Grants +2 Magic permanently."),
    ("Guardian's Token", 24, "A polished warden token. Grants +2 Defence and restores 15 HP immediately."),
    ("Merchant's Mystery Box", 14, "A sealed box containing one randomly selected useful item or a surprise purse of gold."),
]


def deluxe_shop(player):
    game.divider()
    game.slow_type("THE GRAND CARAVAN OF ELDORIA")
    game.slow_type("The merchant's old wagon has grown into a sprawling travelling market.")
    game.slow_type("Lanterns hang from ropes, shelves overflow with curios, and every item has a story.")

    while True:
        options = [f"{name} — {price}g" for name, price, _ in DELUXE_GOODS]
        options += ["Ask about an item", "Sell selected supplies", "Leave the caravan"]
        choice = game.get_choice(f"Gold available: {player.gold}\nWhat will you browse?", options)

        if choice == len(options):
            game.slow_type("  The merchant smiles. 'May the roads be kinder to you than they were to me.'")
            return

        if choice == len(options) - 1:
            sellable = [i for i in player.inventory if i in {
                "Health Potion", "Ether Vial", "Mega Potion", "Arcane Brew",
                "Void Flask", "Shadow Oil", "Void Tome"
            }]
            if not sellable:
                game.slow_type("  You have nothing in your pack that the merchant wants today.")
                continue
            sell_options = [f"{item} — {max(2, len(item))}g" for item in sellable] + ["Cancel"]
            sell_choice = game.get_choice("Choose something to sell:", sell_options)
            if sell_choice == len(sell_options):
                continue
            item = sellable[sell_choice - 1]
            value = max(2, len(item))
            player.inventory.remove(item)
            player.gold += value
            game.slow_type(f"  Sold {item} for {value}g. Gold: {player.gold}")
            continue

        if choice == len(options) - 2:
            ask = game.get_choice("Ask about what?", [
                "Healing supplies", "Permanent upgrades", "Maps and exploration", "Magical curios", "Never mind"
            ])
            advice = {
                1: "Healing supplies are cheap now, but they become priceless when the road gets rough.",
                2: "Permanent upgrades cost more, but they stay with you for the whole journey.",
                3: "Maps are often more valuable than gold. Eldoria has roads that disappear from ordinary maps.",
                4: "Curios are unpredictable. Read the description before spending your coins.",
                5: "The merchant nods and returns to polishing a crystal.",
            }[ask]
            game.slow_type(f"  Merchant: '{advice}'")
            continue

        name, price, description = DELUXE_GOODS[choice - 1]
        game.divider()
        game.slow_type(name.upper())
        game.slow_type(f"  Price: {price} gold")
        game.slow_type(f"  Description: {description}")
        if game.get_choice("Purchase this item?", ["Yes", "No"]) == 2:
            continue
        if player.gold < price:
            game.slow_type("  You do not have enough gold.")
            continue

        player.gold -= price
        if name == "Iron Charm":
            player.defence += 3
            game.slow_type("  Defence permanently increased by 3.")
        elif name == "Arcane Crystal":
            player.magic += 5
            game.slow_type("  Magic permanently increased by 5.")
        elif name == "Starlight Lantern":
            player.magic += 2
            player.inventory.append(name)
            game.slow_type("  The lantern glows. Magic permanently increased by 2.")
        elif name == "Guardian's Token":
            player.defence += 2
            healed = player.heal(15)
            player.inventory.append(name)
            game.slow_type(f"  Defence +2 and {healed} HP restored.")
        elif name == "Traveller's Rations":
            healed = player.heal(20)
            game.slow_type(f"  You eat beside the wagon. {healed} HP restored.")
        elif name == "Moonleaf Tea":
            gain = min(20, player.max_mp - player.mp)
            player.mp += gain
            game.slow_type(f"  Your thoughts clear. {gain} MP restored.")
        elif name == "Explorer's Map":
            player.inventory.append(name)
            player.gain_xp(30)
            game.slow_type("  You memorise the safest routes. +30 XP.")
        elif name == "Merchant's Mystery Box":
            result = random.choice(["Health Potion", "Ether Vial", "Moonleaf Tea", "Lucky Coin", "Guardian's Token", "20 gold"])
            if result == "20 gold":
                player.gold += 20
                game.slow_type("  A hidden purse falls out. +20 gold!")
            else:
                player.inventory.append(result)
                game.slow_type(f"  The box contains: {result}!")
        else:
            player.inventory.append(name)
            game.slow_type(f"  Added {name} to your inventory.")

        if len(player.inventory) >= 6:
            game.unlock_achievement(player, "hoarder")


CHAPTERS = {
    "act_one": ("THE LONG ROAD — GREENHOLLOW", "The countryside is full of stories the main road never tells.", [
        ("The Bell Beneath the Roots", "A bell buried beneath an ancient tree rings whenever the Void draws near."),
        ("Letters Never Sent", "A ruined post office contains hundreds of letters written before the Shard Wars."),
        ("The Orchard Keeper", "An old gardener refuses to abandon an orchard growing impossible silver fruit."),
    ]),
    "act_two": ("THE LONG ROAD — IRONPEAK", "The mountain remembers every traveller who ever climbed it.", [
        ("The Empty Foundry", "A silent foundry still produces glowing tools despite having no workers."),
        ("Echoes in the Lift", "An abandoned mine lift descends farther than any surviving map records."),
        ("The Last Apprentice", "A young craftsperson needs help deciding whether to rebuild or leave Ironpeak."),
    ]),
    "act_three": ("THE LONG ROAD — ARCANE SPIRE", "The Spire's scholars know more than they are willing to say.", [
        ("The Library That Moved", "Every time you enter the library, the shelves have rearranged themselves."),
        ("Seven Questions", "A magical door asks questions whose answers change the path behind it."),
        ("The Sleeping Constellation", "A constellation has vanished from the sky and something is trying to replace it."),
    ]),
    "act_four": ("THE LONG ROAD — DUSKMAR", "The city prepares for a festival while the sky quietly darkens.", [
        ("Lanterns for the Lost", "Duskmar's streets are full of abandoned lanterns that still remember their owners."),
        ("The Silent Theatre", "A theatre performs every night even though no audience remembers buying tickets."),
        ("A Name in Ash", "A single name appears on walls throughout the city, always one street ahead of you."),
    ]),
    "act_five": ("THE LONG ROAD — THE VOID FRONTIER", "The final road is not on any map. You walk it anyway.", [
        ("The Door With No Wall", "A doorway stands alone in a field and opens onto somewhere that should not exist."),
        ("The Hourglass Lake", "The lake reflects yesterday instead of today."),
        ("The Fifth Road", "Four roads are marked on the map. A fifth appears only when you stop looking for it."),
    ]),
}


def long_road_chapter(player, region, number, title, premise):
    game.divider()
    game.slow_type(f"CHAPTER {number}: {title}")
    game.slow_type(f"  {premise}")

    if number == 1:
        choice = game.get_choice("How do you approach the mystery?", [
            "Investigate carefully", "Ask the locals what they know", "Follow the strange signal immediately"
        ])
        if choice == 1:
            player.gain_xp(20)
            game.slow_type("  Careful observation reveals a safer route. +20 XP.")
        elif choice == 2:
            player.reputation += 1
            game.slow_type("  The locals appreciate your patience. Reputation +1.")
        else:
            enemy = game.Enemy(
                "Forgotten Guardian", hp=65 + player.level * 5, attack=12 + player.level,
                defence=5, xp_reward=40, gold_drop=12,
                lore="A construct left behind when the old kingdoms still feared the Void.",
                abilities=["shield"]
            )
            if game.combat(player, enemy) == "lose":
                return "lose"

    elif number == 2:
        choice = game.get_choice("A difficult choice appears.", [
            "Preserve the old secret", "Reveal it to everyone", "Use the discovery for your own advantage"
        ])
        if choice == 1:
            player.reputation += 2
            player.gain_xp(35)
        elif choice == 2:
            player.reputation += 1
            player.gain_xp(45)
        else:
            player.reputation -= 2
            player.gold += 18
            game.slow_type("  You profit from the discovery. +18 gold, Reputation -2.")

    else:
        choice = game.get_choice("The final mystery waits.", [
            "Help the people involved", "Take the treasure and leave", "Stay and uncover the entire story"
        ])
        if choice == 1:
            player.reputation += 2
            item = random.choice(["Health Potion", "Ether Vial", "Moonleaf Tea"])
            player.inventory.append(item)
            game.slow_type(f"  Your help is remembered. Reputation +2. You receive {item}.")
        elif choice == 2:
            player.reputation -= 1
            player.gold += 25
        else:
            player.gain_xp(70)
            game.slow_type("  You stay until dawn and piece together the complete history. +70 XP.")

    rewards = {
        "act_one": (35, 1, 0, 0),
        "act_two": (45, 0, 2, 0),
        "act_three": (55, 0, 0, 3),
        "act_four": (65, 0, 0, 0),
        "act_five": (80, 0, 0, 0),
    }
    xp, rep, defence, magic = rewards[region]
    player.gain_xp(xp + number * 10)
    player.reputation += rep
    player.defence += defence
    player.magic += magic
    if region == "act_five":
        player.max_mp += 5
        player.mp = player.max_mp

    player.quests_completed += 1
    game.slow_type(f"  [Long-road chapter complete. Total quests: {player.quests_completed}]")
    if player.quests_completed >= 4:
        game.unlock_achievement(player, "all_quests")
    return None


def extended_act(player, region):
    title, intro, quests = CHAPTERS[region]
    game.divider()
    game.slow_type(title)
    game.slow_type(intro)
    game.slow_type("  Three substantial side chapters unfold here before the main story continues.")

    for number, (quest_title, premise) in enumerate(quests, 1):
        if long_road_chapter(player, region, number, quest_title, premise) == "lose":
            return "lose"

    game.slow_type("  You leave the region with more answers, more history, and several new questions.")
    game.save_game(player, f"{region}_long_road")
    return None


# Replace only the shop and act hooks. The original game remains the source of
# the combat engine, classes, crafting, companions, endings and save format.
game._visit_merchant = deluxe_shop

for _name in ("act_one", "act_two", "act_three", "act_four", "act_five"):
    _original = getattr(game, _name)

    def make_wrapper(original, region):
        def wrapped(player):
            state = original(player)
            if state == "lose" or not player.is_alive():
                return state
            extra = extended_act(player, region)
            return "lose" if extra == "lose" else state
        return wrapped

    setattr(game, _name, make_wrapper(_original, _name))


if __name__ == "__main__":
    game.main()
