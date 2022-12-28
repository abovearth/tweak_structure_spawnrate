# tweak_structure_spawnrate
Python script that tweaks the spawnrate of modded minecraft structures.
The script does that for all mods in a folder.
The mods have to use the datapack system to place structures.

The script works by extracting all data/worldgen/structure_set folders from all mod jars in the modsfolder.
Then for every json it looks for the separation and spacing parameter.
It applies a modifier to that parameter.
It also does some checks on the new parameter in accordance with the minecraft wiki.
It then saves the json files in a datapack.

Drop that datapack in your world folder to enjoy the tweaked spawnrates of modded minecraft structures.

Improvements I can think of are:
Make clearer to the user what the inputs are.
Add logging.
Add parameter for datapack version.
Add datapack version based on mc version.

Optimizations I can think of are:
Don't extract everything. Only what's needed.

Comparison of 3 spawnrate tweakes on the Minecolonies Official pack, 1.19.2 mc, 43.1.47 Forge.

This image is the original map for the seed sub2wol.
![map no tweak 1](https://user-images.githubusercontent.com/12080496/209837826-92cd701d-3754-49b4-b971-8a6c4d2572aa.png)
This image is the tweaked map for the seed sub2wol. The spawnrate of structures has been halved.
![map tweak 0_5](https://user-images.githubusercontent.com/12080496/209837814-9e3b62ef-0117-4e82-9b7f-f5b05a4ec9d2.png)
This image is the tweaked map for the seed sub2wol. The spawnrate of structures was tweaked to 0.8.
![map tweak 0_8](https://user-images.githubusercontent.com/12080496/209837821-fac14ba6-c904-4a73-8323-9188ef310f6b.png)
