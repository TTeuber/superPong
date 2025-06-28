#!/usr/bin/env python3
"""
4-Player Neon Pong Game
A retro-style Pong game with 4 players, neon visuals, and AI opponents.

Controls:
- Player 1 (Left, Blue): W/S keys
- Player 2 (Right, Pink): Arrow Up/Down keys
- Player 3 (Top, Green): J/L keys
- Player 4 (Bottom, Yellow): Numpad 4/6 keys

Press R to reset the game
Press ESC to quit
"""

import sys
import os

# Add the project directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game import Game

def main():
    """Main entry point"""
    print("Starting 4-Player Neon Pong...")
    print("Controls:")
    print("  Player 1 (Left, Blue): Nintendo Switch Controller or W/S keys")
    print("    - Left analog stick or D-pad for movement")
    print("    - Keyboard fallback: W (up) / S (down)")
    print("  Player 2 (Right, Pink): AI")
    print("  Player 3 (Top, Green): AI") 
    print("  Player 4 (Bottom, Yellow): AI")
    print("  Press R to reset, ESC to quit")
    print()

    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Thanks for playing!")

if __name__ == "__main__":
    main()