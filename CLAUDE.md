# CLAUDE.md - Development Context

This document provides essential context for continuing development of the 4-Player Neon Pong game.

## 🎯 Project Vision

We're building "the coolest Pong game ever" with these key features:
- **4-player simultaneous gameplay** (paddles on all four sides)
- **Retro neon aesthetic** with lots of colors and glowing effects
- **Power-ups system** with paddle modifiers and multi-ball
- **Obstacles** that the ball can bounce off of
- **1-4 human players** with AI filling remaining slots

## 📋 Development Phases

### ✅ Phase 1: Core Foundation (COMPLETED)
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

### ✅ Phase 2: Visual Polish (COMPLETED)
**Status**: ✅ DONE

**Implemented Features**:
- **Enhanced particle effects**: Ball impact bursts, wall sparks, elimination effects, victory celebrations
- **Improved glow and lighting effects**: Multi-layer glow for paddles, balls, boundaries, and text
- **Animated neon grid background**: Pulsing grid with moving offset and intersection highlights
- **Better trail effects**: Enhanced ball trails with variable size and alpha blending
- **Enhanced UI elements**: Glowing pause menu with pulsing selection indicators
- **Screen shake effects**: Dynamic screen shake for paddle hits, eliminations, and collisions
- **Dynamic visual feedback**: Color-coded glow based on last paddle hit, dimmed visuals for eliminated players

### ✅ Phase 2.5: Settings & Difficulty System (COMPLETED)
**Status**: ✅ DONE

**Implemented Features**:
- **Settings System**: JSON persistence with `settings.json` file
- **Settings Screen**: Full UI with navigation and value changing
- **Start Screen**: Main menu with Play and Settings options
- **Difficulty System**: Three-tier AI difficulty with comprehensive behavior changes
  - **Easy (0.1)**: No prediction/strategy, 20-frame delays, 30% slower movement, 60% accuracy
  - **Medium (0.3)**: Limited AI features, 12-frame delays, 15% slower movement, 80% accuracy
  - **Hard (0.6)**: Full AI capabilities, 4-frame delays, full speed, 100% accuracy
- **AI Fixes**: Resolved speed degradation bug that caused AI to stop moving
- **Enhanced Menu System**: Neon-styled menus with controller and keyboard support

### ✅ Phase 2.6: Renderer Refactoring (COMPLETED)
**Status**: ✅ DONE

**Refactoring Goals Achieved**:
- **Reduced monolithic renderer**: Split 913-line renderer into specialized components
- **Created modular architecture**: Separated UI, game elements, and effects rendering
- **Improved maintainability**: Each renderer handles single responsibility
- **Enhanced testability**: Isolated components for unit testing
- **Preserved all functionality**: No breaking changes to existing features

**New Architecture**:
- **`ui/menu_renderer.py`**: All screen and menu rendering (start, game over, settings, pause)
- **`ui/ui_effects.py`**: Font management, background grid, and UI utilities
- **`systems/game_renderer.py`**: Core game elements (paddles, ball, trails, boundaries)
- **`systems/effects_renderer.py`**: Screen shake, glow effects, and visual impact systems
- **`systems/renderer.py`**: Main coordinator (~50 lines, down from 913)

### ✅ Phase 2.7: Mouse Support & Input System Improvements (COMPLETED)
**Status**: ✅ DONE

**Mouse Support Implementation**:
- **Full mouse support**: Added mouse hover and click detection for all menu systems
- **Hover highlighting**: Menu options highlight when mouse cursor hovers over them
- **Click selection**: Mouse clicks execute menu actions (Play, Settings, Resume, etc.)
- **Settings navigation**: Left/right arrow clicks for changing setting values
- **Coordinate precision**: Fixed mouse detection coordinates to match visual button positions

**Input System Enhancements**:
- **Mouse state tracking**: Added `mouse_pos`, `mouse_clicked`, `mouse_just_clicked` to InputHandler
- **Single-frame detection**: Proper mouse click detection prevents double-triggering
- **Point-in-rectangle utility**: Added `is_point_in_rect()` for accurate hit detection

**Powerup System Simplification**:
- **Reduced complexity**: Simplified from 9 powerup types to 3 essential ones (paddle size, shield, decoy ball)
- **Simple toggle**: Replaced complex powerup selection UI with on/off toggle in settings
- **Cleaner codebase**: Removed unused powerup selection rendering and logic

**Critical Bug Fix: Escape Key Double-Trigger**:
- **Root cause identified**: SPACE and ESCAPE serve dual purposes (pause + menu actions)
- **Solution implemented**: Added pause usage tracking flags (`escape_used_for_pause`, `space_used_for_pause`)
- **Proper lifecycle**: Flags persist until key release, preventing immediate menu processing
- **Clean separation**: Each keypress can only trigger ONE action (either pause OR menu)

