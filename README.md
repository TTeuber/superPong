# 4-Player Neon Pong

A retro-style Pong game featuring 4 players, neon visual effects, power-ups, and obstacles. Built with Python and Pygame.

## 🎮 Game Features

- **4-Player Gameplay**: Paddles on all four sides (left, right, top, bottom)
- **Retro Neon Aesthetic**: Glowing paddles, ball trails, and grid backgrounds
- **AI Opponents**: Smart AI with different difficulty levels
- **Power-ups** (planned): Paddle size modifiers, multi-ball, speed boosts
- **Obstacles** (planned): Bouncy barriers in the center area
- **Smooth Physics**: Realistic ball bouncing with spin effects

## 🕹️ Controls

- **Player 1 (Left, Blue)**: W/S keys
- **Player 2 (Right, Pink)**: Arrow Up/Down keys (AI by default)
- **Player 3 (Top, Green)**: J/L keys (AI by default)
- **Player 4 (Bottom, Yellow)**: Numpad 4/6 keys (AI by default)

### Special Keys
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
pong_game/
├── main.py              # Entry point and game initialization
├── game.py              # Main Game class and game loop
├── entities/
│   ├── paddle.py        # Paddle class with movement logic
│   ├── ball.py          # Ball physics and collision detection
│   ├── powerup.py       # Power-up system (planned)
│   └── obstacle.py      # Obstacle entities (planned)
├── systems/
│   ├── renderer.py      # All rendering logic with neon effects
│   ├── input_handler.py # Input management system
│   └── ai.py           # AI player logic
└── utils/
    ├── constants.py     # Game constants and color definitions
    └── math_utils.py    # Vector math and collision helpers
```

## 🎯 Current Status

### ✅ Phase 1 Complete: Core Foundation
- 4-player paddle setup with proper positioning
- Ball physics with realistic collision detection
- Input handling for human players
- AI opponents with different difficulty levels
- Basic scoring system
- Neon visual effects and rendering
- Game loop with 60 FPS performance

### 🚧 Phase 2 Planned: Enhanced Visuals
- Improved particle effects
- Better glow and lighting effects
- Animated backgrounds
- Enhanced UI elements

### 🚧 Phase 3 Planned: Power-ups System
- Paddle size modifiers (grow/shrink)
- Multi-ball power-up
- Speed boost/slow effects
- Timed power-up duration system
- Visual pickup effects

### 🚧 Phase 4 Planned: Obstacles & Polish
- Bouncy obstacles in center area
- Sound effects
- Improved AI behavior
- Game modes and settings

## 🎨 Technical Details

### Architecture
- **Component-based design**: Clean separation of concerns
- **Entity system**: Modular game objects
- **Event-driven input**: Responsive controls
- **Vector-based physics**: Smooth movement and collisions

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
- **Difficulty scaling**: Different precision levels per AI player
- **Movement smoothing**: Natural-feeling paddle movement

## 🔧 Configuration

Key settings can be modified in `utils/constants.py`:
- Screen dimensions
- Paddle sizes and speeds
- Ball physics parameters
- Color scheme
- AI difficulty levels

## 🐛 Known Issues

- Ball can occasionally get stuck in corners (rare)
- AI players don't account for power-ups yet
- No sound effects implemented

## 🤝 Contributing

This is a demo project, but feel free to:
- Add new power-ups
- Implement sound effects
- Create new AI behaviors
- Enhance visual effects
- Add game modes

## 📄 License

This project is for educational and demonstration purposes.