# 4-Player Neon Pong

A retro-style Pong game featuring 4 players, neon visual effects, Nintendo Switch controller support, and a scalable architecture. Built with Python and Pygame.

## 🎮 Game Features

- **1-4 Player Multiplayer**: Support for 1-4 human players with AI filling remaining slots
- **Multi-Controller Support**: Up to 4 Nintendo Switch controllers with automatic assignment
- **Resizable Window**: Dynamic scaling system with monitor-relative sizing (50%-150%)
- **Player Count Selection**: Choose 2-4 player games with controller setup screen
- **Retro Neon Aesthetic**: Glowing paddles, ball trails, and grid backgrounds
- **AI Opponents**: Smart AI with configurable difficulty levels (Easy, Medium, Hard)
- **Settings System**: Persistent JSON settings with in-game menu
- **Triple Input Support**: Controller, keyboard, and mouse support for all players
- **Start Screen**: Main menu with Play and Settings options
- **Pause Menu**: In-game pause with Resume, Restart, Main Menu, and Quit options
- **Power-ups**: Simplified system with paddle size, shield, and decoy ball (toggle on/off)
- **Obstacles** (planned): Bouncy barriers in the center area
- **Smooth Physics**: Realistic ball bouncing with spin effects

## 🕹️ Controls

### Multiplayer Controls (2-4 Players)
- **Player 1 (Left, Blue)**: Nintendo Switch Controller or W/S keys
- **Player 2 (Right, Pink)**: Nintendo Switch Controller or Arrow keys
- **Player 3 (Top, Green)**: Nintendo Switch Controller or J/L keys
- **Player 4 (Bottom, Yellow)**: Nintendo Switch Controller or Numpad 4/6 keys
- **AI fills remaining slots**: Unused player positions become AI opponents

### Controller Support
- **Nintendo Switch Controllers**: Left analog stick or D-pad for movement
- **Hot-plug Detection**: Controllers can be connected/disconnected during gameplay
- **Automatic Assignment**: Controllers automatically assigned to players during setup
- **Ready System**: Players press A button to confirm readiness before game starts

### Game Controls
- **Start Screen**: Navigate with analog stick/arrow keys, select with A/ENTER, or use mouse hover/click
- **Settings Menu**: Navigate with analog stick/arrow keys, change values with left/right, back with B/ESC, or use mouse hover/click on arrows
- **Pause Menu**: Navigate with analog stick/arrow keys, confirm with A/ENTER, cancel with B/ESC, or use mouse hover/click
- **Game Over Screen**: Navigate with analog stick/arrow keys, select with A/ENTER, or use mouse hover/click
- **Window Resize**: Drag window corners to resize, scale automatically saved to settings
- **R**: Reset game
- **ESC**: Pause game (no longer quits)

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
├── settings.json                     # Persistent game settings
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
│   ├── player_count_system.py        # Player count selection screen
│   ├── controller_setup_system.py    # Controller assignment and ready tracking
│   ├── aiming_system.py              # Aiming mode and ball launching
│   ├── collision_system.py           # Collision detection and handling
│   ├── player_manager.py             # Lives, elimination, AI coordination
│   ├── renderer.py                   # Main rendering coordinator (~50 lines)
│   ├── game_renderer.py              # Core game element rendering
│   ├── effects_renderer.py           # Screen shake and visual effects
│   ├── input_handler.py              # Multi-controller and keyboard input
│   ├── ai.py                         # AI player logic with difficulty scaling
│   └── particle_system.py            # Visual effect particles
├── ui/
│   ├── menu_renderer.py              # Screen and menu rendering
│   └── ui_effects.py                 # Font management and UI utilities
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
- Triple input system (controller + keyboard + mouse)
- AI opponents with configurable difficulty levels
- Lives system with player elimination
- Aiming mode for ball launching after life loss
- Start screen with main menu navigation
- Settings system with JSON persistence
- Pause menu with navigation (Resume/Restart/Main Menu/Quit)
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

### ✅ Phase 2.6 Complete: Renderer Refactoring
- **Modular rendering architecture**: Split monolithic renderer (913 lines) into specialized components
- **UI separation**: Created dedicated `ui/` directory for menu and screen rendering
- **Effect isolation**: Extracted screen shake and visual effects into separate renderer
- **Improved maintainability**: Each renderer handles single responsibility (menus, game elements, effects)
- **Better testability**: Isolated rendering components for unit testing
- **Preserved functionality**: All existing visual effects and features maintained

### ✅ Phase 2.7 Complete: Mouse Support & Input System Improvements
- **Full mouse integration**: Complete mouse support for all menu systems (start, settings, pause, game over)
- **Interactive menus**: Hover highlighting and click selection for all menu options
- **Settings enhancement**: Mouse-clickable arrows for changing setting values
- **Powerup simplification**: Reduced from 9 types to 3 essential powerups (paddle size, shield, decoy ball)
- **Simple powerup toggle**: Replaced complex powerup selection with on/off toggle in settings
- **Critical bug fix**: Resolved escape key double-trigger that caused immediate pause/resume
- **Enhanced input handling**: Improved InputHandler with proper single-press detection and dual-purpose key management

