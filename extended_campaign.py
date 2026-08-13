"""Launch the expanded Eldoria narrative layer."""

from eldoria_chronicles import CLASSES, Enemy, Player, combat, get_choice, slow_type
from eldoria_story import ACTS, PROLOGUE, ending_lines


def divider():
    print("\n" + "=" * 68 + "\n")


def tell(title, text):
    divider()
    slow_type(title)
    slow_type(text)


def new_campaign():
    for title, text in PROLOGUE:
        tell(title, text)
    name = input("\nName: ").strip().capitalize() or "Wanderer"
    classes = list(CLASSES)
    choice = get_choice("Choose your class:", classes)
    player = Player(name, classes[choice - 1], CLASSES[classes[choice - 1]])
    for act_number in range(1, 6):
        act = ACTS[act_number]
        tell(f"ACT {act_number}: {act['title']}", act["subtitle"])
        for scene_title, scene_text in act["scenes"]:
            tell(scene_title, scene_text)
        if act_number < 5:
            choice = get_choice("The road ahead:", act["choice_prompts"] + ["Continue"])
            player.reputation += choice - 2
            player.gain_xp(25 + act_number * 10)
            if act_number in (2, 3):
                enemy = Enemy("Crown Hunter", 70 + act_number * 20, 15 + act_number * 2, 5 + act_number, 40, 10)
                if combat(player, enemy) == "lose":
                    tell("THE END", "Your journey ends here. The save from the main campaign remains untouched.")
                    return
    choice = get_choice("The final choice:", ["Claim the Crown", "Choose Mercy", "Forge an Alliance", "Destroy the Shards", "Remember the Sixth"])
    endings = ["crown", "mercy", "alliance", "destroy", "secret"]
    ending = endings[choice - 1]
    tell("EPILOGUE", "\n".join(ending_lines(ending)))


if __name__ == "__main__":
    new_campaign()
