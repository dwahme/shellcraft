# Shellcraft
Minecraft in the Terminal with Computer Blocks

Essentially, this is a Terminal/Shell Video Game, heavily influenced by Minecraft/Terraria. This is implemented completely in the terminal, and supports programmable computer blocks which allow running arbitrary programs and IO interfacing with other computer blocks. You can create a network!


## What it does

Essentially, this is a Terminal/Shell Video Game, heavily influenced by Minecraft/Terraria. This is implemented completely in the terminal, and supports programmable computer blocks which allow running arbitrary programs and IO interfacing with other computer blocks. You can create a network!

### Features:
- **Programmable computer block** 
  - (__Arbitrary__ language supported blocks, programmable with __any__ text editor in game, capable of receiving and transmitting IO via local __ports__, __sockets__, and __threads__)
  - (Computer blocks are able to detect IO on ports based upon wiring in the game. Configured through applying BFS on a network tree)
  - (Adjacent monitors combine to one giant monitor that supports any resolution, displays text output sent via signals from computer blocks)

-  **2D-Minecraft Creative mode** 
  - (Map exploration, block placement, block deletion, player movement, character inventory etc.)
  - **Cool Inter-block Interactions**
    - (Chain-able TNT, Fluid dynamics, Water-lava obsidian generation, Optional player gravity)

- **Game Engine**
   - **Renders** the game, **transfer IO**, **manages block resources**, **physics engine**
   - **Seeded terrain generation using various statistical methods** 
        - (Caves, Lakes, Mountains, Grass) 
   - **Dynamic terrain plant regeneration**

## The Team 
- [Dawson Whitehead](https://github.com/dwahme)
- [Yves Shum](https://github.com/yvesshum)
- [Johnny Hwang](https://github.com/johnnyihwang) 
- [Olivia Weng](https://github.com/oliviaweng)


## What's next for Shellcraft
- Multiplayer 
- Advanced computing interfaces (More IO Devices)
- GUI (Terminal)
- Enemies
- Optimizing the game engine performance
- Survival Mode 


## To Run:
`python3 main.py` Should be able to handle everything 

`python3 main.py -h` To view more options 

## Controlls:
```
WASD - Player movement 

Z - Toggle action Place 
X - Toggle action Break
C - Toggle action Interact 

IJKL - Action at a particular direction 

Iventory: 
1 - DIRT
2 - COMP
3 - WIRE-LRTB
4 - STONE
5 - SAND 
6 - MONITORBASIC
7 - TNT
8 - PI 

Further bindings can be configured in player.py

```

## Enjoy!
