# Community boards

> **Community ports.** NebulaOS is made and tested for the Ender-3 V3 KE. These printers run it
> thanks to owners who use it and share what they find - no guarantee, and the community helps
> each other. Got one working, found a fix, or stuck? Tell us on
> [Discord](https://discord.com/invite/k3HdqpdB) or in an issue, so everyone else gets it too.

NebulaOS is made for the Creality Ender-3 V3 KE. These folders let owners of other printers in the
**Ender-3 V3 family** run NebulaOS on a Nebula Pad. Each has the printer configuration and a
step-by-step how-to. The ready-made mainboard firmwares are in every
[NebulaOS release](https://github.com/NebulaOS-KE/NebulaOS/releases/latest).

| Printer | Mainboard chip | Status | Folder |
|---|---|---|---|
| Ender-3 V3 SE | GD32F303 (every C13, some C14) | **Community proven** | [`ender-3-v3-se`](ender-3-v3-se) |
| Ender-3 V3 SE | STM32F401 (some C14) | Untested with NebulaOS - first testers wanted | [`ender-3-v3-se`](ender-3-v3-se) |

**Community proven** means: people run NebulaOS on it and told us so. A board moves there after
two independent "It works on my printer" reports (or one, while we wait for more testers).

**Tell us:** [It works on my printer](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-works.yml) ·
[I found a fix](https://github.com/NebulaOS-KE/NebulaOS/issues/new?template=community-fix.yml)

Every NebulaOS release builds the mainboard firmwares from the recipes in
[NebulaOS-klipper-mcu](https://github.com/NebulaOS-KE/NebulaOS-klipper-mcu/tree/main/community),
with exactly the official Klipper that release runs.