### 🚧 Phase 3: Power-ups System (NEXT)
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
**Priority**: Low

**Planned Features**:
- Bouncy obstacle barriers in center area
- Sound effects for collisions and power-ups
- Improved AI that accounts for obstacles and power-ups
- Win conditions and game reset improvements

## 🏗️ Architecture Details

### Design Pattern
The project uses a **component-based architecture** with clear separation and single responsibility:
- **Entities**: Game objects (Paddle, Ball, PowerUp, Obstacle)
- **Systems**: Specialized game logic managers (State, Menu, Aiming, Collision, Player, Renderer, Input, AI, Particles)
- **Utils**: Shared utilities (Constants, Math)

### Refactored Architecture (June 2025)
The codebase was refactored to improve scalability and maintainability:
- **Reduced game.py from 514 lines to 227 lines** (>50% reduction)
- **Extracted specialized systems** for better separation of concerns
- **Improved testability** with isolated system responsibilities
- **Enhanced scalability** for adding new features

### Core Systems and Responsibilities

**Game Class** (`game.py`):
- Main game loop coordination (227 lines)
- System orchestration and callbacks
- High-level game flow management
- Event handling and input coordination

**GameStateManager** (`systems/game_state_manager.py`):
- Game state transitions (Start Screen, Settings, Playing, Aiming, Paused, Game Over)
- State validation and management
- Pause/resume functionality

**MenuSystem** (`systems/menu_system.py`):
- Pause menu navigation and selection
- Menu input handling with callback system
- Extensible for future menu systems

**SettingsSystem** (`systems/settings_system.py`):
- JSON file persistence for game settings
- Settings validation and default handling
- Auto-creation of settings.json with defaults

**SettingsScreenSystem** (`systems/settings_screen_system.py`):
- Settings menu UI and navigation
- Value changing with left/right input
- Real-time difficulty application to AI players

**AimingSystem** (`systems/aiming_system.py`):
- Player aiming mode coordination
- Angle calculations for all player positions
- AI auto-aiming with smooth animations
- Ball launching with physics integration

**CollisionSystem** (`systems/collision_system.py`):
- Ball-paddle collision detection
- Ball-boundary collision handling
- Collision response coordination with effects

**PlayerManager** (`systems/player_manager.py`):
- Lives tracking and player elimination
- Paddle initialization and management
- AI player coordination
- Game over detection and winner determination

**GameRenderer Class** (`systems/renderer.py`):
- Main rendering coordinator and orchestrator (~50 lines)
- Delegates to specialized renderers
- Manages frame counting and screen shake coordination
- Provides unified interface to game systems

**CoreGameRenderer Class** (`systems/game_renderer.py`):
- Core game element rendering (paddles, ball, boundaries)
- Ball trails and aiming system visualization
- Lives display and game state indicators
- Delegates effects to EffectsRenderer

**MenuRenderer Class** (`ui/menu_renderer.py`):
- All screen and menu rendering (start, settings, game over, pause)
- Menu navigation and selection highlighting
- Title animations and demo game display
- Uses UIEffects for common UI utilities

**UIEffects Class** (`ui/ui_effects.py`):
- Font management and loading
- Background grid rendering
- Common UI effects (glow, pulsing, arrows)
- Reusable text and instruction rendering

**EffectsRenderer Class** (`systems/effects_renderer.py`):
- Screen shake system and coordination
- Multi-layer glow effects for game elements
- Trail rendering and visual impact effects
- Reusable effect utilities

**InputHandler Class** (`systems/input_handler.py`):
- Keyboard, controller, and mouse input processing
- Nintendo Switch controller support with hot-plug detection
- Player control mapping and coordination
- Mouse hover and click detection for menu systems
- Single-press detection for escape/space keys to prevent double-triggering
- Pause usage tracking to prevent dual-purpose key conflicts

**AIPlayer Class** (`systems/ai.py`):
- Ball tracking logic with configurable difficulty
- Reaction delays to make AI beatable
- Movement decision making

**Entities:**
- **Paddle Class** (`entities/paddle.py`): Position, movement, collision rectangles
- **Ball Class** (`entities/ball.py`): Physics simulation, collision detection, trail effects

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
- **Easy (0.1)**: No prediction/strategy, 20-frame delays, 30% slower movement, 60% accuracy
- **Medium (0.3)**: Limited prediction/strategy, 12-frame delays, 15% slower movement, 80% accuracy  
- **Hard (0.6)**: Full AI capabilities, 4-frame delays, full speed, 100% accuracy
- All AI players (Right, Top, Bottom) use the same difficulty level from settings

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

### Settings System
- JSON persistence with `settings.json` file
- Automatic creation of defaults if file missing
- Real-time application of difficulty changes
- Validation of setting ranges and types

