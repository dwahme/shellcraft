# Shellcraft
2D Minecraft in the terminal with programmable computer blocks 

Uncommon Hacks Hackathon 2020 Submission. See the Devpost project here: https://devpost.com/software/shellcraft. Awarded "Most Technically Impressive 2020"


## What it does

Essentially, this is a Terminal/Shell Video Game, heavily influenced by Minecraft/Terraria. This is implemented completely in the terminal, and supports programmable computer blocks which allow running arbitrary programs and IO interfacing with other computer blocks. You can build networks of computers in the game!

### Features:
- **Programmable computer block** 
  - __Arbitrary__ language supported blocks, programmable with __any__ terminal-based text editor in game, capable of receiving and transmitting IO via local __ports__, __sockets__, and __threads__
  - Computer blocks are able to detect IO on ports based upon wiring in the game. Configured through applying BFS on a network tree
  - Adjacent monitors combine to one giant monitor that supports any resolution, displays text output sent via signals from computer blocks

 - **2D-Minecraft Creative mode** 
   - Map exploration, block placement, block deletion, player movement, character inventory etc.
 - **Cool Inter-block Interactions**
   - Chain-able TNT, Fluid dynamics, Water-lava obsidian generation, Optional player gravity

- **Game Engine**
   - **Renders** the game, **transfer IO**, **manages block resources**, **physics engine**
   - **Seeded terrain generation generation using various statistical methods** 
        - Caves, Lakes, Mountains, Grass
   - **Dynamic terrain plant regeneration**
   
## Computers/Networks/IO
- **Computer Blocks**
  - Runs a command or program in a separate process
  - Supports piping stdin and stdout to and from the computer via the Computer class
  - Has a sentinel thread in the game which queues up its outputs on its ports
  - Has 4 IO ports- one on each side

- **Pi Blocks**
  - A specialized computer block which broadcasts and recieves on all sides through the same port
  - Useful for handling programs that don't follow the networking interface
    - Try running `telnet towel.blinkenlights.nl` as the runtime!
  
- **Wires**
  - Automatically detects and updates networks of computers and monitors
  - Broadcasts data across the network
  - Handles cycles and updates in real time (uses BFS for network detection)
  
- **Monitors**
  - Display data that is sent to them from any side
  - Automatically joins together with adjacent monitor blocks to form a larger monitor screen (updates in real time)
  - Uses BFS for joining monitor blocks


## The Team 
- [Dawson Whitehead](https://github.com/dwahme)
- [Yves Shum](https://github.com/yvesshum)
- [Johnny Hwang](https://github.com/johnnyihwang) 
- [Olivia Weng](https://github.com/oliviaweng)


## What's next for Shellcraft
- Saving/loading worlds
- Multiplayer 
- Advanced computing interfaces (More IO Devices)
- GUI (Terminal)
- Enemies
- Optimizing the game engine performance
- Survival Mode
- More blocks
- Revamping the controls (maybe allow using a mouse to interact with the world?)
- Revamping map-screen coordinate conversion
- Restructuring/generalizing how IO objects are handled
- Revamping how monitors display text (implement a micro shell?)
- Fixing bugs
- Miscellaneous code refactoring


## Interesting Technical Challenges
- Coordinate translation for rendering 
    - Converting map coordinates to screen coordinates and back 
    - Screen was centred around the player
    - Each block was 3 tall 5 wide for the desired aspect ratio 

- Seeded map generation 
    - Generating mountains 
        - Guiding a general convex shape generation with mountains 
        - Fine tuning parameters 

- Network ecosystem
     - Merging adjacent monitor blocks into 1 large screen using BFS 
     - Transferring IO between connected devices 
     - Handling appropriate threads and sockets 
     - Defining a computer network

## To Run:
`python3 main.py` Runs the entire game with default settings

`python3 main.py -h` To view usage options 

## Controls:
```
WASD - Player movement 

Z - Toggle action Place 
X - Toggle action Break
C - Toggle action Interact 

IJKL - Action at a particular direction 

Inventory: 
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
