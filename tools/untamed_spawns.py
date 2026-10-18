# Gera os spawns dos Pokémon que entram no lugar dos bichos do Alex's Mobs (data/ecosystems_untamed/spawn_pool_world/
# am_<bicho>.json) e o docs/pokemon-do-alexs-mobs.md (para revisar e editar).
#
# - Os biomas vêm dos arquivos de spawn do próprio Alex's Mobs (config/alexsmobs/<bicho>_spawns.json, que ele cria no
#   primeiro jogo): cada grupo de condições vira um bioma (ou tag) do Cobblemon, e as negações viram "anticondition".
#   Só entram biomas do Minecraft e tags comuns (c:); os de outros mods (Terralith...) ficam de fora.
# - Os drops ficam no próprio spawn: só os Pokémon que nascem no lugar do bicho dão os itens dele (o mesmo Pokémon
#   nascido em outro lugar continua com os drops normais do Cobblemon). Assim os itens do Alex's Mobs que só saíam dos
#   bichos (pelo de urso, escamas de crocodilo, penas...) continuam no jogo.
# - Bichos sem um Pokémon que combine (chefes, monstros e criaturas muito próprias do mod) ficam sem spawn: estão na
#   lista do .md como "sem substituto".
#
# Uso: python untamed_spawns.py <pasta config/alexsmobs> <pasta resources do mod> <pasta docs>
import json
import sys
from pathlib import Path

AM = "alexsmobs:"


def d(item, chance, qty="1"):
    """Um drop: item, chance em % e quantidade ("1" ou "1-2")."""
    return {"item": item if ":" in item else AM + item, "percentage": chance, "qty": qty}


def p(species, bucket, levels, weight):
    return (species, bucket, levels, weight)


