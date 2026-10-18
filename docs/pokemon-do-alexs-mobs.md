# Pokémon no lugar do Alex's Mobs

Gerado por `tools/untamed_spawns.py`. **Edite à vontade** (Pokémon, raridade, níveis, drops) e me avise: eu passo
as mudanças para o script e para o jogo.

- Todos os bichos do Alex's Mobs saem do jogo. Os da tabela dão lugar a Pokémon, que nascem nos mesmos biomas.
- Os **drops só valem para quem nasce no lugar do bicho**: o mesmo Pokémon nascido em outro lugar dá os drops
  normais do Cobblemon. Eles repõem os itens que só saíam dos bichos (pelo de urso, escamas, penas...).
- Raridade: common, uncommon, rare (do Cobblemon). Peso: quanto aparece dentro da mesma raridade.
- Biomas: os do Alex's Mobs (tags com #). "Menos" são os biomas onde não nasce.

| Bicho | Pokémon (raridade, níveis, peso) | Onde | Biomas | Drops | Obs. |
|---|---|---|---|---|---|
| Grizzly Bear | Teddiursa (common, 8-25, 6)<br>Ursaring (uncommon, 30-45, 1) | chão | #is_forest, #is_taiga, cherry_grove<br>menos sparse_jungle | bear_fur 1 (50%) |  |
| Blue Jay | Taillow (common, 5-20, 6)<br>Swellow (rare, 22-40, 1) | chão | #is_forest, #is_taiga, cherry_grove<br>menos sparse_jungle | feather 1 (50%) |  |
| Crow | Rookidee (common, 5-20, 6)<br>Corvisquire (uncommon, 18-35, 2)<br>Corviknight (rare, 38-50, 0.5) | chão | #c:is_plains, #is_forest, #is_taiga, cherry_grove<br>menos #is_savanna | feather 1 (50%) |  |
| Raccoon | Zigzagoon (common, 5-20, 6)<br>Linoone (uncommon, 20-35, 2) | chão | #is_forest, #c:is_plains, #is_taiga, cherry_grove<br>menos #is_savanna | raccoon_tail 1 (25%) |  |
| Skunk | Stunky (common, 8-25, 5)<br>Skuntank (rare, 34-45, 1) | chão | #is_forest, cherry_grove<br>menos #is_savanna, #c:is_cold_overworld, sparse_jungle | skunk_spray 1 (20%) |  |
| Tasmanian Devil | Poochyena (common, 8-20, 5)<br>Mightyena (rare, 18-35, 1) | chão | #is_forest<br>menos #is_savanna, #c:is_cold_overworld, sparse_jungle | normais do Cobblemon |  |
| Sugar Glider | Emolga (uncommon, 10-30, 4)<br>Pachirisu (uncommon, 10-30, 3) | chão | birch_forest, old_growth_birch_forest | normais do Cobblemon |  |
| Bison | Bouffalant (uncommon, 20-40, 4) | chão | #c:is_plains, meadow<br>menos #is_savanna, #c:is_hot_overworld | beef 1-2 (60%)<br>bison_fur 1 (50%) |  |
| Potoo | Hoothoot (common, 8-20, 5)<br>Noctowl (rare, 20-40, 1) | chão | dark_forest | feather 1 (50%) | Floresta escura |
| Bald Eagle | Rufflet (uncommon, 15-30, 4)<br>Braviary (rare, 54-60, 0.5) | chão | #c:is_coniferous, grove, windswept_forest | feather 1-2 (60%) |  |
| Banana Slug | Shellos (common, 10-25, 5)<br>Gastrodon (rare, 30-45, 1) | chão | old_growth_pine_taiga, old_growth_spruce_taiga, #c:is_rare | banana_slug_slime 1 (50%) | Taigas antigas |
| Moose | Stantler (uncommon, 15-35, 4)<br>Wyrdeer (rare, 35-50, 0.5) | chão | #c:is_wasteland, #is_taiga | moose_ribs 1 (50%)<br>moose_antler 1 (10%) |  |
| Hummingbird | Cutiefly (common, 5-20, 5)<br>Ribombee (rare, 25-40, 1) | chão | flower_forest, sunflower_plains, #is_jungle, meadow, cherry_grove | normais do Cobblemon |  |
| Crocodile | Croconaw (uncommon, 18-30, 3)<br>Feraligatr (rare, 30-50, 1) | chão | #c:is_swamp, mangrove_swamp, #is_river<br>menos #c:is_cold | crocodile_scute 1 (40%)<br>crocodile_egg 1 (5%) |  |
| Caiman | Totodile (common, 5-18, 5) | chão | mangrove_swamp | caiman_egg 1 (5%) | Mangue |
| Alligator Snapping Turtle | Chewtle (common, 8-22, 5)<br>Drednaw (rare, 22-45, 1) | chão | #c:is_swamp<br>menos mangrove_swamp | spiked_scute 1 (20%) |  |
| Anaconda | Ekans (common, 8-20, 4)<br>Arbok (rare, 22-40, 1) | chão | #c:is_swamp, mangrove_swamp | shed_snake_skin 1 (30%) |  |
| Catfish | Barboach (common, 8-25, 6)<br>Whiscash (rare, 30-45, 1) | água | #c:is_swamp, #is_river<br>menos mangrove_swamp, #c:is_cold_overworld | raw_catfish 1 (60%) |  |
| Shoebill | Cramorant (uncommon, 20-40, 3) | chão | #c:is_swamp<br>menos mangrove_swamp | feather 1 (50%) |  |
| Platypus | Psyduck (common, 8-25, 5)<br>Golduck (rare, 33-45, 1) | água | #is_river<br>menos #c:is_cold_overworld | normais do Cobblemon |  |
| Terrapin | Squirtle (uncommon, 5-16, 3)<br>Wartortle (rare, 16-36, 1) | água | #is_river<br>menos #c:is_cold_overworld | normais do Cobblemon |  |
| Mudskipper | Mudkip (uncommon, 5-16, 3)<br>Marshtomp (rare, 16-36, 1) | chão | mangrove_swamp | tropical_fish 1 (30%) | Mangue |
| Capuchin Monkey | Aipom (common, 8-25, 5)<br>Ambipom (rare, 25-40, 1) | chão | #is_jungle, mangrove_swamp<br>menos bamboo_jungle | banana 1 (20%) |  |
| Gorilla | Slakoth (common, 8-18, 4)<br>Vigoroth (uncommon, 18-36, 2)<br>Slaking (rare, 36-50, 0.5) | chão | #is_jungle<br>menos bamboo_jungle | banana 1-2 (30%) |  |
| Toucan | Pikipek (common, 5-14, 5)<br>Trumbeak (uncommon, 14-28, 2)<br>Toucannon (rare, 28-45, 0.5) | chão | #is_jungle<br>menos bamboo_jungle | feather 1 (50%) |  |
| Anteater | Heatmor (uncommon, 20-40, 3) | chão | #is_jungle<br>menos bamboo_jungle | normais do Cobblemon | Caça os Durant dos formigueiros |
| Komodo Dragon | Salandit (common, 10-33, 4)<br>Salazzle (rare, 33-45, 1) | chão | #is_jungle<br>menos #c:is_dense_overworld | komodo_spit 1 (20%) |  |
| Tiger | Litten (uncommon, 5-17, 3)<br>Torracat (rare, 17-34, 1) | chão | bamboo_jungle, cherry_grove | normais do Cobblemon | Selva de bambu |
| Elephant | Phanpy (common, 8-25, 5)<br>Donphan (rare, 25-45, 1) | chão | #is_savanna | acacia_blossom 1 (15%) |  |
| Rhinoceros | Rhyhorn (common, 15-42, 4)<br>Rhydon (rare, 42-55, 0.5) | chão | #is_savanna | normais do Cobblemon |  |
| Gazelle | Deerling (common, 8-34, 5)<br>Sawsbuck (rare, 34-50, 1) | chão | #is_savanna | mutton 1 (50%)<br>gazelle_horn 1 (25%) |  |
| Maned Wolf | Rockruff (uncommon, 10-25, 3)<br>Lycanroc (rare, 25-45, 0.5) | chão | #is_savanna | normais do Cobblemon |  |
| Kangaroo | Kangaskhan (uncommon, 20-40, 3) | chão | #is_badlands, #is_savanna | kangaroo_meat 1 (50%)<br>kangaroo_hide 1 (40%) |  |
| Emu | Doduo (common, 10-31, 5)<br>Dodrio (rare, 31-45, 1) | chão | #is_badlands, #is_savanna | emu_feather 1 (40%)<br>feather 1 (40%)<br>emu_egg 1 (5%) |  |
| Roadrunner | Fletchling (common, 5-17, 5)<br>Fletchinder (uncommon, 17-35, 1) | chão | #is_badlands, #c:is_sandy | roadrunner_feather 1 (40%) |  |
| Rattlesnake | Seviper (uncommon, 15-40, 4) | chão | #is_badlands, #c:is_sandy | rattlesnake_rattle 1 (30%) |  |
| Jerboa | Sandshrew (common, 8-22, 5)<br>Sandslash (rare, 22-40, 1) | chão | #c:is_sandy<br>menos #is_badlands | normais do Cobblemon |  |
| Rain Frog | Croagunk (uncommon, 10-37, 3) | chão | #c:is_sandy<br>menos #is_badlands | normais do Cobblemon |  |
| Tarantula Hawk | Beedrill (uncommon, 15-40, 3) | chão | #c:is_sandy<br>menos #is_badlands | tarantula_hawk_wing_fragment 1 (30%) |  |
| Triops | Kabuto (uncommon, 10-30, 3) | água | #c:is_sandy<br>menos #is_badlands | normais do Cobblemon | Poças do deserto |
| Gelada Monkey | Mankey (common, 8-28, 5)<br>Primeape (rare, 28-45, 1) | chão | #c:is_plateau | normais do Cobblemon |  |
| Snow Leopard | Absol (uncommon, 20-45, 2) | chão | #c:is_snowy, snowy_slopes, frozen_peaks, jagged_peaks | normais do Cobblemon |  |
| Tusklin | Swinub (common, 8-33, 5)<br>Piloswine (uncommon, 33-45, 1)<br>Mamoswine (rare, 45-60, 0.3) | chão | ice_spikes, #c:is_plains | porkchop 1 (50%)<br>snowball 1 (40%) |  |
| Froststalker | Sneasel (uncommon, 15-40, 3) | chão | ice_spikes, frozen_peaks | froststalker_horn 1 (20%) |  |
| Sunbird | Fletchinder (uncommon, 17-35, 2)<br>Talonflame (rare, 35-50, 0.5) | chão | #is_mountain, snowy_slopes, frozen_peaks, jagged_peaks | normais do Cobblemon |  |
| Seagull | Wingull (common, 5-25, 6)<br>Pelipper (rare, 25-45, 1) | chão | #is_beach, stony_shore | feather 1 (50%) |  |
| Lobster | Corphish (common, 8-30, 5)<br>Crawdaunt (rare, 30-45, 1) | chão | #is_beach, stony_shore | lobster_tail 1 (50%) |  |
| Seal | Seel (common, 10-34, 4)<br>Spheal (common, 10-32, 3)<br>Dewgong (rare, 34-50, 1) | chão | #is_beach, #c:is_cold_overworld, stony_shore | normais do Cobblemon |  |
| Cachalot Whale | Wailmer (uncommon, 15-40, 3)<br>Wailord (rare, 40-55, 1) | água | #c:is_cold_overworld, lukewarm_ocean, deep_ocean, deep_lukewarm_ocean | ambergris 1 (10%)<br>cachalot_whale_tooth 1 (10%) |  |
| Orca | Finizen (uncommon, 15-38, 3)<br>Palafin (rare, 38-50, 0.5) | água | #c:is_cold_overworld | normais do Cobblemon |  |
| Hammerhead Shark | Carvanha (common, 10-30, 4)<br>Sharpedo (rare, 30-45, 1) | água | #c:is_hot_overworld | shark_tooth 1 (30%) |  |
| Frilled Shark | Relicanth (rare, 20-45, 1) | água | #is_deep_ocean | serrated_shark_tooth 1 (10%) |  |
| Giant Squid | Inkay (uncommon, 10-30, 3)<br>Malamar (rare, 30-50, 1) | água | #is_deep_ocean | ink_sac 1-3 (60%)<br>lost_tentacle 1 (5%) |  |
| Blobfish | Alomomola (uncommon, 20-45, 3) | água | #is_deep_ocean | blobfish 1 (40%) |  |
| Comb Jelly | Frillish (common, 10-40, 4)<br>Jellicent (rare, 40-55, 0.5) | água | frozen_ocean, deep_frozen_ocean | rainbow_jelly 1 (40%) |  |
| Flying Fish | Mantyke (common, 10-30, 4)<br>Mantine (rare, 30-45, 0.5) | água | #is_ocean<br>menos #c:is_cold_overworld, #c:is_hot_overworld, deep_ocean, deep_lukewarm_ocean | flying_fish 1 (40%) |  |
| Mimic Octopus | Remoraid (common, 10-25, 4)<br>Octillery (rare, 25-45, 1) | água | #is_ocean<br>menos deep_warm_ocean | ink_sac 1 (50%) |  |
| Mantis Shrimp | Krabby (common, 10-28, 4)<br>Kingler (rare, 28-45, 1) | água | #c:is_hot_overworld, mangrove_swamp | normais do Cobblemon |  |
| Cave Centipede | Venipede (common, 10-22, 5)<br>Whirlipede (uncommon, 22-30, 2)<br>Scolipede (rare, 30-45, 0.5) | caverna | #is_overworld<br>menos #is_ocean, #c:is_mushroom, deep_dark | centipede_leg 1 (30%) |  |
| Cockroach | Nincada (common, 8-20, 5)<br>Ninjask (rare, 20-40, 1) | caverna | #is_overworld<br>menos #is_ocean, #c:is_mushroom, deep_dark | cockroach_wing_fragment 1 (40%)<br>cockroach_ootheca 1 (5%) |  |
| Rocky Roller | Geodude (common, 10-25, 5)<br>Graveler (uncommon, 25-40, 2)<br>Golem (rare, 40-55, 0.3) | caverna | dripstone_caves | rocky_shell 1 (15%)<br>tuff 1 (40%)<br>pointed_dripstone 1 (40%) | Cavernas de espeleotema |
| Flutter | Morelull (common, 10-24, 5)<br>Shiinotic (rare, 24-40, 1) | caverna | lush_caves | spore_blossom 1 (15%) | Cavernas exuberantes |
| Bunfungus | Foongus (common, 10-39, 4)<br>Amoonguss (rare, 39-50, 1) | chão | #c:is_rare | red_mushroom 1-2 (50%) |  |
| Mungus | Paras (common, 8-24, 5)<br>Parasect (rare, 24-45, 1) | chão | #c:is_rare | mungal_spores 1 (20%) |  |
| Dropbear | Komala (uncommon, 20-45, 2) | chão | nether_wastes | dropbear_claw 1 (30%) |  |
| Soul Vulture | Murkrow (common, 15-35, 4)<br>Honchkrow (rare, 35-50, 1) | chão | soul_sand_valley | bone 1 (40%)<br>soul_heart 1 (5%) |  |
| Stradpole | Slugma (common, 15-38, 4) | chão | basalt_deltas | normais do Cobblemon |  |
| Straddler | Magcargo (uncommon, 38-50, 2) | chão | basalt_deltas | straddlite 1 (30%)<br>basalt 1 (40%) |  |
| Warped Toad | Tympole (common, 10-25, 4)<br>Palpitoad (uncommon, 25-36, 2)<br>Seismitoad (rare, 36-50, 0.5) | chão | warped_forest | shroomlight 1 (20%)<br>nether_wart 1 (30%) |  |
| Endergrade | Elgyem (common, 20-42, 4)<br>Beheeyem (rare, 42-55, 1) | chão | #is_end<br>menos the_end | normais do Cobblemon |  |
| Enderiophage | Solosis (common, 20-32, 4)<br>Duosion (uncommon, 32-41, 2)<br>Reuniclus (rare, 41-55, 0.5) | chão | #is_end<br>menos the_end, end_barrens, end_highlands, small_end_islands | capsid 1 (20%) |  |
| Mimicube | Ditto (uncommon, 20-50, 3) | chão | #is_end<br>menos the_end | mimicream 1 (30%) |  |
| Spectre | Drifloon (common, 20-28, 4)<br>Drifblim (rare, 28-50, 1) | chão | #is_end<br>menos the_end | normais do Cobblemon |  |

## Especiais

- **Leafcutter Anthill**: Formigueiro: vira colônia de Durant (AnthillColonies)

## Sem substituto (por enquanto)

Saem do jogo e não têm Pokémon no lugar. Ideias são bem-vindas:

- Bone Serpent
- Laviathan
- Crimson Mosquito
- Warped Mosco
- Guster
- Murmur
- Skelewag
- Skreecher
- Underminer
- Void Worm
- Farseer
- Cosmaw
- Cosmic Cod
- Fly
- Devil's Hole Pupfish
- Cachalot Whale (encalhada)