### AI Difficulty Implementation
- **Multi-layer difficulty system** with exponential scaling
- **Feature toggles**: Prediction and strategy disabled for Easy mode
- **Speed preservation**: Original paddle speed stored to prevent degradation
- **Accuracy modifiers**: Intentional errors injected for easier difficulties
- **Reaction scaling**: 20/12/4 frame delays for Easy/Medium/Hard

### File Organization
```
superPong/
├── main.py                           # Entry point
├── game.py                           # Main game coordination (227 lines)
├── settings.json                     # Persistent game settings (JSON)
├── CLAUDE.md                         # Development context and instructions
├── README.md                         # Project documentation
├── entities/
│   ├── paddle.py                     # Paddle movement and collision
│   ├── ball.py                       # Ball physics and bouncing
│   ├── obstacle.py                   # Obstacle entities (future)
│   └── powerup.py                    # Power-up entities (future)
├── systems/
│   ├── game_state_manager.py         # Game state transitions
│   ├── menu_system.py                # Menu navigation and callbacks
│   ├── settings_system.py            # Settings persistence and management
│   ├── settings_screen_system.py     # Settings UI and navigation
│   ├── aiming_system.py              # Aiming mode and ball launching
│   ├── collision_system.py           # Collision detection and handling
│   ├── player_manager.py             # Lives, elimination, AI coordination
│   ├── renderer.py                   # Main rendering coordinator (~50 lines)
│   ├── game_renderer.py              # Core game element rendering
│   ├── effects_renderer.py           # Screen shake and visual effects
│   ├── input_handler.py              # Keyboard and controller input
│   ├── ai.py                         # AI player logic with difficulty scaling
│   └── particle_system.py            # Visual effect particles
├── ui/
│   ├── menu_renderer.py              # Screen and menu rendering
│   └── ui_effects.py                 # Font management and UI utilities
├── utils/
│   ├── constants.py                  # Game configuration and difficulty values
│   └── math_utils.py                 # Vector math utilities
└── tests/
    └── controller_button_tester.py   # Controller testing utility
```

**Organization Principles:**
- **Single Responsibility**: Each file handles one specific concern
- **Modular Rendering**: UI, game elements, and effects separated into specialized renderers
- **Clear Dependencies**: Systems depend on entities and utils, renderers depend on effects
- **Extensible Design**: Easy to add new systems, entities, or rendering components
- **Testable Architecture**: Isolated systems and renderers for unit testing

## 🐛 Known Issues to Address

1. **Ball corner sticking**: Rare issue where ball gets stuck in corners
2. **Power-up balance**: Need playtesting to fine-tune effects (when implemented)
3. **Visual polish**: Some glow effects could be more dramatic
4. **Sound system**: No audio implementation yet

## ✅ Recently Fixed Issues

1. **Escape key double-trigger**: Fixed issue where pressing escape would pause and immediately resume the game
2. **Mouse detection offset**: Resolved mouse hover detection being offset from visual button positions
3. **AI speed degradation**: Fixed bug where AI players would gradually slow down and stop moving
4. **Powerup system complexity**: Simplified from 9 powerup types to 3 essential ones with cleaner UI

## 🎆 Recent Improvements (July 2025)

### Settings & Difficulty System Implementation
- **Complete settings infrastructure** with JSON persistence
- **Three-tier difficulty system** with comprehensive AI behavior changes
- **AI bug fixes**: Resolved speed degradation causing complete movement failure
- **Enhanced menu system** with neon styling and controller support
- **Real-time difficulty application** to existing AI players

### Renderer Architecture Refactoring
- **Massive code reduction**: Split monolithic 913-line renderer into focused components
- **New UI directory**: Dedicated `ui/` folder for menu and screen rendering
- **Specialized renderers**: Game elements, effects, and UI separated for maintainability
- **Preserved functionality**: All visual effects and features maintained during refactor
- **Improved scalability**: Much easier to add new rendering features or modify existing ones

### Mouse Support & Input System Overhaul
- **Full mouse integration**: Complete mouse support for all menu systems (start, settings, pause, game over)
- **Interactive menus**: Hover highlighting and click selection for all menu options
- **Settings enhancement**: Mouse-clickable arrows for changing setting values
- **Powerup simplification**: Reduced from 9 types to 3 essential powerups with simple toggle
- **Critical bug fix**: Resolved escape key double-trigger that caused immediate pause/resume
- **Input architecture**: Enhanced InputHandler with proper single-press detection and dual-purpose key handling

## 💡 Future Enhancement Ideas

- **Network multiplayer**: Online 4-player support
- **Custom paddle shapes**: Different paddle designs
- **Environmental effects**: Moving backgrounds, screen shake
- **Sound system**: Impact sounds, background music
- **Replay system**: Save and replay epic matches
- **Tournament mode**: Bracket-style competitions