# bicho: (nome, onde nasce, [Pokémon], drops, observação)
# onde: grounded, submerged, cave (no chão, sem ver o céu), surface (na superfície da água)
MOBS = {
    # --- Florestas, planícies e taigas ---
    "grizzly_bear": ("Grizzly Bear", "grounded", [p("teddiursa", "common", "8-25", 6), p("ursaring", "uncommon", "30-45", 1)],
                     [d("bear_fur", 50)], ""),
    "blue_jay": ("Blue Jay", "grounded", [p("taillow", "common", "5-20", 6), p("swellow", "rare", "22-40", 1)],
                 [d("minecraft:feather", 50)], ""),
    "crow": ("Crow", "grounded", [p("rookidee", "common", "5-20", 6), p("corvisquire", "uncommon", "18-35", 2),
                                  p("corviknight", "rare", "38-50", 0.5)], [d("minecraft:feather", 50)], ""),
    "raccoon": ("Raccoon", "grounded", [p("zigzagoon", "common", "5-20", 6), p("linoone", "uncommon", "20-35", 2)],
                [d("raccoon_tail", 25)], ""),
    "skunk": ("Skunk", "grounded", [p("stunky", "common", "8-25", 5), p("skuntank", "rare", "34-45", 1)],
              [d("skunk_spray", 20)], ""),
    "tasmanian_devil": ("Tasmanian Devil", "grounded", [p("poochyena", "common", "8-20", 5), p("mightyena", "rare", "18-35", 1)],
                        [], ""),
    "sugar_glider": ("Sugar Glider", "grounded", [p("emolga", "uncommon", "10-30", 4), p("pachirisu", "uncommon", "10-30", 3)],
                     [], ""),
    "bison": ("Bison", "grounded", [p("bouffalant", "uncommon", "20-40", 4)],
              [d("minecraft:beef", 60, "1-2"), d("bison_fur", 50)], ""),
    "potoo": ("Potoo", "grounded", [p("hoothoot", "common", "8-20", 5), p("noctowl", "rare", "20-40", 1)],
              [d("minecraft:feather", 50)], "Floresta escura"),
    "bald_eagle": ("Bald Eagle", "grounded", [p("rufflet", "uncommon", "15-30", 4), p("braviary", "rare", "54-60", 0.5)],
                   [d("minecraft:feather", 60, "1-2")], ""),
    "banana_slug": ("Banana Slug", "grounded", [p("shellos", "common", "10-25", 5), p("gastrodon", "rare", "30-45", 1)],
                    [d("banana_slug_slime", 50)], "Taigas antigas"),
    "moose": ("Moose", "grounded", [p("stantler", "uncommon", "15-35", 4), p("wyrdeer", "rare", "35-50", 0.5)],
              [d("moose_ribs", 50), d("moose_antler", 10)], ""),
    "hummingbird": ("Hummingbird", "grounded", [p("cutiefly", "common", "5-20", 5), p("ribombee", "rare", "25-40", 1)], [], ""),
    # --- Pântanos, rios e mangues ---
    "crocodile": ("Crocodile", "grounded", [p("croconaw", "uncommon", "18-30", 3), p("feraligatr", "rare", "30-50", 1)],
                  [d("crocodile_scute", 40), d("crocodile_egg", 5)], ""),
    "caiman": ("Caiman", "grounded", [p("totodile", "common", "5-18", 5)], [d("caiman_egg", 5)], "Mangue"),
    "alligator_snapping_turtle": ("Alligator Snapping Turtle", "grounded",
                                  [p("chewtle", "common", "8-22", 5), p("drednaw", "rare", "22-45", 1)],
                                  [d("spiked_scute", 20)], ""),
    "anaconda": ("Anaconda", "grounded", [p("ekans", "common", "8-20", 4), p("arbok", "rare", "22-40", 1)],
                 [d("shed_snake_skin", 30)], ""),
    "catfish": ("Catfish", "submerged", [p("barboach", "common", "8-25", 6), p("whiscash", "rare", "30-45", 1)],
                [d("raw_catfish", 60)], ""),
    "shoebill": ("Shoebill", "grounded", [p("cramorant", "uncommon", "20-40", 3)], [d("minecraft:feather", 50)], ""),
    "platypus": ("Platypus", "submerged", [p("psyduck", "common", "8-25", 5), p("golduck", "rare", "33-45", 1)], [], ""),
    "terrapin": ("Terrapin", "submerged", [p("squirtle", "uncommon", "5-16", 3), p("wartortle", "rare", "16-36", 1)], [], ""),
    "mudskipper": ("Mudskipper", "grounded", [p("mudkip", "uncommon", "5-16", 3), p("marshtomp", "rare", "16-36", 1)],
                   [d("minecraft:tropical_fish", 30)], "Mangue"),
    # --- Selva ---
    "capuchin_monkey": ("Capuchin Monkey", "grounded", [p("aipom", "common", "8-25", 5), p("ambipom", "rare", "25-40", 1)],
                        [d("banana", 20)], ""),
    "gorilla": ("Gorilla", "grounded", [p("slakoth", "common", "8-18", 4), p("vigoroth", "uncommon", "18-36", 2),
                                        p("slaking", "rare", "36-50", 0.5)], [d("banana", 30, "1-2")], ""),
    "toucan": ("Toucan", "grounded", [p("pikipek", "common", "5-14", 5), p("trumbeak", "uncommon", "14-28", 2),
                                      p("toucannon", "rare", "28-45", 0.5)], [d("minecraft:feather", 50)], ""),
    "anteater": ("Anteater", "grounded", [p("heatmor", "uncommon", "20-40", 3)], [], "Caça os Durant dos formigueiros"),
    "komodo_dragon": ("Komodo Dragon", "grounded", [p("salandit", "common", "10-33", 4), p("salazzle", "rare", "33-45", 1)],
                      [d("komodo_spit", 20)], ""),
    "tiger": ("Tiger", "grounded", [p("litten", "uncommon", "5-17", 3), p("torracat", "rare", "17-34", 1)], [], "Selva de bambu"),
    # --- Savana, deserto e badlands ---
    "elephant": ("Elephant", "grounded", [p("phanpy", "common", "8-25", 5), p("donphan", "rare", "25-45", 1)],
                 [d("acacia_blossom", 15)], ""),
    "rhinoceros": ("Rhinoceros", "grounded", [p("rhyhorn", "common", "15-42", 4), p("rhydon", "rare", "42-55", 0.5)], [], ""),
    "gazelle": ("Gazelle", "grounded", [p("deerling", "common", "8-34", 5), p("sawsbuck", "rare", "34-50", 1)],
                [d("minecraft:mutton", 50), d("gazelle_horn", 25)], ""),
    "maned_wolf": ("Maned Wolf", "grounded", [p("rockruff", "uncommon", "10-25", 3), p("lycanroc", "rare", "25-45", 0.5)], [], ""),
    "kangaroo": ("Kangaroo", "grounded", [p("kangaskhan", "uncommon", "20-40", 3)],
                 [d("kangaroo_meat", 50), d("kangaroo_hide", 40)], ""),
    "emu": ("Emu", "grounded", [p("doduo", "common", "10-31", 5), p("dodrio", "rare", "31-45", 1)],
            [d("emu_feather", 40), d("minecraft:feather", 40), d("emu_egg", 5)], ""),
    "roadrunner": ("Roadrunner", "grounded", [p("fletchling", "common", "5-17", 5), p("fletchinder", "uncommon", "17-35", 1)],
                   [d("roadrunner_feather", 40)], ""),
    "rattlesnake": ("Rattlesnake", "grounded", [p("seviper", "uncommon", "15-40", 4)], [d("rattlesnake_rattle", 30)], ""),
    "jerboa": ("Jerboa", "grounded", [p("sandshrew", "common", "8-22", 5), p("sandslash", "rare", "22-40", 1)], [], ""),
    "rain_frog": ("Rain Frog", "grounded", [p("croagunk", "uncommon", "10-37", 3)], [], ""),
    "tarantula_hawk": ("Tarantula Hawk", "grounded", [p("beedrill", "uncommon", "15-40", 3)],
                       [d("tarantula_hawk_wing_fragment", 30)], ""),
    "triops": ("Triops", "submerged", [p("kabuto", "uncommon", "10-30", 3)], [], "Poças do deserto"),
    "gelada_monkey": ("Gelada Monkey", "grounded", [p("mankey", "common", "8-28", 5), p("primeape", "rare", "28-45", 1)], [], ""),
    # --- Neve e montanhas ---
    "snow_leopard": ("Snow Leopard", "grounded", [p("absol", "uncommon", "20-45", 2)], [], ""),
    "tusklin": ("Tusklin", "grounded", [p("swinub", "common", "8-33", 5), p("piloswine", "uncommon", "33-45", 1),
                                        p("mamoswine", "rare", "45-60", 0.3)],
                [d("minecraft:porkchop", 50), d("minecraft:snowball", 40)], ""),
    "froststalker": ("Froststalker", "grounded", [p("sneasel", "uncommon", "15-40", 3)], [d("froststalker_horn", 20)], ""),
    "sunbird": ("Sunbird", "grounded", [p("fletchinder", "uncommon", "17-35", 2), p("talonflame", "rare", "35-50", 0.5)], [], ""),
    # --- Praia e oceano ---
    "seagull": ("Seagull", "grounded", [p("wingull", "common", "5-25", 6), p("pelipper", "rare", "25-45", 1)],
                [d("minecraft:feather", 50)], ""),
    "lobster": ("Lobster", "grounded", [p("corphish", "common", "8-30", 5), p("crawdaunt", "rare", "30-45", 1)],
                [d("lobster_tail", 50)], ""),
    "seal": ("Seal", "grounded", [p("seel", "common", "10-34", 4), p("spheal", "common", "10-32", 3), p("dewgong", "rare", "34-50", 1)],
             [], ""),
    "cachalot_whale": ("Cachalot Whale", "submerged", [p("wailmer", "uncommon", "15-40", 3), p("wailord", "rare", "40-55", 1)],
                       [d("ambergris", 10), d("cachalot_whale_tooth", 10)], ""),
    "orca": ("Orca", "submerged", [p("finizen", "uncommon", "15-38", 3), p("palafin", "rare", "38-50", 0.5)], [], ""),
    "hammerhead_shark": ("Hammerhead Shark", "submerged", [p("carvanha", "common", "10-30", 4), p("sharpedo", "rare", "30-45", 1)],
                         [d("shark_tooth", 30)], ""),
    "frilled_shark": ("Frilled Shark", "submerged", [p("relicanth", "rare", "20-45", 1)], [d("serrated_shark_tooth", 10)], ""),
    "giant_squid": ("Giant Squid", "submerged", [p("inkay", "uncommon", "10-30", 3), p("malamar", "rare", "30-50", 1)],
                    [d("minecraft:ink_sac", 60, "1-3"), d("lost_tentacle", 5)], ""),
    "blobfish": ("Blobfish", "submerged", [p("alomomola", "uncommon", "20-45", 3)], [d("blobfish", 40)], ""),
    "comb_jelly": ("Comb Jelly", "submerged", [p("frillish", "common", "10-40", 4), p("jellicent", "rare", "40-55", 0.5)],
                   [d("rainbow_jelly", 40)], ""),
    "flying_fish": ("Flying Fish", "submerged", [p("mantyke", "common", "10-30", 4), p("mantine", "rare", "30-45", 0.5)],
                    [d("flying_fish", 40)], ""),
    "mimic_octopus": ("Mimic Octopus", "submerged", [p("remoraid", "common", "10-25", 4), p("octillery", "rare", "25-45", 1)],
                      [d("minecraft:ink_sac", 50)], ""),
    "mantis_shrimp": ("Mantis Shrimp", "submerged", [p("krabby", "common", "10-28", 4), p("kingler", "rare", "28-45", 1)], [], ""),
    # --- Cavernas ---
    "cave_centipede": ("Cave Centipede", "cave", [p("venipede", "common", "10-22", 5), p("whirlipede", "uncommon", "22-30", 2),
                                                  p("scolipede", "rare", "30-45", 0.5)], [d("centipede_leg", 30)], ""),
    "cockroach": ("Cockroach", "cave", [p("nincada", "common", "8-20", 5), p("ninjask", "rare", "20-40", 1)],
                  [d("cockroach_wing_fragment", 40), d("cockroach_ootheca", 5)], ""),
    "rocky_roller": ("Rocky Roller", "cave", [p("geodude", "common", "10-25", 5), p("graveler", "uncommon", "25-40", 2),
                                              p("golem", "rare", "40-55", 0.3)],
                     [d("rocky_shell", 15), d("minecraft:tuff", 40), d("minecraft:pointed_dripstone", 40)], "Cavernas de espeleotema"),
    "flutter": ("Flutter", "cave", [p("morelull", "common", "10-24", 5), p("shiinotic", "rare", "24-40", 1)],
                [d("minecraft:spore_blossom", 15)], "Cavernas exuberantes"),
    # --- Cogumelos ---
    "bunfungus": ("Bunfungus", "grounded", [p("foongus", "common", "10-39", 4), p("amoonguss", "rare", "39-50", 1)],
                  [d("minecraft:red_mushroom", 50, "1-2")], ""),
    "mungus": ("Mungus", "grounded", [p("paras", "common", "8-24", 5), p("parasect", "rare", "24-45", 1)],
               [d("mungal_spores", 20)], ""),
    # --- Nether ---
    "dropbear": ("Dropbear", "grounded", [p("komala", "uncommon", "20-45", 2)], [d("dropbear_claw", 30)], ""),
    "soul_vulture": ("Soul Vulture", "grounded", [p("murkrow", "common", "15-35", 4), p("honchkrow", "rare", "35-50", 1)],
                     [d("minecraft:bone", 40), d("soul_heart", 5)], ""),
    "stradpole": ("Stradpole", "grounded", [p("slugma", "common", "15-38", 4)], [], ""),
    "straddler": ("Straddler", "grounded", [p("magcargo", "uncommon", "38-50", 2)], [d("straddlite", 30), d("minecraft:basalt", 40)], ""),
    "warped_toad": ("Warped Toad", "grounded", [p("tympole", "common", "10-25", 4), p("palpitoad", "uncommon", "25-36", 2),
                                                p("seismitoad", "rare", "36-50", 0.5)],
                    [d("minecraft:shroomlight", 20), d("minecraft:nether_wart", 30)], ""),
    # --- End ---
    "endergrade": ("Endergrade", "grounded", [p("elgyem", "common", "20-42", 4), p("beheeyem", "rare", "42-55", 1)], [], ""),
    "enderiophage": ("Enderiophage", "grounded", [p("solosis", "common", "20-32", 4), p("duosion", "uncommon", "32-41", 2),
                                                  p("reuniclus", "rare", "41-55", 0.5)], [d("capsid", 20)], ""),
    "mimicube": ("Mimicube", "grounded", [p("ditto", "uncommon", "20-50", 3)], [d("mimicream", 30)], ""),
    "spectre": ("Spectre", "grounded", [p("drifloon", "common", "20-28", 4), p("drifblim", "rare", "28-50", 1)],
               [], ""),
}

