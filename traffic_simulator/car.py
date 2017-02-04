"""
Car model for simulations
"""

class Car:
    def __init__(self, car_id, distance_to_end, current_location):
        self.car_id = car_id
        self.speed = 0
        self.distance_to_end = distance_to_end
        self.pervious_location = None
        self.current_location = current_location

    def move(self, new_speed, new_location):
        """
        Function that helps a car to move to a new place.
        It checks whether the new location is different
        from the current location. If it is, the
        distance to end is reduced.
        """
        self.speed = new_speed
        if self.current_location != new_location:
            self.distance_to_end -= 1
        self.pervious_location = self.current_location
        self.current_location = new_location        
