# CLAUDE.md - Development Context

This document provides essential context for continuing development of the 4-Player Neon Pong game.

## 🎯 Project Overview
w
A complete 4-player Pong game with these core features:
- **1-4 player multiplayer** with AI filling remaining slots
- **Multi-controller support** (up to 4 Nintendo Switch controllers)
- **Resizable window** with dynamic scaling and aspect ratio preservation
- **Retro neon aesthetic** with glow effects and particle systems
- **Configurable AI difficulty** (Easy, Medium, Hard)
- **Complete UI system** with settings, menus, and multiplayer setup
- **Power-ups system** (paddle size, shield, decoy ball - optional toggle)

## 🏗️ Architecture

### Design Pattern
**Component-based architecture** with clear separation:
- **Entities**: Game objects (Paddle, Ball, PowerUp)
- **Systems**: Specialized managers (GameState, Menu, Input, AI, Rendering, etc.)
- **UI**: Dedicated rendering for menus and screens
- **Utils**: Shared utilities (Constants, Math)

### Core Systems

**Game Class** (`game.py`):
- Main game loop coordination and system orchestration
- State management and event handling

**Key Systems**:
- **GameStateManager**: Handles transitions between start screen, playing, paused, game over, etc.
- **PlayerManager**: Tracks lives, elimination, human vs AI configuration
- **InputHandler**: Multi-controller support with keyboard fallback
- **AimingSystem**: Manual aiming for human players after losing a point
- **CollisionSystem**: Ball-paddle and boundary collision handling
- **Settings**: JSON persistence with real-time application

**Rendering Architecture**:
- **renderer.py**: Main coordinator (~50 lines)
- **game_renderer.py**: Core game elements (paddles, ball, boundaries)
- **effects_renderer.py**: Screen shake, glow effects, particles
- **ui/menu_renderer.py**: All screen and menu rendering
- **ui/ui_effects.py**: Font management and UI utilities

### Multiplayer System

**Player Count Flow**:
1. Start Screen → Player Count Selection (2-4 players)
2. Controller Setup → Automatic assignment + ready confirmation
3. Game starts with assigned human players + AI for remaining slots

**Input Handling**:
- **Multi-controller support**: Up to 4 controllers with hot-plug detection
- **Player-controller assignment**: Dynamic mapping stored in InputHandler
- **Human vs AI distinction**: PlayerManager tracks configuration
- **Keyboard fallback**: Each player has dedicated keys (WASD, arrows, IJKL, numpad)

## 🎨 Visual Design

### Color Palette
```python
NEON_BLUE = (0, 255, 255)      # Player 1 (Left)
NEON_PINK = (255, 20, 147)     # Player 2 (Right)  
NEON_GREEN = (57, 255, 20)     # Player 3 (Top)
NEON_YELLOW = (255, 255, 0)    # Player 4 (Bottom)
NEON_PURPLE = (191, 0, 255)    # Power-ups
```

### Visual Effects
- **Glow effects**: Multi-layer alpha blending for all neon elements
- **Particle system**: Impact bursts, elimination effects, victory celebrations
- **Screen shake**: Dynamic intensity based on collision type
- **Ball trails**: Position history with fade-out alpha
- **Animated grid background**: Pulsing with intersection highlights

## 🤖 AI System

**Difficulty Levels** (configurable in settings):
- **Easy (0.1)**: No prediction/strategy, 20-frame delays, 70% speed, 60% accuracy
- **Medium (0.3)**: Limited prediction, 12-frame delays, 85% speed, 80% accuracy  
- **Hard (0.6)**: Full AI capabilities, 4-frame delays, 100% speed, 100% accuracy

**AI Features**:
- Ball trajectory prediction with wall bounce calculation
- Strategic positioning and center-seeking behavior
- Smooth movement with hysteresis to feel natural
- Auto-aiming during aiming phase with smooth angle transitions

## 🎮 Controls & Input

### Player Assignments
- **Player 1 (Left)**: Controller 0 or WASD keys
- **Player 2 (Right)**: Controller 1 or Arrow keys
- **Player 3 (Top)**: Controller 2 or JL keys
- **Player 4 (Bottom)**: Controller 3 or Numpad 4/6

### Input System Features
- **Nintendo Switch controller support** with hot-plug detection
- **Triple input support**: Controller + keyboard + mouse for menus
- **Single-press detection**: Prevents rapid menu navigation and double-triggering
- **Pause handling**: Proper separation of pause vs menu actions

## 📏 Resizable Window System

