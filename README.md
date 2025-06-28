# 4-Player Neon Pong

A retro-style Pong game featuring 4 players, neon visual effects, Nintendo Switch controller support, and a scalable architecture. Built with Python and Pygame.

## 🎮 Game Features

- **4-Player Gameplay**: Paddles on all four sides (left, right, top, bottom)
- **Retro Neon Aesthetic**: Glowing paddles, ball trails, and grid backgrounds
- **AI Opponents**: Smart AI with different difficulty levels
- **Power-ups** (planned): Paddle size modifiers, multi-ball, speed boosts
- **Obstacles** (planned): Bouncy barriers in the center area
- **Smooth Physics**: Realistic ball bouncing with spin effects

## 🕹️ Controls

### Player 1 (Left, Blue) - Human Player
- **Nintendo Switch Controller**: Left analog stick or D-pad for movement
- **Keyboard Fallback**: W (up) / S (down)
- **Pause**: START button or P/SPACE key

### AI Players
- **Player 2 (Right, Pink)**: AI controlled
- **Player 3 (Top, Green)**: AI controlled  
- **Player 4 (Bottom, Yellow)**: AI controlled

### Game Controls
- **Pause Menu**: Navigate with analog stick/arrow keys, confirm with A/ENTER, cancel with B/ESC
- **R**: Reset game
- **ESC**: Quit game

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Pygame library

### Installation
```bash
# Install Pygame
pip install pygame

# Clone/download the project
# Navigate to project directory

# Run the game
python main.py
```

## 🏗️ Project Structure

```
superPong/
├── main.py                           # Entry point
├── game.py                           # Main game coordination (227 lines)
├── entities/
│   ├── paddle.py                     # Paddle movement and collision
│   ├── ball.py                       # Ball physics and bouncing
│   ├── obstacle.py                   # Obstacle entities (future)
│   └── powerup.py                    # Power-up entities (future)
├── systems/
│   ├── game_state_manager.py         # Game state transitions
│   ├── menu_system.py                # Menu navigation and callbacks
│   ├── aiming_system.py              # Aiming mode and ball launching
│   ├── collision_system.py           # Collision detection and handling
│   ├── player_manager.py             # Lives, elimination, AI coordination
│   ├── renderer.py                   # Neon visual effects
│   ├── input_handler.py              # Keyboard and controller input
│   ├── ai.py                         # AI player logic
│   └── particle_system.py            # Visual effect particles
├── utils/
│   ├── constants.py                  # Game configuration
│   └── math_utils.py                 # Vector math utilities
└── tests/
    └── controller_button_tester.py   # Controller testing utility
```

## 🎯 Current Status

### ✅ Phase 1 Complete: Core Foundation
- 4-player paddle setup with proper positioning
- Ball physics with realistic collision detection
- Nintendo Switch USB controller support with hot-plug detection
- Dual input system (controller + keyboard)
- AI opponents with different difficulty levels
- Lives system with player elimination
- Aiming mode for ball launching after life loss
- Pause menu with navigation (Resume/Restart/Quit)
- Basic neon visual effects and rendering
- Game loop with 60 FPS performance
- **Refactored Architecture**: Reduced main game file from 514 to 227 lines

### ✅ Phase 2 Complete: Visual Polish
- **Enhanced particle effects**: Ball impact bursts, wall sparks, elimination effects, victory celebrations
- **Advanced glow system**: Multi-layer glow effects for paddles, balls, boundaries, and UI text
- **Animated neon grid background**: Pulsing grid with moving animations and intersection highlights
- **Improved ball trails**: Variable-size trails with proper alpha blending and glow effects
- **Dynamic screen shake**: Responsive screen shake for different impact types and intensities
- **Enhanced UI effects**: Glowing pause menu with pulsing selection indicators and smooth transitions
- **Visual feedback system**: Color-coded effects based on player interactions and game state

### 🚧 Phase 3 Next: Power-ups System
- Paddle size modifiers (grow/shrink)
- Multi-ball power-up with chaos effects
- Speed boost/slow effects for dynamic gameplay
- Visual pickup effects with neon styling
- Timed power-up duration system
- Strategic spawn locations

### 🚧 Phase 4 Planned: Obstacles & Polish
- Bouncy obstacles in center area
- Sound effects
- Improved AI behavior
- Game modes and settings

## 🎨 Technical Details

### Architecture
- **Component-based design**: Clean separation of concerns with specialized systems
- **Entity system**: Modular game objects (Paddle, Ball, PowerUp, Obstacle)
- **System managers**: GameState, Menu, Aiming, Collision, Player management
- **Event-driven input**: Responsive controls with controller and keyboard support
- **Vector-based physics**: Smooth movement and collisions
- **Scalable design**: Easy to add new features and systems

### Performance
- Optimized for 60 FPS gameplay
- Efficient collision detection using Pygame rects
- Minimal memory allocation during gameplay
- Designed for M3 MacBook Pro performance

### Visual Effects
- Real-time glow effects using alpha blending
- Ball trail system with fade-out
- Grid background with center line highlights
- Color-coded players with neon theme

## 🤖 AI System

The AI players use a simple but effective tracking system:
- **Target tracking**: AI paddles follow the ball position
- **Reaction delays**: Configurable delays make AI beatable
- **Difficulty scaling**: Different precision levels per AI player (0.6-0.7)
- **Movement smoothing**: Natural-feeling paddle movement
- **Aiming intelligence**: AI automatically aims with smooth angle transitions

## 🔧 Configuration

Key settings can be modified in `utils/constants.py`:
- Screen dimensions (850x850)
- Paddle sizes and speeds
- Ball physics parameters
- Color scheme (neon theme)
- AI difficulty levels
- Controller settings (deadzone, sensitivity)
- Nintendo Switch controller button mappings

## 🐛 Known Issues

- Ball can occasionally get stuck in corners (rare)
- AI players don't account for power-ups or obstacles yet
- No sound effects implemented
- Visual polish could be enhanced with more dramatic effects

## 🤝 Contributing

This is a demo project, but feel free to:
- Add new power-ups
- Implement sound effects
- Create new AI behaviors
- Enhance visual effects
- Add game modes

## 📄 License

This project is for educational and demonstration purposes.