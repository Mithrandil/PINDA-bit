# PINDA-bit
3D Printed Bit Holder for high resolution Heatbed Scanning

This is a simple and useful accessory for the Prusa MK2 and MK2S 3D printers (or other printers with an inductive probe). It is a plastic tube that holds a bit for a screwdriver and allows you to scan the MK42 heatbed with the P.I.N.D.A sensor. This way, you can level the bed for non-magnetic or off-magnet print surfaces.

The advantage of using this accessory is that you can perform a finer mesh bed leveling with a 7x7 grid or any arbitrary resolution. This can improve the first layer quality and adhesion on uneven or warped beds. Moreover, since the shape of the MK42 heatbed depends only on the temperature and is consistent between prints, you don’t need to scan the bed every time you change the print surface, as long as you use the same temperature. You can also save different presets of the bed mesh for different temperatures and recall them when needed.

However, to scan a print surface that is outside of the magnet points, you need to use a custom firmware such as Klipper. Klipper is an alternative firmware that runs on a Raspberry Pi and communicates with the printer’s board via USB. It offers more flexibility and features than the stock Prusa firmware, such as pressure advance, input shaping, and custom g-code macros.

One of these macros is a module that corrects the tilt of the X-axis before each print. This is necessary because the position of the Z-axis motors is not preserved between prints when they are not powered. Therefore, if you use this accessory to scan a non-magnetic print surface, you need to run this module before printing to ensure a level bed.

The accessory is easy to use: just insert the bit into the tube and place it on the P.I.N.D.A sensor. The tube should protrude much more than the nozzle, so that it can reach the print surface without touching it. Then, run a custom g-code macro to perform a mesh bed leveling with your desired resolution. You can save the mesh in your configuration file for future prints (after removing the tube).

The accessory is also easy to print: it doesn’t require any supports or infill and it takes less than 10 minutes to print. You should use a filament that can withstand high temperatures and does not deform easily, such as PETG or ASA. These filaments are especially recommended if you use an enclosure for your printer.
