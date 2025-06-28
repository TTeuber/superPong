#!/usr/bin/env python3
"""
Nintendo Switch Controller Button Tester

This script helps identify the correct button and axis numbers for the Nintendo Switch controller.
Press buttons and move analog sticks to see their corresponding numbers.

Controls:
- Press any controller button to see its number
- Move analog sticks to see axis values
- Press ESC to quit and print mapping summary
"""

import pygame
import sys
import os

def main():
    pygame.init()
    
    # Initialize joystick subsystem
    pygame.joystick.init()
    
    # Check for controller
    if pygame.joystick.get_count() == 0:
        print("No controller detected! Please connect your Nintendo Switch controller.")
        return
    
    # Initialize the first controller
    controller = pygame.joystick.Joystick(0)
    controller.init()
    
    print(f"Controller detected: {controller.get_name()}")
    print(f"Number of buttons: {controller.get_numbuttons()}")
    print(f"Number of axes: {controller.get_numaxes()}")
    print(f"Number of hats: {controller.get_numhats()}")
    print()
    print("Press buttons and move sticks to see their numbers.")
    print("Press ESC to quit and see mapping summary.")
    print("-" * 50)
    
    # Set up display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Switch Controller Button Tester")
    font = pygame.font.Font(None, 24)
    small_font = pygame.font.Font(None, 18)
    
    clock = pygame.time.Clock()
    running = True
    
    # Track button presses for mapping
    button_names = {}
    pressed_buttons = set()
    current_axes = {}
    
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                button_num = event.button
                pressed_buttons.add(button_num)
                print(f"Button {button_num} pressed")
            elif event.type == pygame.JOYBUTTONUP:
                button_num = event.button
                pressed_buttons.discard(button_num)
        
        # Update button states
        button_states = {}
        for i in range(controller.get_numbuttons()):
            button_states[i] = controller.get_button(i)
        
        # Update axis states
        axis_states = {}
        for i in range(controller.get_numaxes()):
            value = controller.get_axis(i)
            axis_states[i] = value
            # Track significant axis movements
            if abs(value) > 0.3:
                current_axes[i] = value
        
        # Update hat states (D-pad)
        hat_states = {}
        for i in range(controller.get_numhats()):
            hat_states[i] = controller.get_hat(i)
        
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Display title
        title = font.render("Nintendo Switch Controller Tester", True, (255, 255, 255))
        screen.blit(title, (10, 10))
        
        # Display controller info
        info = small_font.render(f"Controller: {controller.get_name()}", True, (200, 200, 200))
        screen.blit(info, (10, 40))
        
        # Display buttons
        y_offset = 70
        buttons_text = font.render("Buttons:", True, (255, 255, 0))
        screen.blit(buttons_text, (10, y_offset))
        y_offset += 30
        
        for i in range(controller.get_numbuttons()):
            color = (0, 255, 0) if button_states[i] else (100, 100, 100)
            status = "PRESSED" if button_states[i] else "released"
            text = small_font.render(f"Button {i:2d}: {status}", True, color)
            screen.blit(text, (10, y_offset + i * 20))
        
        # Display axes
        axes_y_start = y_offset + controller.get_numbuttons() * 20 + 20
        axes_text = font.render("Analog Sticks/Triggers:", True, (255, 255, 0))
        screen.blit(axes_text, (10, axes_y_start))
        axes_y_start += 30
        
        for i in range(controller.get_numaxes()):
            value = axis_states[i]
            color = (0, 255, 0) if abs(value) > 0.1 else (100, 100, 100)
            text = small_font.render(f"Axis {i:2d}: {value:+.3f}", True, color)
            screen.blit(text, (10, axes_y_start + i * 20))
        
        # Display hats (D-pad)
        if controller.get_numhats() > 0:
            hat_y_start = axes_y_start + controller.get_numaxes() * 20 + 20
            hat_text = font.render("D-pad (Hat):", True, (255, 255, 0))
            screen.blit(hat_text, (10, hat_y_start))
            hat_y_start += 30
            
            for i in range(controller.get_numhats()):
                hat_value = hat_states[i]
                color = (0, 255, 0) if hat_value != (0, 0) else (100, 100, 100)
                text = small_font.render(f"Hat {i}: {hat_value}", True, color)
                screen.blit(text, (10, hat_y_start + i * 20))
        
        # Display suggested mapping on the right side
        mapping_x = 400
        mapping_text = font.render("Suggested Button Mapping:", True, (0, 255, 255))
        screen.blit(mapping_text, (mapping_x, 70))
        
        suggestions = [
            "Try pressing these buttons:",
            "",
            "A button (bottom face button)",
            "B button (right face button)", 
            "X button (left face button)",
            "Y button (top face button)",
            "",
            "D-pad up/down/left/right",
            "",
            "Start/Plus button (top right)",
            "Select/Minus button (top left)",
            "",
            "Left analog stick (move around)",
            "Right analog stick (move around)",
            "",
            "L/R shoulder buttons",
            "ZL/ZR trigger buttons"
        ]
        
        for i, suggestion in enumerate(suggestions):
            color = (200, 200, 200) if suggestion else (100, 100, 100)
            text = small_font.render(suggestion, True, color)
            screen.blit(text, (mapping_x, 100 + i * 18))
        
        # Display exit instruction
        exit_text = font.render("Press ESC to quit and see mapping summary", True, (255, 100, 100))
        screen.blit(exit_text, (10, 550))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Print mapping summary
    print("\n" + "=" * 60)
    print("CONTROLLER MAPPING SUMMARY")
    print("=" * 60)
    print(f"Controller: {controller.get_name()}")
    print(f"Total buttons: {controller.get_numbuttons()}")
    print(f"Total axes: {controller.get_numaxes()}")
    print(f"Total hats: {controller.get_numhats()}")
    print()
    
    print("Use these values in your SWITCH_CONTROLLER_MAPPINGS:")
    print("{")
    print("    # Analog sticks")
    print("    'left_stick_x': 0,    # Usually axis 0")
    print("    'left_stick_y': 1,    # Usually axis 1") 
    print("    'right_stick_x': 2,   # Usually axis 2")
    print("    'right_stick_y': 3,   # Usually axis 3")
    print()
    print("    # Face buttons (test to confirm)")
    print("    'a_button': ?,        # Bottom face button")
    print("    'b_button': ?,        # Right face button")
    print("    'x_button': ?,        # Left face button") 
    print("    'y_button': ?,        # Top face button")
    print()
    print("    # System buttons")
    print("    'start_button': ?,    # Plus/Start button")
    print("    'select_button': ?,   # Minus/Select button")
    print()
    print("    # D-pad (if using buttons, not hat)")
    print("    'dpad_up': ?,")
    print("    'dpad_down': ?,")
    print("    'dpad_left': ?,")
    print("    'dpad_right': ?,")
    print("}")
    
    pygame.quit()

if __name__ == "__main__":
    main()