package com.luiz.ecosystemsuntamed;

import com.cobblemon.mod.common.api.pokemon.PokemonSpecies;
import com.cobblemon.mod.common.api.pokemon.evolution.Evolution;
import com.cobblemon.mod.common.entity.pokemon.PokemonEntity;
import com.cobblemon.mod.common.pokemon.Gender;
import com.cobblemon.mod.common.pokemon.Pokemon;
import com.cobblemon.mod.common.pokemon.Species;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerInteractEvent;

/**
 * A Durant fêmea do nível 35 em diante vira Reginant (a rainha da colônia) quando o dono usa Gongylidia nela.
 * <p>
 * A evolução está nos dados (species_additions/durant_reginant.json, "item_interact"), mas a Gongylidia é comida: o
 * Cobblemon dava o fungo para ela comer em vez de tentar a evolução. Aqui o uso do fungo é visto antes de tudo: se
 * a evolução dos dados vale para ela (fêmea, nível), ela evolui como qualquer outra (com a animação do Cobblemon) e
 * gasta um fungo.
 */
@EventBusSubscriber(modid = EcosystemsUntamed.MOD_ID)
public final class QueenEvolution {
    private static final ResourceLocation GONGYLIDIA = ResourceLocation.fromNamespaceAndPath("alexsmobs", "gongylidia");
    private static final String EVOLUTION_ID = "durant_reginant";

    private QueenEvolution() {}

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onInteract(PlayerInteractEvent.EntityInteract event) {
        Player player = event.getEntity();
        ItemStack stack = event.getItemStack();
        if (!(event.getTarget() instanceof PokemonEntity entity) || !GONGYLIDIA.equals(BuiltInRegistries.ITEM.getKey(stack.getItem()))) return;
        Pokemon pokemon = entity.getPokemon();
        // Só a Durant do próprio jogador (como as pedras de evolução).
        if (!player.getUUID().equals(entity.getOwnerUUID())
                || !pokemon.getSpecies().getResourceIdentifier().getPath().equals("durant")) return;
        event.setCanceled(true);
        event.setCancellationResult(InteractionResult.sidedSuccess(player.level().isClientSide()));
        if (player.level().isClientSide()) return;

        if (pokemon.getGender() != Gender.FEMALE || pokemon.getLevel() < 35) {
            player.displayClientMessage(Component.translatable("message.ecosystems_untamed.reginant_not_ready"), true);
            return;
        }
        Evolution evolution = null;
        for (Evolution e : pokemon.getEvolutions()) {
            if (EVOLUTION_ID.equals(e.getId())) evolution = e;
        }
        if (evolution != null) {
            if (!evolution.evolve(pokemon)) return;
        } else {
            // Os dados da evolução não chegaram (outro pacote de dados sobrescreveu a Durant?): troca a espécie direto.
            Species reginant = PokemonSpecies.INSTANCE.getByName("reginant");
            if (reginant == null) return;
            EcosystemsUntamed.LOGGER.warn("Evolução {} não encontrada na Durant: trocando a espécie direto", EVOLUTION_ID);
            pokemon.setSpecies(reginant);
        }
        if (!player.getAbilities().instabuild) stack.shrink(1);
    }
}
