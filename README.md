A simple program to patch and run PMD Sky ROM hacks, mostly made for personal reasons. Targets Linux installs out of the box as it uses the `mv` command for drag and drop.

Current Features:
 - Auto-detecting drag and drop
   - Can drag .nds and .xdelta files
   - Base ROMs will automatically be loaded
 - Auto-patch and launch hacks using MelonDS
 - Will prioritize showing .nds files over .xdelta files if both are found with the same name
 - Ability to choose region on patch


Requirements:
 - Python with tkinter support
 - tkinterdnd2
 - melonDS in PATH
 - xdelta3 in PATH
 - Clean ROM(s) of US/EU version of PMD2