class TouchData:
    def __init__(self,
                 x_distance,
                 y_distance,
                 x_offset,
                 y_offset,
                 relative_distance,
                 is_external,
                 in_range):
        self.x_distance = x_distance
        self.y_distance = y_distance
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.relative_distance = relative_distance
        self.is_external = is_external
        self.in_range = in_range
