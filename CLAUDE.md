# CLAUDE.md - Development Context

This document provides essential context for continuing development of the 4-Player Neon Pong game.

## 🎯 Project Vision

We're building "the coolest Pong game ever" with these key features:
- **4-player simultaneous gameplay** (paddles on all four sides)
- **Retro neon aesthetic** with lots of colors and glowing effects
- **Power-ups system** with paddle modifiers and multi-ball
- **Obstacles** that the ball can bounce off of
- **1-4 human players** with AI filling remaining slots
- **Quick development** - designed to make good progress in under an hour

## 📋 Development Phases

### ✅ Phase 1: Core Foundation (COMPLETED)
**Duration**: 15-20 minutes  
**Status**: ✅ DONE

**Implemented**:
- Component-based architecture with clean file separation
- 4-paddle setup (left/right vertical, top/bottom horizontal)
- Ball physics with realistic collision detection and spin
- Input handling system for human players
- AI opponents with configurable difficulty
- Neon visual rendering with glow effects
- Basic scoring system
- 60 FPS game loop

**Files Created**:
- `main.py` - Entry point
- `game.py` - Main game class and loop
- `entities/paddle.py` - Paddle movement and collision
- `entities/ball.py` - Ball physics and bouncing
- `systems/renderer.py` - Neon visual effects
- `systems/input_handler.py` - Keyboard input
- `systems/ai.py` - AI player logic
- `utils/constants.py` - Game configuration
- `utils/math_utils.py` - Vector math utilities

### 🚧 Phase 2: Visual Polish (NEXT)
**Duration**: 10-15 minutes  
**Priority**: Medium

**Planned Features**:
- Enhanced particle effects for ball impacts
- Improved glow and lighting effects
- Animated neon grid background
- Better trail effects for ball movement
- Enhanced UI elements and typography
- Screen shake effects on paddle hits

### 🚧 Phase 3: Power-ups System (HIGH PRIORITY)
**Duration**: 15-20 minutes  
**Priority**: High

**Planned Power-ups**:
- **Paddle Size Modifiers**: Make enemy paddles smaller, make your paddle longer
- **Multi-ball**: Spawn additional balls
- **Speed Effects**: Speed boost/slow for ball or paddles
- Visual pickup effects with neon styling
- Timed duration system for power-ups
- Spawn locations and collection mechanics

**Implementation Notes**:
- Create `entities/powerup.py` class
- Add power-up spawning logic to game loop
- Implement visual pickup effects in renderer
- Add power-up collision detection
- Create timer system for effect duration

### 🚧 Phase 4: Obstacles & Polish (FINAL)
**Duration**: 5-10 minutes  
**Priority**: Low

**Planned Features**:
- Bouncy obstacle barriers in center area
- Sound effects for collisions and power-ups
- Improved AI that accounts for obstacles and power-ups
- Win conditions and game reset improvements

## 🏗️ Architecture Details

### Design Pattern
The project uses a **component-based architecture** with clear separation:
- **Entities**: Game objects (Paddle, Ball, PowerUp, Obstacle)
- **Systems**: Game logic (Renderer, InputHandler, AI)
- **Utils**: Shared utilities (Constants, Math)

### Key Classes and Responsibilities

**Game Class** (`game.py`):
- Main game loop and state management
- Entity coordination and updates
- Event handling and game flow
- Scoring and win condition logic

**Paddle Class** (`entities/paddle.py`):
- Position and movement logic
- Vertical (left/right) vs horizontal (top/bottom) orientation
- Collision rectangle management
- Player input integration

**Ball Class** (`entities/ball.py`):
- Physics simulation with velocity vectors
- Wall and paddle collision detection
- Realistic bouncing with spin effects based on hit position
- Trail effect system for visual appeal

**GameRenderer Class** (`systems/renderer.py`):
- All visual rendering with neon effects
- Glow effects using alpha blending
- Background grid and boundary drawing
- Score display and UI elements

**InputHandler Class** (`systems/input_handler.py`):
- Keyboard input processing
- Player control mapping
- Event handling integration