# Sem um Pokémon que combine (por enquanto): chefes, monstros e criaturas muito próprias do Alex's Mobs.
NO_POKEMON = {
    "bone_serpent": "Bone Serpent", "laviathan": "Laviathan", "crimson_mosquito": "Crimson Mosquito",
    "warped_mosco": "Warped Mosco", "guster": "Guster", "murmur": "Murmur", "skelewag": "Skelewag",
    "skreecher": "Skreecher", "underminer": "Underminer", "void_worm": "Void Worm", "farseer": "Farseer",
    "cosmaw": "Cosmaw", "cosmic_cod": "Cosmic Cod", "fly": "Fly", "devils_hole_pupfish": "Devil's Hole Pupfish",
    "cachalot_whale_beached": "Cachalot Whale (encalhada)",
}
SPECIAL = {"leafcutter_anthill": "Formigueiro: vira colônia de Durant (AnthillColonies)"}
WHERE = {"grounded": "chão", "submerged": "água", "cave": "caverna", "surface": "superfície"}


def biomes_of(config_dir, mob):
    """Os biomas do Alex's Mobs para o bicho: (biomas, biomas que não valem). Ignora os de outros mods."""
    path = config_dir / f"{mob}_spawns.json"
    if not path.exists():
        path = config_dir / f"{mob}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    yes, no = [], []
    for group in data.get("biomes", []):
        if not all(c["value"].split(":")[0] in ("minecraft", "c") for c in group):
            continue
        positive = [c for c in group if not c["negate"] and c["value"] != "minecraft:is_overworld"]
        for c in group:
            if c["negate"] and c["value"] != "c:no_default_monsters":
                name = ("#" if c["type"] == "BIOME_TAG" else "") + c["value"]
                if name not in no:
                    no.append(name)
        # Cobblemon não junta tags com "e": fica a última (a mais específica, ex. "colinas e coníferas" -> coníferas).
        pick = positive[-1] if positive else {"type": "BIOME_TAG", "value": "minecraft:is_overworld"}
        name = ("#" if pick["type"] == "BIOME_TAG" else "") + pick["value"]
        if name not in yes:
            yes.append(name)
    return yes, no


