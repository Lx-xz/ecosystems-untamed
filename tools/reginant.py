# Reginant: a rainha das colônias de Durant (os formigueiros do Alex's Mobs, veja AnthillColonies.java). Espécie nova,
# Inseto/Aço, só fêmea; a Durant fêmea do nível 35 em diante evolui quando recebe Gongylidia (o fungo que a colônia
# cultiva: usar o item nela, como a Dawn Stone na Snorunt fêmea; segurando, ela comeria o fungo). Cada formigueiro tem uma rainha lá dentro, que só sai
# se ele for quebrado.
# - Modelo: o da Durant (mesmos ossos: usa o poser e as animações dela), com uma coroa de três pontas na cabeça, o
#   abdômen maior e as duas asas de rainha de formiga nas costas.
# - Textura: a da Durant com a armadura dourada e as partes escuras roxas (realeza), mantendo a luz e o desenho do
#   original; os olhos continuam. Shiny: armadura de platina e partes escuras verde-azuladas, com os olhos do shiny
#   da Durant.
# - Asas: membrana translúcida âmbar com as nervuras escuras (camada translúcida por cima).
#
# Uso: python reginant.py <jar do Cobblemon> <pasta resources do mod> [pasta da prévia]
import colorsys
import copy
import json
import math
import sys
import zipfile
from io import BytesIO
from pathlib import Path

from PIL import Image

FOLDER = "0632_durant"
NAME = "reginant"
GOLD = [(70, 40, 10), (128, 82, 18), (186, 136, 36), (228, 186, 72), (250, 226, 140), (255, 246, 200)]
ROYAL = [(22, 8, 30), (44, 16, 58), (70, 30, 92), (102, 52, 128), (136, 82, 160)]
PLATINUM = [(78, 82, 92), (130, 136, 148), (180, 186, 198), (220, 226, 236), (246, 248, 255)]
TEAL = [(8, 34, 38), (16, 60, 66), (30, 92, 98), (52, 128, 130), (86, 164, 160)]
GEM = (210, 30, 60)
WING_MEMBRANE, WING_VEIN = (236, 200, 130, 110), (92, 56, 24, 230)

# Peças novas: (osso, origem, tamanho, tipo[, pivô, rotação])
CROWN = [("head", (x, 11.75, -8.25), (1, h, 1), "crown") for x, h in ((-2.25, 2), (-0.5, 3), (1.25, 2))] + [
    ("head", (x, 11.75, -6.5), (1, 1, 1), "crown") for x in (-2.25, 1.25)]
WINGS = [("torso", (0.5, 13.8, -1), (5, 0, 11), "wing", (0.5, 13.8, 0), (0, 15, -10)),
         ("torso", (-5.5, 13.8, -1), (5, 0, 11), "wing", (-0.5, 13.8, 0), (0, -15, 10))]
# Abdômen maior: o cubo grande cresce (inflate) e vai para trás junto com a ponta.
ABDOMEN = {(8, 8, 6): (2.0, 2.0), (5, 5, 2): (1.0, 4.5)}   # tamanho do cubo: (inflate, quanto vai para trás)


def luma(p):
    return (0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) / 255


def box_faces(uv, size):
    u, v = uv
    w, h, d = size
    faces = [(u + d, v, w, d), (u + d + w, v, w, d), (u, v + d, d, h), (u + d, v + d, w, h),
             (u + d + w, v + d, d, h), (u + 2 * d + w, v + d, w, h)]
    return [f for f in faces if f[2] > 0 and f[3] > 0]


def ramp(ts, t):
    t = max(0.0, min(1.0, t)) * (len(ts) - 1)
    i = min(int(t), len(ts) - 2)
    f = t - i
    return tuple(int(a + (b - a) * f) for a, b in zip(ts[i], ts[i + 1]))


def owner_map(geo, w, h):
    used = [[False] * w for _ in range(h)]
    for bone in geo["bones"]:
        for c in bone.get("cubes", []):
            for x0, y0, fw, fh in box_faces(c["uv"], [math.ceil(v) for v in c["size"]]):
                for y in range(max(0, y0), min(h, y0 + fh)):
                    for x in range(max(0, x0), min(w, x0 + fw)):
                        used[y][x] = True
    return used


def allocate(img, used, size):
    w, h, d = size
    bw, bh = math.ceil(2 * d + 2 * w), math.ceil(d + h)
    px = img.load()
    for y in range(img.height - bh, -1, -1):
        for x in range(img.width - bw, -1, -1):
            if not any(used[y + j][x + i] or px[x + i, y + j][3] for i in range(bw) for j in range(bh)):
                for j in range(bh):
                    for i in range(bw):
                        used[y + j][x + i] = True
                return x, y
    raise ValueError("sem espaço livre na textura")


