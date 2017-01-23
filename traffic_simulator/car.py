"""
Car model for simulations
"""

class Car:
    def __init__(self, distance_to_end, current_location):
        self.speed = 0
        self.distance_to_end = distance_to_end
        self.pervious_location = None
        self.current_location = current_location

    def move(self, new_speed, new_location):
        self.speed = new_speed
        if self.current_location != new_location:
            self.distance_to_end -= 1
        self.pervious_location = self.current_location
        self.current_location = new_location        