def drop_table(drops):
    entries = []
    for x in drops:
        e = {"item": x["item"], "percentage": float(x["percentage"])}
        if x["qty"] != "1":
            e["quantityRange"] = x["qty"]
        entries.append(e)
    return {"amount": len(entries), "entries": entries}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main():
    config_dir, resources, docs = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pool = resources / "data/ecosystems_untamed/spawn_pool_world"
    for old in pool.glob("am_*.json"):
        old.unlink()
    rows = []
    for mob, (name, where, pokemon, drops, note) in MOBS.items():
        yes, no = biomes_of(config_dir, mob)
        condition = {"biomes": yes}
        if where == "cave":
            condition["canSeeSky"] = False
        spawns = []
        for species, bucket, levels, weight in pokemon:
            spawn = {"id": f"ecosystems_untamed-{mob}-{species}", "pokemon": species, "type": "pokemon",
                     "spawnablePositionType": "grounded" if where == "cave" else where,
                     "bucket": bucket, "level": levels, "weight": float(weight), "condition": condition}
            if no:
                spawn["anticondition"] = {"biomes": no}
            if drops:
                spawn["drops"] = drop_table(drops)
            spawns.append(spawn)
        write(pool / f"am_{mob}.json", {"enabled": True, "neededInstalledMods": ["alexsmobs"],
                                         "neededUninstalledMods": [], "spawns": spawns})
        rows.append((name, pokemon, where, yes, no, drops, note))
    write_md(docs / "pokemon-do-alexs-mobs.md", rows)
    print(f"{len(rows)} bichos com Pokémon, {len(NO_POKEMON)} sem substituto")


