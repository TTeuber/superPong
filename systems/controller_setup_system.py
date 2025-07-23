from utils import constants

class ControllerSetupSystem:
    """Manages controller assignment and readiness tracking for multiplayer games"""
    
    def __init__(self, input_handler):
        self.input_handler = input_handler
        self.required_players = 2  # Will be set based on player count selection
        
        # Player readiness tracking
        self.player_ready = {}  # Dict of {player_id: bool}
        self.player_controllers = {}  # Dict of {player_id: controller_index}
        
        # Visual feedback
        self.ready_circle_fill = {}  # Dict of {player_id: fill_percentage (0.0-1.0)}
        
        # Auto-assignment tracking
        self.auto_assignment_attempted = False
        
    def set_required_players(self, player_count):
        """Set the number of players required for this game"""
        self.required_players = player_count
        self.reset_ready_state()
    
    def reset_ready_state(self):
        """Reset all readiness states"""
        self.player_ready.clear()
        self.player_controllers.clear()
        self.ready_circle_fill.clear()
        self.auto_assignment_attempted = False
        
        # Initialize all required players as not ready
        for player_id in range(self.required_players):
            self.player_ready[player_id] = False
            self.ready_circle_fill[player_id] = 0.0
    
    def attempt_auto_assignment(self):
        """Attempt to automatically assign available controllers to players"""
        if self.auto_assignment_attempted:
            return
        
        available_controllers = self.input_handler.get_available_controllers()
        print(f"Attempting auto-assignment with {len(available_controllers)} controllers for {self.required_players} players")
        
        # Clear existing assignments
        self.input_handler.clear_player_assignments()
        
        # Assign controllers to players in order
        assignments_made = 0
        for player_id in range(self.required_players):
            if assignments_made < len(available_controllers):
                controller_index = available_controllers[assignments_made]
                if self.input_handler.assign_player_to_controller(player_id, controller_index):
                    self.player_controllers[player_id] = controller_index
                    assignments_made += 1
                    controller_name = self.input_handler.get_controller_name(controller_index)
                    print(f"Auto-assigned Player {player_id + 1} to Controller {controller_index} ({controller_name})")
        
        self.auto_assignment_attempted = True
        
        # Show warning if not enough controllers
        if assignments_made < self.required_players:
            print(f"Warning: Only {assignments_made} controllers available for {self.required_players} players")
            print("Additional players will need to use keyboard controls")
    
    def update(self):
        """Update controller setup state - check for A button presses"""
        available_controllers = self.input_handler.get_available_controllers()
        
        # Check each controller for A button press
        for controller_index in available_controllers:
            if self.input_handler.is_controller_a_just_pressed(controller_index):
                # Find which player this controller is assigned to
                player_id = self.input_handler.get_controller_player(controller_index)
                if player_id is not None and player_id < self.required_players:
                    # Toggle ready state
                    self.player_ready[player_id] = not self.player_ready[player_id]
                    controller_name = self.input_handler.get_controller_name(controller_index)
                    ready_status = "ready" if self.player_ready[player_id] else "not ready"
                    print(f"Player {player_id + 1} ({controller_name}) is now {ready_status}")
        
        # Update visual fill percentages for ready circles
        for player_id in range(self.required_players):
            target_fill = 1.0 if self.player_ready[player_id] else 0.0
            current_fill = self.ready_circle_fill[player_id]
            
            # Smooth animation towards target
            if current_fill != target_fill:
                fill_speed = 0.1  # Animation speed
                if target_fill > current_fill:
                    self.ready_circle_fill[player_id] = min(1.0, current_fill + fill_speed)
                else:
                    self.ready_circle_fill[player_id] = max(0.0, current_fill - fill_speed)
    
    def are_all_players_ready(self):
        """Check if all required players are ready"""
        if len(self.player_ready) < self.required_players:
            return False
        
        for player_id in range(self.required_players):
            if not self.player_ready.get(player_id, False):
                return False
        
        return True
    
    def get_player_ready_status(self, player_id):
        """Get ready status for a specific player"""
        return self.player_ready.get(player_id, False)
    
    def get_ready_circle_fill(self, player_id):
        """Get the fill percentage for a player's ready circle"""
        return self.ready_circle_fill.get(player_id, 0.0)
    
    def get_player_controller_name(self, player_id):
        """Get the controller name for a specific player"""
        controller_index = self.player_controllers.get(player_id)
        if controller_index is not None:
            return self.input_handler.get_controller_name(controller_index)
        return None
    
    def get_player_controller_index(self, player_id):
        """Get the controller index for a specific player"""
        return self.player_controllers.get(player_id)
    
    def get_ready_count(self):
        """Get the number of players currently ready"""
        ready_count = 0
        for player_id in range(self.required_players):
            if self.player_ready.get(player_id, False):
                ready_count += 1
        return ready_count
    
    def get_required_players(self):
        """Get the number of required players"""
        return self.required_players
    
    def get_controller_assignments(self):
        """Get a dict of player assignments for game initialization"""
        assignments = {}
        for player_id in range(self.required_players):
            controller_index = self.player_controllers.get(player_id)
            assignments[player_id] = {
                'has_controller': controller_index is not None,
                'controller_index': controller_index,
                'is_human': True,  # All players in multiplayer are human
                'ready': self.player_ready.get(player_id, False)
            }
        return assignments
    
    def get_insufficient_controllers_warning(self):
        """Get warning message if there are insufficient controllers"""
        available_count = len(self.input_handler.get_available_controllers())
        if available_count < self.required_players:
            missing_count = self.required_players - available_count
            return f"Warning: {missing_count} player(s) will use keyboard controls"
        return None
    
    def reset(self):
        """Reset the controller setup system"""
        self.required_players = 2
        self.reset_ready_state()
        self.input_handler.clear_player_assignments()