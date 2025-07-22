import pygame
from utils.constants import CONTROLLER_DEADZONE, CONTROLLER_SENSITIVITY, SWITCH_CONTROLLER_MAPPINGS, MAX_CONTROLLERS

class InputHandler:
    def __init__(self):
        self.keys_pressed = set()
        
        # Initialize joystick subsystem
        pygame.joystick.init()
        
        # Multiple controller state
        self.controllers = {}  # Dict of {controller_index: pygame.Joystick}
        self.multi_controller_buttons = {}  # Dict of {controller_index: {button_id: pressed}}
        self.multi_controller_axes = {}  # Dict of {controller_index: {axis_id: value}}
        self.controller_just_pressed_a = {}  # Dict of {controller_index: bool} for A button detection
        
        # Player assignment to controllers
        self.player_controllers = {}  # Dict of {player_id: controller_index}
        self.controller_players = {}  # Dict of {controller_index: player_id}
        
        # Legacy single controller support (for backwards compatibility)
        self.controller = None
        self.controller_connected = False
        self.controller_buttons = {}  # Legacy format for backwards compatibility
        self.controller_axes = {}  # Legacy format for backwards compatibility
        
        # Mouse state
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.mouse_just_clicked = False  # Single frame click detection
        
        # Key press tracking for single-press detection
        self.escape_just_pressed = False
        self.space_just_pressed = False
        self.escape_used_for_pause = False  # Track if escape was used for pause
        self.space_used_for_pause = False   # Track if space was used for pause
        
        # Menu navigation single-press detection
        self.menu_nav_pressed = False  # Track if navigation input was already processed
        
        # Initialize controllers if available
        self.initialize_controllers()

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

    def initialize_controllers(self):
        """Initialize all available controllers"""
        controller_count = pygame.joystick.get_count()
        print(f"Detected {controller_count} controller(s)")
        
        self.controllers.clear()
        self.multi_controller_buttons.clear()
        self.multi_controller_axes.clear()
        self.controller_just_pressed_a.clear()
        
        for i in range(min(controller_count, MAX_CONTROLLERS)):
            try:
                controller = pygame.joystick.Joystick(i)
                controller.init()
                self.controllers[i] = controller
                self.multi_controller_buttons[i] = {}
                self.multi_controller_axes[i] = {}
                self.controller_just_pressed_a[i] = False
                print(f"Controller {i} initialized: {controller.get_name()}")
            except pygame.error as e:
                print(f"Failed to initialize controller {i}: {e}")
        
        # Maintain backwards compatibility with single controller
        if 0 in self.controllers:
            self.controller = self.controllers[0]
            self.controller_connected = True
        else:
            self.controller = None
            self.controller_connected = False
            
        if not self.controllers:
            print("No controllers detected, using keyboard input")

    def handle_controller_events(self, event):
        """Handle controller connection/disconnection events"""
        if event.type == pygame.JOYDEVICEADDED:
            print(f"Controller connected (device {event.device_index})")
            self.initialize_controllers()  # Re-initialize all controllers
        elif event.type == pygame.JOYDEVICEREMOVED:
            print(f"Controller disconnected (device {event.device_index})")
            # Remove the disconnected controller from our tracking
            if event.device_index in self.controllers:
                del self.controllers[event.device_index]
                del self.multi_controller_buttons[event.device_index]
                del self.multi_controller_axes[event.device_index]
                del self.controller_just_pressed_a[event.device_index]
                
                # Remove from player assignments
                if event.device_index in self.controller_players:
                    player_id = self.controller_players[event.device_index]
                    del self.player_controllers[player_id]
                    del self.controller_players[event.device_index]
            
            # Update legacy controller reference
            if 0 in self.controllers:
                self.controller = self.controllers[0]
                self.controller_connected = True
            else:
                self.controller = None
                self.controller_connected = False

    def update_controller_state(self):
        """Update controller button and axis states for all controllers"""
        # Reset A button just pressed states
        for controller_index in self.controller_just_pressed_a:
            self.controller_just_pressed_a[controller_index] = False
            
        for controller_index, controller in self.controllers.items():
            try:
                # Update button states
                previous_buttons = self.multi_controller_buttons[controller_index].copy()
                self.multi_controller_buttons[controller_index] = {}
                for i in range(controller.get_numbuttons()):
                    current_pressed = controller.get_button(i)
                    self.multi_controller_buttons[controller_index][i] = current_pressed
                    
                    # Detect A button just pressed (was not pressed, now pressed)
                    a_button = SWITCH_CONTROLLER_MAPPINGS.get('a_button', 0)
                    if i == a_button and current_pressed and not previous_buttons.get(i, False):
                        self.controller_just_pressed_a[controller_index] = True
                
                # Update axis states
                self.multi_controller_axes[controller_index] = {}
                for i in range(controller.get_numaxes()):
                    axis_value = controller.get_axis(i)
                    # Apply deadzone
                    if abs(axis_value) < CONTROLLER_DEADZONE:
                        axis_value = 0.0
                    self.multi_controller_axes[controller_index][i] = axis_value
                    
            except pygame.error as e:
                print(f"Error updating controller {controller_index} state: {e}")
                
        # Update legacy single controller state for backwards compatibility
        if 0 in self.multi_controller_buttons:
            # Map first controller to legacy format for existing code
            # CRITICAL: Update the actual legacy attributes that existing code uses
            self.controller_buttons = self.multi_controller_buttons[0].copy()
            self.controller_axes = self.multi_controller_axes[0].copy()
        else:
            # No controllers connected, clear legacy state
            self.controller_buttons = {}
            self.controller_axes = {}

    def get_available_controllers(self):
        """Get list of available controller indices"""
        return list(self.controllers.keys())
    
    def is_controller_connected(self, controller_index):
        """Check if a specific controller is connected"""
        return controller_index in self.controllers
    
    def get_controller_name(self, controller_index):
        """Get the name of a specific controller"""
        if controller_index in self.controllers:
            return self.controllers[controller_index].get_name()
        return None
    
    def assign_player_to_controller(self, player_id, controller_index):
        """Assign a player to a specific controller"""
        if controller_index in self.controllers:
            # Remove any existing assignments
            if player_id in self.player_controllers:
                old_controller = self.player_controllers[player_id]
                if old_controller in self.controller_players:
                    del self.controller_players[old_controller]
            
            if controller_index in self.controller_players:
                old_player = self.controller_players[controller_index]
                if old_player in self.player_controllers:
                    del self.player_controllers[old_player]
            
            # Create new assignment
            self.player_controllers[player_id] = controller_index
            self.controller_players[controller_index] = player_id
            return True
        
        return False
    
    def get_player_controller(self, player_id):
        """Get the controller assigned to a player"""
        return self.player_controllers.get(player_id, None)
    
    def get_controller_player(self, controller_index):
        """Get the player assigned to a controller"""
        return self.controller_players.get(controller_index, None)
    
    def is_controller_a_just_pressed(self, controller_index):
        """Check if A button was just pressed on a specific controller"""
        return self.controller_just_pressed_a.get(controller_index, False)
    
    def get_unassigned_controllers(self):
        """Get list of controllers not assigned to any player"""
        return [c for c in self.controllers.keys() if c not in self.controller_players]
    
    def clear_player_assignments(self):
        """Clear all player-controller assignments"""
        self.player_controllers.clear()
        self.controller_players.clear()

    def get_controller_movement(self, player_id):
        """Get movement input from controller for specified player (legacy single-controller method)"""
        # Legacy method: Only Player 0 can use the first controller
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

    def get_multi_controller_movement(self, player_id):
        """Get movement input from assigned controller for specified player (multi-controller system)"""
        movement = {'up': False, 'down': False, 'left': False, 'right': False}
        
        # Get the controller assigned to this player
        controller_index = self.get_player_controller(player_id)
        
        if controller_index is None:
            return movement
        
        # Check if the controller is still connected
        if controller_index not in self.multi_controller_axes or controller_index not in self.multi_controller_buttons:
            return movement
        
        controller_axes = self.multi_controller_axes[controller_index]
        controller_buttons = self.multi_controller_buttons[controller_index]
        
        # Check analog stick (left stick Y-axis for vertical paddles, X-axis for horizontal)
        left_stick_y_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_y', 1)
        left_stick_x_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_x', 0)
        
        if left_stick_y_axis in controller_axes:
            stick_y = controller_axes[left_stick_y_axis]
            # Invert Y-axis (negative = up, positive = down)
            if stick_y < -CONTROLLER_DEADZONE:
                movement['up'] = True
            elif stick_y > CONTROLLER_DEADZONE:
                movement['down'] = True
        
        if left_stick_x_axis in controller_axes:
            stick_x = controller_axes[left_stick_x_axis]
            if stick_x < -CONTROLLER_DEADZONE:
                movement['left'] = True
            elif stick_x > CONTROLLER_DEADZONE:
                movement['right'] = True
        
        # Check D-pad buttons as backup
        dpad_up = SWITCH_CONTROLLER_MAPPINGS.get('dpad_up', 12)
        dpad_down = SWITCH_CONTROLLER_MAPPINGS.get('dpad_down', 13)
        dpad_left = SWITCH_CONTROLLER_MAPPINGS.get('dpad_left', 14)
        dpad_right = SWITCH_CONTROLLER_MAPPINGS.get('dpad_right', 15)
        
        if dpad_up in controller_buttons and controller_buttons[dpad_up]:
            movement['up'] = True
        if dpad_down in controller_buttons and controller_buttons[dpad_down]:
            movement['down'] = True
        if dpad_left in controller_buttons and controller_buttons[dpad_left]:
            movement['left'] = True
        if dpad_right in controller_buttons and controller_buttons[dpad_right]:
            movement['right'] = True
            
        return movement

    def is_pause_pressed(self):
        """Check if pause button/key is pressed (single press detection)"""
        # Check keyboard pause (Escape key or SPACE) - only on initial press
        keyboard_pause = self.escape_just_pressed or self.space_just_pressed
        
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
        """Get menu navigation direction (-1 for up, 1 for down, 0 for none) with single-press detection"""
        nav_input_detected = False
        nav_direction = 0
        
        # Check keyboard input
        if pygame.K_UP in self.keys_pressed or pygame.K_w in self.keys_pressed:
            nav_input_detected = True
            nav_direction = -1
        elif pygame.K_DOWN in self.keys_pressed or pygame.K_s in self.keys_pressed:
            nav_input_detected = True
            nav_direction = 1
        
        # Check controller input
        if self.controller_connected and nav_direction == 0:
            # Check left analog stick
            left_stick_y_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_y', 1)
            if left_stick_y_axis in self.controller_axes:
                stick_y = self.controller_axes[left_stick_y_axis]
                if stick_y < -CONTROLLER_DEADZONE:
                    nav_input_detected = True
                    nav_direction = -1
                elif stick_y > CONTROLLER_DEADZONE:
                    nav_input_detected = True
                    nav_direction = 1
            
            # Check D-pad (if stick didn't trigger)
            if nav_direction == 0:
                dpad_up = SWITCH_CONTROLLER_MAPPINGS.get('dpad_up', 12)
                dpad_down = SWITCH_CONTROLLER_MAPPINGS.get('dpad_down', 13)
                
                if dpad_up in self.controller_buttons and self.controller_buttons[dpad_up]:
                    nav_input_detected = True
                    nav_direction = -1
                elif dpad_down in self.controller_buttons and self.controller_buttons[dpad_down]:
                    nav_input_detected = True
                    nav_direction = 1
        
        # Single-press detection logic
        if nav_input_detected:
            if not self.menu_nav_pressed:
                self.menu_nav_pressed = True
                return nav_direction
        else:
            self.menu_nav_pressed = False
        
        return 0

    def is_menu_confirm_pressed(self):
        """Check if menu confirmation button/key is pressed"""
        # Check keyboard input - exclude space if it was used for pause
        keyboard_confirm = pygame.K_RETURN in self.keys_pressed or (pygame.K_SPACE in self.keys_pressed and not self.space_used_for_pause)
        
        # Check controller input
        controller_confirm = False
        if self.controller_connected:
            a_button = SWITCH_CONTROLLER_MAPPINGS.get('a_button', 0)
            controller_confirm = a_button in self.controller_buttons and self.controller_buttons[a_button]
        
        return keyboard_confirm or controller_confirm

    def get_horizontal_navigation(self):
        """Get horizontal navigation direction (-1 for left, 1 for right, 0 for none)"""
        # Check keyboard input
        if pygame.K_LEFT in self.keys_pressed or pygame.K_a in self.keys_pressed:
            return -1
        elif pygame.K_RIGHT in self.keys_pressed or pygame.K_d in self.keys_pressed:
            return 1
        
        # Check controller input
        if self.controller_connected:
            # Check left analog stick
            left_stick_x_axis = SWITCH_CONTROLLER_MAPPINGS.get('left_stick_x', 0)
            if left_stick_x_axis in self.controller_axes:
                stick_x = self.controller_axes[left_stick_x_axis]
                if stick_x < -CONTROLLER_DEADZONE:
                    return -1
                elif stick_x > CONTROLLER_DEADZONE:
                    return 1
            
            # Check D-pad
            dpad_left = SWITCH_CONTROLLER_MAPPINGS.get('dpad_left', 14)
            dpad_right = SWITCH_CONTROLLER_MAPPINGS.get('dpad_right', 15)
            
            if dpad_left in self.controller_buttons and self.controller_buttons[dpad_left]:
                return -1
            elif dpad_right in self.controller_buttons and self.controller_buttons[dpad_right]:
                return 1
        
        return 0

    def is_menu_cancel_pressed(self):
        """Check if menu cancel/back button is pressed (B button or ESC)"""
        # Check keyboard input - only allow escape if it wasn't used for pause this frame or last frame
        keyboard_cancel = pygame.K_ESCAPE in self.keys_pressed and not self.escape_just_pressed and not self.escape_used_for_pause
        
        # Check controller input
        controller_cancel = False
        if self.controller_connected:
            b_button = SWITCH_CONTROLLER_MAPPINGS.get('b_button', 1)
            controller_cancel = b_button in self.controller_buttons and self.controller_buttons[b_button]
        
        return keyboard_cancel or controller_cancel

    def handle_events(self, events):
        """Process pygame events"""
        # Reset single-frame detections
        self.mouse_just_clicked = False
        self.escape_just_pressed = False
        self.space_just_pressed = False
        # DON'T reset pause usage flags here - they persist until key release
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                # Track single key presses
                if event.key == pygame.K_ESCAPE:
                    self.escape_just_pressed = True
                elif event.key == pygame.K_SPACE:
                    self.space_just_pressed = True
            elif event.type == pygame.KEYUP:
                self.keys_pressed.discard(event.key)
                # Reset pause usage flags when keys are released
                if event.key == pygame.K_ESCAPE:
                    self.escape_used_for_pause = False
                elif event.key == pygame.K_SPACE:
                    self.space_used_for_pause = False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_clicked = True
                    self.mouse_just_clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    self.mouse_clicked = False
            else:
                # Handle controller events
                self.handle_controller_events(event)
        
        # Update controller state each frame
        self.update_controller_state()

    def update_paddle_movement(self, paddles):
        """Update paddle movement based on current key and controller states"""
        for paddle in paddles:
            # Use the paddle's actual player_id, not the enumerate index
            player_id = paddle.player_id
            
            if player_id not in self.key_mappings:
                continue

            mapping = self.key_mappings[player_id]

            # Reset movement flags
            paddle.moving_up = False
            paddle.moving_down = False
            paddle.moving_left = False
            paddle.moving_right = False

            # Check for assigned controller first (multi-controller system)
            controller_movement = self.get_multi_controller_movement(player_id)
            has_controller_input = any(controller_movement.values())
            
            if has_controller_input:
                # Use multi-controller input
                if paddle.orientation == 'vertical':
                    paddle.moving_up = controller_movement['up']
                    paddle.moving_down = controller_movement['down']
                else:  # horizontal
                    paddle.moving_left = controller_movement['left']
                    paddle.moving_right = controller_movement['right']
            
            # Check keyboard input (always available, can supplement controller)
            if paddle.orientation == 'vertical':
                keyboard_up = mapping.get('up') in self.keys_pressed
                keyboard_down = mapping.get('down') in self.keys_pressed
                
                # Use keyboard if no controller, or allow keyboard to supplement controller
                if not has_controller_input:
                    paddle.moving_up = keyboard_up
                    paddle.moving_down = keyboard_down
                else:
                    # Allow keyboard to override controller (useful for debugging/backup)
                    if keyboard_up:
                        paddle.moving_up = True
                    if keyboard_down:
                        paddle.moving_down = True
                        
            else:  # horizontal
                keyboard_left = mapping.get('left') in self.keys_pressed
                keyboard_right = mapping.get('right') in self.keys_pressed
                
                if not has_controller_input:
                    paddle.moving_left = keyboard_left
                    paddle.moving_right = keyboard_right
                else:
                    # Allow keyboard to override controller
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
            # Also clear multi-controller states
            for controller_index in self.multi_controller_buttons:
                self.multi_controller_buttons[controller_index].clear()
            for controller_index in self.multi_controller_axes:
                self.multi_controller_axes[controller_index].clear()
            
        # Clear mouse states
        self.mouse_clicked = False
        self.mouse_just_clicked = False
        
        # Clear key press states
        self.escape_just_pressed = False
        self.space_just_pressed = False
        # Reset pause usage flags when doing full reset
        self.escape_used_for_pause = False
        self.space_used_for_pause = False
        # Reset navigation state
        self.menu_nav_pressed = False
    
    def get_mouse_pos(self):
        """Get current mouse position"""
        return self.mouse_pos
    
    def is_mouse_clicked(self):
        """Check if mouse was just clicked this frame"""
        return self.mouse_just_clicked
    
    def is_point_in_rect(self, point, rect):
        """Check if a point is inside a rectangle"""
        x, y = point
        return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]
    
    def mark_escape_used_for_pause(self):
        """Mark that escape was used for pause this frame"""
        self.escape_used_for_pause = True
    
    def mark_space_used_for_pause(self):
        """Mark that space was used for pause this frame"""
        self.space_used_for_pause = True