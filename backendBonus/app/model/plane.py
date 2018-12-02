class Aeroplane:
    def __init__(self, id, model, seats):
        self.id = id
        self.model = model
        self.seats = seats

    def to_dict(self):
        return{
            'id': self.id,
            'model': self.model,
            'max_seats': self.seats
        }