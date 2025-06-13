
class Item:
    """Represents an item of any type."""

    def __init__(self, id=None):
        # Initialize every attribute an item can have
        self.id = id
        self.type = None
        self.name = None
        self.image = None
        self.damage = None
        self.shot_speed = None
        self.fire_rate = None
        self.range = None
        self.tier = None
        self.shot_number = None
        self.shot_angle = None
        self.special = None
        self.special_amount = None