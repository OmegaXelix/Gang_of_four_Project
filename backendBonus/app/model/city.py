class City:
    def __init__(self, id, city_name):
        self.id = id
        self.city_name = city_name

    def to_dict(self):
        return {
            'id': self.id,
            'city_name': self.city_name
        }