**AIPlayer Class** (`systems/ai.py`):
- Ball tracking logic with configurable difficulty
- Reaction delays to make AI beatable
- Movement decision making

### Technical Decisions Made

1. **Pygame Choice**: Selected for 2D graphics and rapid prototyping
2. **Vector Physics**: Using custom Vector2 class for smooth ball movement
3. **Component Separation**: Each system handles one responsibility
4. **Color-coded Players**: NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW
5. **60 FPS Target**: Optimized for smooth gameplay on M3 MacBook Pro
6. **No External Dependencies**: Only Pygame required

## 🎨 Visual Design Guidelines

### Color Palette
```python
NEON_BLUE = (0, 255, 255)      # Player 1 (Left)
NEON_PINK = (255, 20, 147)     # Player 2 (Right)  
NEON_GREEN = (57, 255, 20)     # Player 3 (Top)
NEON_YELLOW = (255, 255, 0)    # Player 4 (Bottom)
NEON_PURPLE = (191, 0, 255)    # For power-ups
NEON_ORANGE = (255, 165, 0)    # For obstacles
```

### Visual Effects Standards
- **Glow effects**: Use alpha blending with larger transparent shapes
- **Trail effects**: Store position history and fade with alpha
- **Grid background**: Subtle dark cyan lines with bright center lines
- **Particle effects**: Small, short-lived colored dots for impacts

## 🚀 Development Priorities

### Immediate Next Steps (Phase 3)
1. **Create PowerUp entity class** with spawn/collection mechanics
2. **Implement paddle size power-up** (most requested feature)
3. **Add multi-ball power-up** for chaos factor
4. **Create power-up visual effects** with neon styling
5. **Integrate power-up spawning** into game loop

### Code Quality Standards
- **Clean separation**: Each file has a single responsibility
- **Consistent naming**: snake_case for functions/variables
- **Type safety**: Use proper collision detection with pygame.Rect
- **Performance**: Avoid object creation in game loop
- **Readability**: Clear variable names and comments

## 🎮 Gameplay Balance

### Current AI Difficulty Settings
- Player 2 (Right): 0.7 difficulty (hardest)
- Player 3 (Top): 0.6 difficulty
- Player 4 (Bottom): 0.6 difficulty

### Ball Physics Parameters
- Base speed: 6 pixels/frame
- Spin factor: 0.7 (affects angle change on paddle hits)
- Minimum speeds: 2 pixels/frame in each direction (prevents getting stuck)

### Power-up Balance Suggestions
- **Paddle size change**: 50% size reduction for enemies, 150% for player
- **Multi-ball duration**: 10-15 seconds
- **Power-up spawn rate**: Every 15-30 seconds
- **Effect duration**: 8-12 seconds for temporary effects

## 🔧 Technical Notes

### Performance Considerations
- Game runs at 60 FPS on M3 MacBook Pro
- Uses pygame.sprite groups for efficient collision detection
- Minimal object allocation during gameplay
- Optimized rendering with dirty rectangle updates

### Collision System
- Uses pygame.Rect for all collision detection
- Ball-paddle collisions calculate relative hit position for spin
- Wall bouncing with boundary thickness consideration
- Power-up collection uses simple rect overlap

### File Organization
- Keep entities in `entities/` folder
- Keep systems in `systems/` folder
- Keep utilities in `utils/` folder
- Main game logic in root level files

## 🐛 Known Issues to Address

1. **Ball corner sticking**: Rare issue where ball gets stuck in corners
2. **AI prediction**: AI doesn't anticipate ball trajectory, only current position
3. **Power-up balance**: Need playtesting to fine-tune effects
4. **Visual polish**: Some glow effects could be more dramatic

## 💡 Future Enhancement Ideas

- **Network multiplayer**: Online 4-player support
- **Custom paddle shapes**: Different paddle designs
- **Environmental effects**: Moving backgrounds, screen shake
- **Sound system**: Impact sounds, background music
- **Replay system**: Save and replay epic matches
- **Tournament mode**: Bracket-style competitions