### Dynamic Scaling Architecture
- **Base Reference Size**: 850x850px for all game design calculations
- **Monitor-Relative Scaling**: Window size calculated as percentage of available screen space
- **Square Aspect Ratio**: Always maintained regardless of screen size
- **Real-time Scaling**: All game elements (UI, entities, positions) scale dynamically

### Scaling Implementation
- **Scale Factor Calculation**: `SCALE_FACTOR = min(width, height) / 850`
- **Universal Application**: Applied to fonts, sprites, positions, speeds, and collision boxes
- **Settings Integration**: Scale setting (50%-150%) persisted in settings.json
- **Manual Window Resize**: Drag window corners to resize, settings automatically update

### Technical Details
- **Import Architecture**: Uses `from utils import constants` to avoid import caching issues
- **Entity Scaling**: All entities have `recreate_with_scale()` methods for dynamic updates
- **UI Font Scaling**: Font sizes recalculated and recreated on scale changes
- **Collision System**: All hitboxes and physics calculations scale-aware

## ⚙️ Configuration

### Settings (settings.json)
- `ai_difficulty`: 0.1 (Easy), 0.3 (Medium), 0.6 (Hard)
- `controller_sensitivity`: Analog stick sensitivity
- `sound_enabled`: For future sound implementation
- `powerups_enabled`: Toggle power-up system on/off
- `screen_scale`: Window size as percentage of monitor (0.5-1.5, default 0.75)

### Key Constants (utils/constants.py)
- Base screen dimensions: 850x850 (reference size for scaling)
- Dynamic screen scaling with `SCALE_FACTOR` applied to all elements
- Window size range: 600-1600px with square aspect ratio maintained
- Paddle speeds and sizes (scale-aware)
- Ball physics parameters (speed, spin factor)
- Controller settings (deadzone, button mappings)
- Game states and timing values

## 🔧 File Structure

```
superPong/
├── main.py                           # Entry point
├── game.py                           # Main game coordination
├── settings.json                     # Persistent settings
├── entities/
│   ├── paddle.py                     # Paddle with size modifiers
│   ├── ball.py                       # Ball physics with trails
│   └── powerup.py                    # Power-up entities
├── systems/
│   ├── game_state_manager.py         # State transitions
│   ├── player_count_system.py        # Player selection screen
│   ├── controller_setup_system.py    # Controller assignment
│   ├── input_handler.py              # Multi-controller input
│   ├── player_manager.py             # Human/AI coordination
│   ├── aiming_system.py              # Manual aiming phase
│   ├── collision_system.py           # Physics and collisions
│   ├── ai.py                         # AI behavior
│   ├── renderer.py                   # Rendering coordinator
│   ├── game_renderer.py              # Game element rendering
│   ├── effects_renderer.py           # Visual effects
│   ├── particle_system.py            # Particle effects
│   ├── powerup_system.py             # Power-up logic
│   └── powerup_renderer.py           # Power-up visuals
├── ui/
│   ├── menu_renderer.py              # Screen/menu rendering
│   └── ui_effects.py                 # UI utilities
└── utils/
    ├── constants.py                  # Game configuration
    └── math_utils.py                 # Vector utilities
```

## 🎯 Current State

The game is **feature-complete** with:
- ✅ Full multiplayer support (1-4 players)
- ✅ Complete controller system with assignment
- ✅ Resizable window with dynamic scaling system
- ✅ All game modes and screens functional
- ✅ Settings system with persistence
- ✅ AI opponents with difficulty scaling
- ✅ Power-up system (optional)
- ✅ Visual effects and neon styling
- ✅ Mouse, keyboard, and controller input

## 🐛 Known Issues

1. **Ball corner sticking**: Rare physics edge case
2. **Visual polish**: Some effects could be more dramatic
3. **No sound system**: Audio not implemented

## 🔨 Development Notes

### Testing
- Use `tests/controller_button_tester.py` to debug controller inputs
- Test all player counts (1-4) and controller combinations
- Verify settings persistence and real-time application

### Common Tasks
- **Add new visual effects**: Extend `effects_renderer.py` or `particle_system.py`
- **Modify AI behavior**: Update `ai.py` difficulty parameters
- **Change game balance**: Adjust constants in `utils/constants.py`
- **Add new settings**: Update `settings_system.py` and UI screens

### Performance
- Game runs at 60 FPS on M3 MacBook Pro
- Optimized collision detection using pygame rects
- Minimal object allocation during gameplay

### Code Style
- Snake_case for functions and variables
- Clear component separation with single responsibility
- No comments added unless requested
- Follow existing patterns when adding features