# Farming Puzzle Game (Unfinished)

A turn-based farming puzzle game built with `pygame`, where players plant, grow, and harvest crops while protecting them from crows. The game requires strategic planning to maximize crop yield and manage resources.

## Features

- **Dynamic Crop Management**: Plant and grow various crops like carrots and blueberries with unique growth stages and animations.
- **NPC Pathfinding**: Crows are programmed to seek out and attempt to reach mature crops, adding an interactive challenge.
- **Inventory and Hotbar System**: Track seeds, harvested crops, and select items easily using a hotbar with visual indicators.
- **Sprite Animations and Indicators**: Clear visuals for crop states, selected actions, and player interactions, enhancing the gameplay experience.

## Getting Started

### Prerequisites

- Python 3.7+
- Pygame (`pip install pygame`)

### Installation

1. **Clone the repository**.
2. **Install dependencies**:
    ```bash
    pip install pygame
    ```
## **Running the Game**

To start the game, run:

```bash
python FarmingGame.py
```

## **Gameplay**
- **Movement**: Use `W`, `A`, `S`, and `D` keys to move the player.
- **Planting**: Approach a dirt tile adjacent to your player and `left-click` to plant a seed.
- **Harvesting**: When crops are fully grown, `left-click` on the mature crop to collect it.

## **Controls**
`W`, `A`, `S`, `D` - Move player
`Mouse scroll` - Cycle through hotbar items
`Left-click` - Plant or harvest crops

## **Configuration**
Adjust game settings like resolution, crop indicators, and tile size directly in the `FarmingGame.py` file.