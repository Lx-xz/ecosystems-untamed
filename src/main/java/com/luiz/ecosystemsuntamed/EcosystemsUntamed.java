package com.luiz.ecosystemsuntamed;

import org.slf4j.Logger;

import com.mojang.logging.LogUtils;

import net.neoforged.fml.common.Mod;

/**
 * Cobblemon Ecosystems: Untamed. Compat do mod base com o Alex's Mobs (port do Raguto): os bichos do Alex's Mobs dão
 * lugar a Pokémon, que herdam o que eles faziam (formigueiros, bananas, drops...).
 */
@Mod(EcosystemsUntamed.MOD_ID)
public class EcosystemsUntamed {
    public static final String MOD_ID = "ecosystems_untamed";
    public static final Logger LOGGER = LogUtils.getLogger();
}
