package com.luiz.ecosystemsuntamed;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import com.cobblemon.mod.common.api.pokemon.PokemonProperties;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.github.alexthe666.alexsmobs.tileentity.TileEntityLeafcutterAnthill;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.ai.memory.MemoryModuleType;
import net.minecraft.world.entity.ai.memory.WalkTarget;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.chunk.LevelChunk;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.level.ChunkEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

/**
 * Formigueiros do Alex's Mobs viram colônias de Durant, como as colmeias do mod base viram colônias de Combee.
 * <ul>
 *   <li>Quando o formigueiro carrega (ou tenta soltar uma formiga, que o mod base bloqueia), as formigas de dentro
 *       somem e nascem de 2 a 4 Durant que moram ali.</li>
 *   <li>De dia, cada Durant vai até as folhas das árvores por perto, "corta" um pedaço e leva para o formigueiro: o
 *       fungo da câmara cresce, como fazia com as formigas (o jogador continua colhendo o gongylidia).</li>
 *   <li>Eles não se afastam muito de casa. Capturados, viram Durant normais.</li>
 * </ul>
 */
@EventBusSubscriber(modid = EcosystemsUntamed.MOD_ID)
public final class AnthillColonies {
    private static final ResourceLocation LEAFCUTTER_ANT = ResourceLocation.fromNamespaceAndPath("alexsmobs", "leafcutter_ant");
    private static final String HOME_KEY = EcosystemsUntamed.MOD_ID + ":anthill";
    private static final String CARRYING_KEY = EcosystemsUntamed.MOD_ID + ":carrying_leaf";
    private static final String LEAF_KEY = EcosystemsUntamed.MOD_ID + ":leaf_target";
    private static final String NEXT_TRIP_KEY = EcosystemsUntamed.MOD_ID + ":next_trip";
    /** No formigueiro: a colônia já nasceu. */
    private static final String COLONY_KEY = EcosystemsUntamed.MOD_ID + ":colony";
    private static final int MIN_COLONY = 2, MAX_COLONY = 4;
    private static final int LEAF_RADIUS = 10, HOME_RADIUS = 20;
    /** Descanso entre uma viagem e outra: 30 a 90 s. */
    private static final int REST_MIN = 600, REST_EXTRA = 1200;

    private record Pending(ServerLevel level, BlockPos pos) {}
    private static final List<Pending> pending = new ArrayList<>();
    private static final Set<PokemonEntity> workers = new HashSet<>();
    private static Field antsField;
    private static int tick;

    private AnthillColonies() {}

    // ----- Colônias -----

    @SubscribeEvent
    public static void onChunkLoad(ChunkEvent.Load event) {
        if (!(event.getLevel() instanceof ServerLevel level) || !(event.getChunk() instanceof LevelChunk chunk)) return;
        for (BlockEntity be : chunk.getBlockEntities().values()) {
            if (be instanceof TileEntityLeafcutterAnthill && !be.getPersistentData().getBoolean(COLONY_KEY)) {
                pending.add(new Pending(level, be.getBlockPos()));
            }
        }
    }

    /** Formiga saindo do formigueiro, bloqueada pelo mod base: o formigueiro vira colônia de Durant. */
    @SubscribeEvent(priority = EventPriority.LOWEST, receiveCanceled = true)
    public static void onEntityJoin(EntityJoinLevelEvent event) {
        if (!(event.getLevel() instanceof ServerLevel level)) return;
        Entity entity = event.getEntity();
        if (entity instanceof PokemonEntity pokemon && pokemon.getPersistentData().contains(HOME_KEY)) {
            workers.add(pokemon);
            return;
        }
        if (!event.isCanceled() || !LEAFCUTTER_ANT.equals(BuiltInRegistries.ENTITY_TYPE.getKey(entity.getType()))) return;
        BlockPos.betweenClosedStream(entity.blockPosition().offset(-3, -3, -3), entity.blockPosition().offset(3, 3, 3))
                .filter(pos -> level.getBlockEntity(pos) instanceof TileEntityLeafcutterAnthill)
                .findFirst()
                .ifPresent(pos -> pending.add(new Pending(level, pos.immutable())));
    }

    @SubscribeEvent
    public static void onServerTick(ServerTickEvent.Post event) {
        for (Pending p : List.copyOf(pending)) createColony(p.level(), p.pos());
        pending.clear();
        if (++tick % 40 == 0) workAll();
    }

    private static void createColony(ServerLevel level, BlockPos pos) {
        if (!(level.getBlockEntity(pos) instanceof TileEntityLeafcutterAnthill anthill)) return;
        clearAnts(anthill);
        if (anthill.getPersistentData().getBoolean(COLONY_KEY)) return;
        anthill.getPersistentData().putBoolean(COLONY_KEY, true);
        anthill.setChanged();
        int count = MIN_COLONY + level.random.nextInt(MAX_COLONY - MIN_COLONY + 1);
        for (int i = 0; i < count; i++) {
            PokemonEntity durant = PokemonProperties.Companion.parse("durant level=" + (10 + level.random.nextInt(16))).createEntity(level);
            durant.moveTo(pos.getX() + 0.5 + level.random.nextInt(5) - 2, pos.getY() + 1, pos.getZ() + 0.5 + level.random.nextInt(5) - 2,
                    level.random.nextFloat() * 360f, 0f);
            durant.getPersistentData().putLong(HOME_KEY, pos.asLong());
            if (level.addFreshEntity(durant)) workers.add(durant);
        }
    }

