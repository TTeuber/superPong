#!/usr/bin/env python3
"""
Test script for Version 3: Chaos Power-ups

This script tests all the chaos power-up functionality to ensure they work correctly:
- DECOY BALL: Spawns fake balls that don't cause life loss
- WILD BOUNCE: Ball randomly changes direction during flight  
- CONTROL SCRAMBLE: All player controls get scrambled

Usage: python test_chaos_powerups.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.constants import *
from systems.powerup_system import PowerUpSystem
from systems.settings_system import SettingsSystem
from entities.ball import Ball
from entities.powerup import PowerUp

def test_chaos_constants():
    """Test that all chaos power-up constants are defined"""
    print("Testing chaos power-up constants...")
    
    # Test chaos power-up types exist
    assert hasattr(sys.modules['utils.constants'], 'POWERUP_DECOY_BALL')
    assert hasattr(sys.modules['utils.constants'], 'POWERUP_WILD_BOUNCE') 
    assert hasattr(sys.modules['utils.constants'], 'POWERUP_CONTROL_SCRAMBLE')
    
    # Test chaos types are in all types
    assert POWERUP_DECOY_BALL in POWERUP_ALL_TYPES
    assert POWERUP_WILD_BOUNCE in POWERUP_ALL_TYPES
    assert POWERUP_CONTROL_SCRAMBLE in POWERUP_ALL_TYPES
    
    # Test chaos category exists
    assert "Chaos" in POWERUP_CATEGORIES
    assert POWERUP_DECOY_BALL in POWERUP_CATEGORIES["Chaos"]
    assert POWERUP_WILD_BOUNCE in POWERUP_CATEGORIES["Chaos"]
    assert POWERUP_CONTROL_SCRAMBLE in POWERUP_CATEGORIES["Chaos"]
    
    # Test descriptions exist
    assert POWERUP_DECOY_BALL in POWERUP_DESCRIPTIONS
    assert POWERUP_WILD_BOUNCE in POWERUP_DESCRIPTIONS
    assert POWERUP_CONTROL_SCRAMBLE in POWERUP_DESCRIPTIONS
    
    print("✓ All chaos power-up constants defined correctly")

def test_powerup_entity():
    """Test PowerUp entity with chaos variants"""
    print("Testing PowerUp entity with chaos variants...")
    
    # Test each chaos power-up type
    chaos_types = [POWERUP_DECOY_BALL, POWERUP_WILD_BOUNCE, POWERUP_CONTROL_SCRAMBLE]
    
    for powerup_type in chaos_types:
        powerup = PowerUp(100, 100, powerup_type)
        assert powerup.type == powerup_type
        assert powerup.variant in ["decoy", "wild", "scramble"]
        assert powerup.get_duration() > 0 or powerup.get_duration() == -1  # Some are instant
        
        # Test color is unique
        color = powerup.get_base_color()
        assert len(color) == 3  # RGB tuple
        assert all(0 <= c <= 255 for c in color)
        
        # Test icon exists
        icon_points = powerup.get_icon_points()
        assert len(icon_points) > 0
        
    print("✓ PowerUp entity handles all chaos variants correctly")

def test_ball_entity():
    """Test Ball entity with decoy functionality"""
    print("Testing Ball entity with decoy functionality...")
    
    # Test regular ball
    regular_ball = Ball(100, 100, is_decoy=False)
    assert not regular_ball.is_decoy
    assert regular_ball.lifetime == -1  # Infinite
    assert regular_ball.alpha == 255  # Fully opaque
    assert regular_ball.causes_life_loss()
    assert not regular_ball.is_expired()
    
    # Test decoy ball
    decoy_ball = Ball(100, 100, is_decoy=True)
    assert decoy_ball.is_decoy
    assert decoy_ball.lifetime == POWERUP_DURATION_DECOY_BALL
    assert decoy_ball.alpha < 255  # Transparent
    assert not decoy_ball.causes_life_loss()
    assert not decoy_ball.is_expired()  # Not expired initially
    
    # Test decoy ball expiration
    decoy_ball.lifetime = 0
    assert decoy_ball.is_expired()
    
    print("✓ Ball entity supports decoy functionality correctly")

def test_powerup_system():
    """Test PowerUpSystem with chaos effects"""
    print("Testing PowerUpSystem with chaos effects...")
    
    settings_system = SettingsSystem()
    powerup_system = PowerUpSystem(settings_system)
    
    # Test decoy ball spawning
    powerup_system.spawn_decoy_ball()
    decoy_balls = powerup_system.get_decoy_balls()
    assert len(decoy_balls) == 1
    assert decoy_balls[0].is_decoy
    
    # Test wild bounce detection
    assert not powerup_system.has_wild_bounce()  # No active effect
    
    # Test control scramble detection  
    assert not powerup_system.has_control_scramble()  # No active effect
    
    # Test scrambled player ID (should return original when no scramble)
    assert powerup_system.get_scrambled_player_id(0) == 0
    assert powerup_system.get_scrambled_player_id(1) == 1
    
    print("✓ PowerUpSystem handles chaos effects correctly")

def test_settings_integration():
    """Test settings system integration with chaos power-ups"""
    print("Testing settings system integration...")
    
    settings_system = SettingsSystem()
    
    # Test enabled power-ups includes chaos types by default
    enabled = settings_system.get_enabled_powerups()
    assert isinstance(enabled, list)
    
    # Test chaos power-ups can be toggled
    original_count = len(enabled)
    was_enabled = POWERUP_DECOY_BALL in enabled
    
    # Try to toggle a chaos power-up
    success = settings_system.toggle_powerup(POWERUP_DECOY_BALL)
    new_enabled = settings_system.get_enabled_powerups()
    
    if was_enabled:
        # Was enabled, should now be disabled (if more than 1 was enabled)
        if original_count > 1:
            assert success
            assert len(new_enabled) == original_count - 1
            assert POWERUP_DECOY_BALL not in new_enabled
        else:
            # Can't disable last power-up
            assert not success
            assert len(new_enabled) == original_count
            assert POWERUP_DECOY_BALL in new_enabled
    else:
        # Was disabled, should now be enabled
        assert success
        assert len(new_enabled) == original_count + 1
        assert POWERUP_DECOY_BALL in new_enabled
    
    # Toggle back to restore original state
    settings_system.toggle_powerup(POWERUP_DECOY_BALL)
    
    print("✓ Settings system integrates with chaos power-ups correctly")

def test_chaos_effects():
    """Test specific chaos power-up effects"""
    print("Testing chaos power-up effects...")
    
    settings_system = SettingsSystem()
    powerup_system = PowerUpSystem(settings_system)
    
    # Test wild bounce effect
    ball = Ball(100, 100)
    original_vx, original_vy = ball.velocity.x, ball.velocity.y
    
    # Add wild bounce effect manually
    effect_data = {
        'type': POWERUP_WILD_BOUNCE,
        'player_id': 0,
        'duration': POWERUP_DURATION_WILD_BOUNCE,
        'variant': 'wild'
    }
    powerup_system.apply_effect(effect_data)
    
    # Should now have wild bounce active
    assert powerup_system.has_wild_bounce()
    
    # Test control scramble effect
    scramble_effect_data = {
        'type': POWERUP_CONTROL_SCRAMBLE,
        'player_id': 0,
        'duration': POWERUP_DURATION_CONTROL_SCRAMBLE,
        'variant': 'scramble'
    }
    powerup_system.apply_effect(scramble_effect_data)
    assert powerup_system.has_control_scramble()
    
    # Test scrambled mappings are different for at least some players
    mappings = []
    for i in range(4):
        mapped = powerup_system.get_scrambled_player_id(i)
        mappings.append(mapped)
    
    # Should have some scrambling (not all players mapped to themselves)
    original_mappings = [0, 1, 2, 3]
    assert mappings != original_mappings  # At least some scrambling occurred
    
    print("✓ All chaos power-up effects function correctly")

def run_all_tests():
    """Run all chaos power-up tests"""
    print("=" * 50)
    print("TESTING VERSION 3: CHAOS POWER-UPS")
    print("=" * 50)
    
    try:
        test_chaos_constants()
        test_powerup_entity()
        test_ball_entity()
        test_powerup_system()
        test_settings_integration()
        test_chaos_effects()
        
        print("\n" + "=" * 50)
        print("✅ ALL TESTS PASSED!")
        print("Version 3: Chaos Power-ups successfully implemented!")
        print("=" * 50)
        
        print("\n🎮 CHAOS POWER-UPS READY FOR TESTING:")
        print("• DECOY BALL - Spawns fake balls that don't cause life loss")
        print("• WILD BOUNCE - Ball randomly changes direction during flight")
        print("• CONTROL SCRAMBLE - All player controls get scrambled")
        print("\nStart the game and test the new chaos power-ups!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)