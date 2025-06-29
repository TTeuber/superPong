import pygame
from utils.constants import CONTROLLER_DEADZONE, CONTROLLER_SENSITIVITY, SWITCH_CONTROLLER_MAPPINGS

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        
        # Initialize joystick subsystem
        pygame.joystick.init()
        
        # Controller state
        self.controller = None
        self.controller_connected = False
        self.controller_buttons = {}
        self.controller_axes = {}
        
        # Initialize controller if available
        self.initialize_controller()

        # Key mappings for up to 4 players
        self.key_mappings = {
            0: {  # Player 1 (Left paddle) - WASD
                'up': pygame.K_w,
                'down': pygame.K_s,
            },
            1: {  # Player 2 (Right paddle) - Arrow keys
                'up': pygame.K_UP,
                'down': pygame.K_DOWN,
            },
            2: {  # Player 3 (Top paddle) - IJKL
                'left': pygame.K_j,
                'right': pygame.K_l,
            },
            3: {  # Player 4 (Bottom paddle) - Numpad
                'left': pygame.K_KP4,
                'right': pygame.K_KP6,
            }
        }

    def initialize_controller(self):
        """Initialize the first available controller"""
        if pygame.joystick.get_count() > 0:
            self.controller = pygame.joystick.Joystick(0)
            self.controller.init()
            self.controller_connected = True
            print(f"Controller connected: {self.controller.get_name()}")
        else:
            self.controller_connected = False
            print("No controller detected, using keyboard input")

    def handle_controller_events(self, event):
        """Handle controller connection/disconnection events"""
        if event.type == pygame.JOYDEVICEADDED:
            if not self.controller_connected:
                self.initialize_controller()
        elif event.type == pygame.JOYDEVICEREMOVED:
            if self.controller_connected:
                self.controller_connected = False
                self.controller = None
                print("Controller disconnected, switching to keyboard input")

    def update_controller_state(self):
        """Update controller button and axis states"""
        if not self.controller_connected or not self.controller:
            return
            
        # Update button states
        self.controller_buttons = {}
        for i in range(self.controller.get_numbuttons()):
            self.controller_buttons[i] = self.controller.get_button(i)
            
        # Update axis states
        self.controller_axes = {}
        for i in range(self.controller.get_numaxes()):
            axis_value = self.controller.get_axis(i)
            # Apply deadzone
            if abs(axis_value) < CONTROLLER_DEADZONE:
                axis_value = 0.0
            self.controller_axes[i] = axis_value

    def get_controller_movement(self, player_id):
        """Get movement input from controller for specified player"""
        if not self.controller_connected or player_id != 0:
            return {'up': False, 'down': False, 'left': False, 'right': False}
        
        movement = {'up': False, 'down': False, 'left': False, 'right': False}
        
        # Check analog stick (left stick Y-axis for vertical paddles)
        left_stick_y_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_y', 1)
        if left_stick_y_axis in self.controller_axes:
            stick_y = self.controller_axes[left_stick_y_axis]
            # Invert Y-axis (negative = up, positive = down)
            if stick_y < -CONTROLLER_DEADZONE:
                movement['up'] = True
            elif stick_y > CONTROLLER_DEADZONE:
                movement['down'] = True
        
        # Check D-pad buttons as backup
        dpad_up = SWITCH_CONTROLLER_MAPPINGS.get('dpad_up', 13)
        dpad_down = SWITCH_CONTROLLER_MAPPINGS.get('dpad_down', 14)
        
        if dpad_up in self.controller_buttons and self.controller_buttons[dpad_up]:
            movement['up'] = True
        if dpad_down in self.controller_buttons and self.controller_buttons[dpad_down]:
            movement['down'] = True
            
        return movement

    def is_pause_pressed(self):
        """Check if pause button/key is pressed (single press detection)"""
        # Check keyboard pause (P key or SPACE)
        keyboard_pause = pygame.K_p in self.keys_pressed or pygame.K_SPACE in self.keys_pressed
        
        # Check controller pause buttons
        controller_pause = False
        if self.controller_connected:
            start_button = SWITCH_CONTROLLER_MAPPINGS.get('start_button', 9)
            select_button = SWITCH_CONTROLLER_MAPPINGS.get('select_button', 8)
            
            controller_pause = (
                (start_button in self.controller_buttons and self.controller_buttons[start_button]) or
                (select_button in self.controller_buttons and self.controller_buttons[select_button])
            )
        
        return keyboard_pause or controller_pause

    def get_menu_navigation(self):
        """Get menu navigation direction (-1 for up, 1 for down, 0 for none)"""
        # Check keyboard input
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            return -1
        elif pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            return 1
        
        # Check controller input
        if self.controller_connected:
            # Check left analog stick
            left_stick_y_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_y', 1)
            if left_stick_y_axis in self.controller_axes:
                stick_y = self.controller_axes[left_stick_y_axis]
                if stick_y < -CONTROLLER_DEADZONE:
                    return -1
                elif stick_y > CONTROLLER_DEADZONE:
                    return 1
            
            # Check D-pad
            dpad_up = SWITCH_CONTROLLER_MAPPINGS.get('dpad_up', 12)
            dpad_down = SWITCH_CONTROLLER_MAPPINGS.get('dpad_down', 13)
            
            if dpad_up in self.controller_buttons and self.controller_buttons[dpad_up]:
                return -1
            elif dpad_down in self.controller_buttons and self.controller_buttons[dpad_down]:
                return 1
        
        return 0

    def is_menu_confirm_pressed(self):
        """Check if menu confirmation button/key is pressed"""
        # Check keyboard input
        keyboard_confirm = pygame.K_RETURN in self.keys_pressed or pygame.K_SPACE in self.keys_pressed
        
        # Check controller input
        controller_confirm = False
        if self.controller_connected:
            a_button = SWITCH_CONTROLLER_MAPPINGS.get('a_button', 0)
            controller_confirm = a_button in self.controller_buttons and self.controller_buttons[a_button]
        
        return keyboard_confirm or controller_confirm

    def is_menu_cancel_pressed(self):
        """Check if menu cancel/back button is pressed (B button or ESC)"""
        # Check keyboard input
        keyboard_cancel = pygame.K_ESCAPE in self.keys_pressed
        
        # Check controller input
        controller_cancel = False
        if self.controller_connected:
            b_button = SWITCH_CONTROLLER_MAPPINGS.get('b_button', 1)
            controller_cancel = b_button in self.controller_buttons and self.controller_buttons[b_button]
        
        return keyboard_cancel or controller_cancel

    def handle_events(self, events):
        """Process pygame events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
            else:
                # Handle controller events
                self.handle_controller_events(event)
        
        # Update controller state each frame
        self.update_controller_state()

    def update_paddle_movement(self, paddles):
        """Update paddle movement based on current key and controller states"""
        for player_id, paddle in enumerate(paddles):
            if player_id not in self.key_mappings:
                continue

            mapping = self.key_mappings[player_id]

            # Reset movement flags
            paddle.moving_up = False
            paddle.moving_down = False
            paddle.moving_left = False
            paddle.moving_right = False

            # For Player 1 (left paddle), check controller input first, then keyboard
            if player_id == 0 and self.controller_connected:
                controller_movement = self.get_controller_movement(player_id)
                if paddle.orientation == 'vertical':
                    paddle.moving_up = controller_movement['up']
                    paddle.moving_down = controller_movement['down']
                else:  # horizontal
                    paddle.moving_left = controller_movement['left']
                    paddle.moving_right = controller_movement['right']
            
            # Always check keyboard input (controller overrides keyboard for Player 1)
            # For other players, only keyboard input is available
            if paddle.orientation == 'vertical':
                keyboard_up = mapping.get('up') in self.keys_pressed
                keyboard_down = mapping.get('down') in self.keys_pressed
                
                # If no controller input for Player 1, use keyboard
                if player_id != 0 or not self.controller_connected:
                    paddle.moving_up = keyboard_up
                    paddle.moving_down = keyboard_down
                elif player_id == 0:
                    # For Player 1 with controller, keyboard can override if pressed
                    if keyboard_up:
                        paddle.moving_up = True
                    if keyboard_down:
                        paddle.moving_down = True
                        
            else:  # horizontal
                keyboard_left = mapping.get('left') in self.keys_pressed
                keyboard_right = mapping.get('right') in self.keys_pressed
                
                if player_id != 0 or not self.controller_connected:
                    paddle.moving_left = keyboard_left
                    paddle.moving_right = keyboard_right
                elif player_id == 0:
                    if keyboard_left:
                        paddle.moving_left = True
                    if keyboard_right:
                        paddle.moving_right = True

    def is_key_pressed(self, key):
        """Check if a specific key is currently pressed"""
        return key in self.keys_pressed
    
    def reset_input_states(self):
        """Reset input states to prevent input leakage between game states"""
        # Clear keyboard states
        self.keys_pressed.clear()
        
        # Clear controller button states
        if self.controller_connected:
            self.controller_buttons.clear()
            self.controller_axes.clear()