def build_model(geo_json, texture):
    model = copy.deepcopy(geo_json)
    geo = model["minecraft:geometry"][0]
    geo["description"]["identifier"] = f"geometry.{NAME}"
    geo["description"]["visible_bounds_width"] = 4
    used = owner_map(geo, texture.width, texture.height)
    uvs, kinds = {}, []
    for bone in geo["bones"]:
        if bone["name"] == "back":
            for c in bone["cubes"]:
                grow, back = ABDOMEN.get(tuple(c["size"]), (0, 0))
                c["inflate"] = c.get("inflate", 0) + grow
                c["origin"][2] += back
    for part in CROWN + WINGS:
        bone_name, origin, size, kind = part[:4]
        if size not in uvs:
            uvs[size] = allocate(texture, used, size)
        cube = {"origin": list(origin), "size": list(size), "uv": list(uvs[size])}
        if len(part) > 4:
            cube["pivot"], cube["rotation"] = list(part[4]), list(part[5])
        if kind == "wing":
            # Plano fino: as faces de cima e de baixo ficariam no mesmo lugar e, na camada translúcida, piscariam.
            cube["inflate"] = 0.02
        next(b for b in geo["bones"] if b["name"] == bone_name)["cubes"].append(cube)
        kinds.append((kind, size, uvs[size]))
    return model, kinds


def recolor(texture, shiny_eyes, light_tones, dark_tones):
    src = texture.convert("RGBA")
    out = src.copy()
    sp, op = src.load(), out.load()
    lum = [luma(sp[x, y]) for y in range(src.height) for x in range(src.width) if sp[x, y][3]]
    lo, hi = min(lum), max(lum)
    split = 0.42
    for y in range(src.height):
        for x in range(src.width):
            p = sp[x, y]
            if not p[3]:
                continue
            if colorsys.rgb_to_hsv(*(c / 255 for c in p[:3]))[1] > 0.4:
                if shiny_eyes is not None:
                    op[x, y] = shiny_eyes.getpixel((x, y))
                continue                     # olhos (vermelhos no normal)
            t = (luma(p) - lo) / (hi - lo)
            if t >= split:
                op[x, y] = ramp(light_tones, (t - split) / (1 - split)) + (p[3],)
            else:
                op[x, y] = ramp(dark_tones, t / split) + (p[3],)
    return out


def paint_parts(img, layer, kinds, light_tones):
    p, lp = img.load(), layer.load()
    for kind, size, (u, v) in kinds:
        w, h, d = [math.ceil(s) for s in size]
        if kind == "crown":
            for x0, y0, fw, fh in box_faces((u, v), (w, h, d)):
                for j in range(fh):
                    for i in range(fw):
                        # Mais claro na ponta, mais escuro na base, com um brilho de lado.
                        t = 0.35 + 0.55 * (1 - j / max(1, fh - 1)) + (0.1 if i == 0 else 0)
                        p[x0 + i, y0 + j] = ramp(light_tones, t) + (255,)
            if h == 3:   # a ponta do meio tem uma pedra vermelha na frente
                p[u + d, v + d + 1] = GEM + (255,)
        elif kind == "wing":
            for x0, y0, fw, fh in box_faces((u, v), (w, h, d)):
                for j in range(fh):
                    for i in range(fw):
                        # Nervuras: a borda da frente e duas que vão da base para a ponta, abrindo.
                        vein = i == 0 or j == 0 or i == int(1 + j * 0.25) or i == int(2.5 + j * 0.15)
                        tip = j > fh - 2 and i > fw - 3
                        if tip:
                            continue          # ponta arredondada
                        lp[x0 + i, y0 + j] = WING_VEIN if vein else WING_MEMBRANE
                        p[x0 + i, y0 + j] = (0, 0, 0, 0)


# Golpes por nível: a rainha manda na colônia. As três "ordens" (Attack, Defend e Heal Order, os golpes de comando da
# Vespiquen), Beat Up (chama as operárias), Instruct (manda repetir o golpe) e Victory Dance; troca a Agility da
# Durant por Iron Defense (é lenta) e o Guillotine por First Impression no fim.
LEVEL_MOVES = ["1:attackorder", "1:defendorder", "1:healorder", "1:sandattack", "1:furycutter", "1:visegrip",
               "1:metalclaw", "12:beatup", "16:bugbite", "20:bite", "24:irondefense", "28:dig", "32:xscissor",
               "35:defendorder", "38:instruct", "42:ironhead", "46:attackorder", "50:healorder", "54:crunch",
               "58:victorydance", "64:firstimpression"]