### ✅ Phase 2.8 Complete: Multiplayer Controller Support
- **Complete multiplayer foundation**: Added full support for 2-4 player games with controller assignment
- **Player count selection**: New screen for choosing number of players with controller setup
- **Multi-controller input**: Enhanced InputHandler to support up to 4 controllers simultaneously
- **Player-controller assignment**: Dynamic assignment system with hot-plug support and ready confirmation
- **Human vs AI distinction**: Clear separation between human players and AI opponents in all game modes
- **Aiming system updates**: Support for manual aiming by any human player, not just Player 1
- **Input processing fixes**: All human players now receive proper controller/keyboard input during gameplay
- **Critical multiplayer bugs**: Fixed game auto-start, pause menu flashing, menu navigation speed, and Player 2+ input issues

### ✅ Phase 2.9 Complete: Resizable Window System
- **Dynamic scaling architecture**: All game elements scale proportionally with window size
- **Monitor-relative sizing**: Window size calculated as percentage of available screen space (50%-150%)
- **Square aspect ratio preservation**: Always maintains 1:1 ratio regardless of monitor size
- **Settings integration**: Screen scale persisted in settings.json with real-time updates
- **Manual window resize**: Drag window corners to resize, settings automatically update
- **Universal scaling**: Fonts, sprites, positions, speeds, and collision boxes all scale-aware
- **Import architecture fixes**: Resolved scaling import caching issues for consistent behavior

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
- **Modular rendering**: Specialized renderers for game elements, UI, and effects
- **Multi-input support**: Responsive controls with controller, keyboard, and mouse support
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

The AI players use an advanced multi-layer difficulty system:
- **Ball Prediction**: Trajectory prediction with wall bounce calculation
- **Strategic Positioning**: Center-seeking behavior and defensive positioning
- **Difficulty Scaling**: Three distinct difficulty levels with multiple parameters
  - **Easy (0.1)**: No prediction, no strategy, slow reactions (20 frames), 30% slower movement, 40% accuracy
  - **Medium (0.3)**: Limited prediction/strategy, moderate reactions (12 frames), 15% slower movement, 80% accuracy
  - **Hard (0.6)**: Full AI capabilities, fast reactions (4 frames), full speed, 100% accuracy
- **Movement Smoothing**: Natural-feeling paddle movement with hysteresis
- **Aiming Intelligence**: AI automatically aims with smooth angle transitions
- **Reaction Delays**: Variable delays based on difficulty to maintain fairness

## 🔧 Configuration

### In-Game Settings (settings.json)
- **AI Difficulty**: Easy, Medium, Hard levels with comprehensive AI behavior changes
- **Screen Scale**: Window size as percentage of monitor (50%-150%, default 75%)
- **Sound**: Enable/disable sound effects (when implemented)
- **Controller Sensitivity**: Analog stick sensitivity adjustment
- **Powerups**: Simple on/off toggle for powerup system (paddle size, shield, decoy ball)

### Developer Settings (utils/constants.py)
- Base screen dimensions (850x850 reference size)
- Dynamic scaling system with SCALE_FACTOR applied to all elements
- Window size constraints (600-1600px with square aspect ratio)
- Paddle sizes and speeds (scale-aware)
- Ball physics parameters
- Color scheme (neon theme)
- AI prediction and strategy parameters
- Controller settings (deadzone, sensitivity)
- Nintendo Switch controller button mappings
- Game state definitions and menu configurations

## 🐛 Known Issues

- Ball can occasionally get stuck in corners (rare)
- AI players don't account for power-ups or obstacles yet
- No sound effects implemented
- Visual polish could be enhanced with more dramatic effects

## ✅ Recently Fixed

- **Escape key double-trigger**: Fixed issue where pressing escape would pause and immediately resume the game
- **Mouse detection offset**: Resolved mouse hover detection being offset from visual button positions
- **Complex powerup system**: Simplified from 9 powerup types to 3 essential ones with cleaner interface
- **Game auto-starting**: Fixed input bleed-through causing game to bypass start menu
- **Pause menu flashing**: Resolved rapid pause/unpause cycles with proper input debouncing
- **Menu navigation speed**: Added single-press detection to prevent skipping menu options
- **Multiplayer controller support**: Fixed controller input only working for Player 1, now supports all players
- **Aiming mode for multiplayer**: Fixed Player 2+ getting AI auto-aiming instead of manual control
- **Scale calculation bug**: Fixed cumulative scaling issue where changes applied to current size instead of base monitor size
- **PowerUp AttributeErrors**: Fixed missing movement_timer and variant attributes causing game crashes during power-up collection

## 🤝 Contributing

This is a demo project, but feel free to:
- Add new power-ups
- Implement sound effects
- Create new AI behaviors
- Enhance visual effects
- Add game modes

## 📄 License

This project is for educational and demonstration purposes.