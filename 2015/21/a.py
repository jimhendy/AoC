import re
import pandas as pd


def fight(equipment, my_hp, boss_hp, boss_damage, boss_armor):
    my_damage = sum([e["Damage"] for e in equipment])
    my_armor = sum([e["Armor"] for e in equipment])
    my_cost = sum([e["Cost"] for e in equipment])

    my_attack = max([my_damage - boss_armor, 1])
    boss_attack = max([boss_damage - my_armor, 1])

    while True:
        # My turn
        boss_hp -= my_attack
        if boss_hp <= 0:
            # Win
            return my_cost

        # Boss turn
        my_hp -= boss_attack
        if my_hp <= 0:
            return False

        pass
    pass


def run(inputs):

    all_equipment = []
    equip_type = None
    with open("2015/21/store.txt", "r") as f:
        for l in f.readlines():
            type_match = re.match("^[^\s]+: ", l)
            if type_match:
                equip_type = type_match[0].rstrip(" :")
            else:
                l_split = re.findall("^(.+)\s+(\d+)\s+(\d)\s+(\d)$", l)
                if not len(l_split):
                    continue
                l_split = l_split[0]
                all_equipment.append(
                    {
                        "Type": equip_type,
                        "Name": l_split[0].strip(),
                        "Cost": int(l_split[1]),
                        "Damage": int(l_split[2]),
                        "Armor": int(l_split[3]),
                    }
                )
    df_equip = pd.DataFrame(all_equipment)

    def extract(type_name):
        type_dict = df_equip[df_equip.Type.eq(type_name)].set_index("Name").T.to_dict()
        if type_name != "Weapons":
            type_dict[f"Empty_{type_name}"] = {"Cost": 0, "Damage": 0, "Armor": 0}
        return type_dict

    weapons = extract("Weapons")
    armor = extract("Armor")
    rings = extract("Rings")

    fights = []
    for wn, w in weapons.items():
        for an, a in armor.items():
            for rn1, r1 in rings.items():
                for rn2, r2 in rings.items():
                    if rn1 == rn2:
                        continue
                    result = fight((w, a, r1, r2), 100, 103, 9, 2)
                    if result:
                        fights.append((result, (wn, an, rn1, rn2)))

    return sorted(fights, key=lambda x: x[0])[0][0]