def species_json(durant):
    # Os golpes por nível são os dela; os de TM, tutor, ovo e antigos vêm da Durant.
    moves = LEVEL_MOVES + [m for m in durant["moves"] if not m.split(":")[0].isdigit()]
    behaviour = copy.deepcopy(durant["behaviour"])
    behaviour["herd"]["toleratedLeaders"] = [{"pokemon": "reginant", "tier": 2}]
    return {
        "implemented": True,
        "nationalPokedexNumber": 10632,
        "name": "Reginant",
        "primaryType": "bug",
        "secondaryType": "steel",
        "maleRatio": 0,
        "height": 8,
        "weight": 900,
        "pokedex": ["cobblemon.species.reginant.desc"],
        "labels": ["custom", "ecosystems_untamed"],
        "aspects": [],
        # Queenly Majesty (ninguém age antes dela: bloqueia golpes de prioridade), Swarm (da Durant) e, escondida,
        # Steelworker (golpes de Aço mais fortes, para uma Inseto/Aço que bate).
        "abilities": ["queenlymajesty", "swarm", "h:steelworker"],
        "eggGroups": ["bug"],
        # A rainha é a tanque da colônia: muito mais vida e defesa que a Durant (58/109/112/48/48/109), ataque um pouco
        # maior e bem mais lenta (é a operária que corre). Total 560.
        "baseStats": {"hp": 95, "attack": 115, "defence": 140, "special_attack": 55, "special_defence": 105, "speed": 50},
        "evYield": {"hp": 1, "attack": 0, "defence": 2, "special_attack": 0, "special_defence": 0, "speed": 0},
        "baseExperienceYield": 205,
        "experienceGroup": durant["experienceGroup"],
        "catchRate": 45,
        "eggCycles": durant["eggCycles"],
        "baseFriendship": durant["baseFriendship"],
        "baseScale": 1.2,
        "hitbox": {"width": 1.4, "height": 1.3, "fixed": False},
        "drops": {"amount": 2, "entries": [{"item": "minecraft:raw_iron", "quantityRange": "1-2"},
                                           {"item": "minecraft:raw_gold", "quantityRange": "0-1"},
                                           {"item": "alexsmobs:gongylidia", "percentage": 25}]},
        "preEvolution": "durant",
        "evolutions": [],
        "behaviour": behaviour,
        "moves": moves,
    }


def durant_addition(durant):
    behaviour = copy.deepcopy(durant["behaviour"])
    behaviour["herd"]["toleratedLeaders"].append({"pokemon": "reginant", "tier": 2})
    return {"target": "cobblemon:durant", "evolutions": [{
        "id": "durant_reginant", "variant": "item_interact", "result": "reginant", "consumeHeldItem": False,
        "learnableMoves": ["defendorder"], "requiredContext": "alexsmobs:gongylidia",
        "requirements": [{"variant": "level", "minLevel": 35}, {"variant": "properties", "target": "gender=female"}]}],
        "behaviour": behaviour}


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main():
    z = zipfile.ZipFile(sys.argv[1])
    res = Path(sys.argv[2])
    preview = Path(sys.argv[3]) if len(sys.argv) > 3 else None
    durant = json.loads(z.read("data/cobblemon/species/generation5/durant.json"))
    texture = Image.open(BytesIO(z.read(f"assets/cobblemon/textures/pokemon/{FOLDER}/durant.png"))).convert("RGBA")
    shiny_src = Image.open(BytesIO(z.read(f"assets/cobblemon/textures/pokemon/{FOLDER}/durant_shiny.png"))).convert("RGBA")
    geo_json = json.loads(z.read(f"assets/cobblemon/bedrock/pokemon/models/{FOLDER}/durant.geo.json"))
    model, kinds = build_model(geo_json, texture)

    tex_dir = res / f"assets/ecosystems_untamed/textures/pokemon/{NAME}"
    tex_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for suffix, eyes, light, dark in (("", None, GOLD, ROYAL), ("_shiny", shiny_src, PLATINUM, TEAL)):
        img = recolor(texture, eyes, light, dark)
        wings = Image.new("RGBA", img.size, (0, 0, 0, 0))
        paint_parts(img, wings, kinds, light)
        img.save(tex_dir / f"{NAME}{suffix}.png")
        wings.save(tex_dir / f"{NAME}{suffix}_wings.png")
        results.append(Image.alpha_composite(img, wings))
    write_json(res / f"assets/ecosystems_untamed/bedrock/pokemon/models/{NAME}.geo.json", model)

    tex = f"ecosystems_untamed:textures/pokemon/{NAME}/{NAME}"
    wings_layer = lambda s: [{"name": "wings", "texture": f"{tex}{s}_wings.png", "translucent": True}]
    write_json(res / f"assets/cobblemon/bedrock/pokemon/resolvers/10632_{NAME}/0_{NAME}_base.json", {
        "species": f"cobblemon:{NAME}", "order": 0, "variations": [
            {"aspects": [], "poser": "cobblemon:durant", "model": f"ecosystems_untamed:{NAME}.geo",
             "texture": f"{tex}.png", "layers": wings_layer("")},
            {"aspects": ["shiny"], "texture": f"{tex}_shiny.png", "layers": wings_layer("_shiny")}]})
    write_json(res / f"data/cobblemon/species/custom/{NAME}.json", species_json(durant))
    write_json(res / f"data/ecosystems_untamed/species_additions/durant_{NAME}.json", durant_addition(durant))
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
        sheet = Image.new("RGBA", (texture.width * 3 * 6, texture.height * 6), (90, 90, 90, 255))
        for i, img in enumerate([texture] + results):
            sheet.alpha_composite(img.resize((img.width * 6, img.height * 6), Image.NEAREST), (i * img.width * 6, 0))
        sheet.save(preview / f"{NAME}_preview.png")


if __name__ == "__main__":
    main()
