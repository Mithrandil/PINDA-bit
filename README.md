# PINDA-bit

3D Printed Bit Holder for High-Resolution Heatbed Scanning

This is a simple and useful accessory for Prusa MK2 and MK2S 3D printers (or other printers with an inductive probe). It is a plastic tube that holds a screwdriver bit and allows you to scan the MK42 heatbed with the P.I.N.D.A sensor. This way, you can level the bed for non-magnetic or off-magnet print surfaces.

The advantage of using this accessory is that you can perform finer mesh bed leveling with a 7x7 grid or any arbitrary resolution. This can improve the first layer quality and adhesion on uneven or warped beds. Moreover, since the shape of the MK42 heatbed depends only on the temperature and is consistent between prints, you don't need to scan the bed every time you change the print surface, as long as you use the same temperature. You can also save different presets of the bed mesh for different temperatures and recall them when needed.

However, to scan a print surface that is outside of the magnet points, you need to use custom firmware such as Klipper. You can find an MK2s config here: https://github.com/Mithrandil/klipper-config-prusa-mk2s

In this repository, you will find a module that corrects the tilt of the X-axis before each print. This is necessary because the position of the Z-axis motors is not preserved between prints when they are not powered. Therefore, if you use this accessory to scan a non-magnetic print surface, you need to run this module before printing to ensure a level bed.

# HOW TO USE:

The accessory is easy to use: just insert the bit into the tube and place it on the P.I.N.D.A sensor. The tube should protrude much more than the nozzle so that it can reach the print surface without touching it. Then, run a custom G-code macro to perform a mesh bed leveling with your desired resolution. You can save the mesh in your configuration file for future prints (after removing the tube).

G-Code macro for scanning and saving the high-resolution bed mesh with the accessory at a given temperature:

For 60°C heated bed (accessory mounted):

CREATE_AND_SAVE_NEW_MESH S60; [60 = first_layer_bed_temperature]

For using the saved mesh corrected with a new one (before each print, no accessory mounted):

BED_MESH_CALIBRATE; mesh bed leveling

BED_TILT_CORRECTION SAVEDMESH=MESH60; [60 = first_layer_bed_temperature]

The accessory is also easy to print: it doesn't require any supports or infill, and it takes less than 10 minutes to print. You should use a filament that can withstand high temperatures and does not deform easily, such as PETG or ASA. These filaments are especially recommended if you use an enclosure for your printer.