def write_md(path, rows):
    pretty = lambda b: b.replace("#minecraft:", "#").replace("minecraft:", "")
    lines = [
        "# Pokémon no lugar do Alex's Mobs",
        "",
        "Gerado por `tools/untamed_spawns.py`. **Edite à vontade** (Pokémon, raridade, níveis, drops) e me avise: eu passo",
        "as mudanças para o script e para o jogo.",
        "",
        "- Todos os bichos do Alex's Mobs saem do jogo. Os da tabela dão lugar a Pokémon, que nascem nos mesmos biomas.",
        "- Os **drops só valem para quem nasce no lugar do bicho**: o mesmo Pokémon nascido em outro lugar dá os drops",
        "  normais do Cobblemon. Eles repõem os itens que só saíam dos bichos (pelo de urso, escamas, penas...).",
        "- Raridade: common, uncommon, rare (do Cobblemon). Peso: quanto aparece dentro da mesma raridade.",
        "- Biomas: os do Alex's Mobs (tags com #). \"Menos\" são os biomas onde não nasce.",
        "",
        "| Bicho | Pokémon (raridade, níveis, peso) | Onde | Biomas | Drops | Obs. |",
        "|---|---|---|---|---|---|",
    ]
    for name, pokemon, where, yes, no, drops, note in rows:
        poke = "<br>".join(f"{s.title()} ({b}, {lv}, {w})" for s, b, lv, w in pokemon)
        biomes = ", ".join(pretty(b) for b in yes) + (f"<br>menos {', '.join(pretty(b) for b in no)}" if no else "")
        drop_text = "<br>".join(f"{x['item'].split(':')[1]} {x['qty']} ({x['percentage']}%)" for x in drops) or "normais do Cobblemon"
        lines.append(f"| {name} | {poke} | {WHERE[where]} | {biomes} | {drop_text} | {note} |")
    lines += ["", "## Especiais", ""]
    lines += [f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in SPECIAL.items()]
    lines += ["", "## Sem substituto (por enquanto)", "",
              "Saem do jogo e não têm Pokémon no lugar. Ideias são bem-vindas:", ""]
    lines += [f"- {v}" for v in NO_POKEMON.values()]
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