    /** Tira as formigas guardadas no formigueiro (senão ele tenta soltá-las sem parar). */
    @SuppressWarnings("unchecked")
    private static void clearAnts(TileEntityLeafcutterAnthill anthill) {
        try {
            if (antsField == null) {
                antsField = TileEntityLeafcutterAnthill.class.getDeclaredField("ants");
                antsField.setAccessible(true);
            }
            ((List<Object>) antsField.get(anthill)).clear();
            anthill.setChanged();
        } catch (ReflectiveOperationException e) {
            EcosystemsUntamed.LOGGER.warn("Não deu para esvaziar o formigueiro em {}", anthill.getBlockPos(), e);
        }
    }

    // ----- Trabalho dos Durant -----

    private static void workAll() {
        workers.removeIf(pokemon -> {
            if (pokemon.isRemoved() || pokemon.getOwnerUUID() != null || !pokemon.getPersistentData().contains(HOME_KEY)) return true;
            if (!(pokemon.level() instanceof ServerLevel level) || pokemon.isBusy()) return false;
            work(level, pokemon);
            return false;
        });
    }

    private static void work(ServerLevel level, PokemonEntity durant) {
        CompoundTag data = durant.getPersistentData();
        BlockPos home = BlockPos.of(data.getLong(HOME_KEY));
        if (!level.isLoaded(home)) return;
        if (!(level.getBlockEntity(home) instanceof TileEntityLeafcutterAnthill anthill)) {
            data.remove(HOME_KEY); // o formigueiro sumiu: vira um Durant comum
            return;
        }
        double toHome = durant.position().distanceTo(home.getCenter());

        if (data.getBoolean(CARRYING_KEY)) {
            if (toHome > 2.5) {
                walkTo(durant, home, 0.5f);
            } else {
                anthill.growFungus();
                data.putBoolean(CARRYING_KEY, false);
                data.putLong(NEXT_TRIP_KEY, level.getGameTime() + REST_MIN + level.random.nextInt(REST_EXTRA));
                level.sendParticles(ParticleTypes.HAPPY_VILLAGER, home.getX() + 0.5, home.getY() + 1.1, home.getZ() + 0.5, 4, 0.3, 0.1, 0.3, 0);
            }
            return;
        }
        if (toHome > HOME_RADIUS) {
            walkTo(durant, home, 0.5f);
            return;
        }
        if (!level.isDay() || level.getGameTime() < data.getLong(NEXT_TRIP_KEY)) return;

        BlockPos leaf = data.contains(LEAF_KEY) ? BlockPos.of(data.getLong(LEAF_KEY)) : findLeaf(level, home, durant);
        if (leaf == null || !level.getBlockState(leaf).is(BlockTags.LEAVES)) {
            data.remove(LEAF_KEY);
            data.putLong(NEXT_TRIP_KEY, level.getGameTime() + REST_MIN);
            return;
        }
        data.putLong(LEAF_KEY, leaf.asLong());
        if (durant.position().distanceTo(leaf.getCenter()) > 3) {
            walkTo(durant, leaf, 0.5f);
            return;
        }
        // Cortou um pedaço da folha (a árvore fica inteira) e leva para casa.
        BlockState state = level.getBlockState(leaf);
        level.sendParticles(new BlockParticleOption(ParticleTypes.BLOCK, state), leaf.getX() + 0.5, leaf.getY() + 0.5, leaf.getZ() + 0.5,
                12, 0.3, 0.3, 0.3, 0.05);
        data.remove(LEAF_KEY);
        data.putBoolean(CARRYING_KEY, true);
    }

    /** Uma folha de árvore perto do formigueiro (sorteando posições, sem varrer tudo). */
    private static BlockPos findLeaf(ServerLevel level, BlockPos home, PokemonEntity durant) {
        for (int i = 0; i < 40; i++) {
            BlockPos pos = home.offset(durant.getRandom().nextInt(LEAF_RADIUS * 2 + 1) - LEAF_RADIUS,
                    durant.getRandom().nextInt(8), durant.getRandom().nextInt(LEAF_RADIUS * 2 + 1) - LEAF_RADIUS);
            if (level.isLoaded(pos) && level.getBlockState(pos).is(BlockTags.LEAVES)) return pos;
        }
        return null;
    }

    private static void walkTo(PokemonEntity pokemon, BlockPos pos, float speed) {
        pokemon.getBrain().setMemory(MemoryModuleType.WALK_TARGET, new WalkTarget(pos, speed, 1));
    }
}
