class Flight:
    def __init__(self, id, start_city, finish_city, plane, date):
        self.id = id
        self.start_city = start_city
        self.finish_city = finish_city
        self.plane = plane
        self.date = date
        self.reservations = []

    def add_reservation(self, reservation):
        self.reservations.append(reservation)

    def to_dict(self):
        return{
            'id': self.id,
            'start_city': self.start_city.to_dict(),
            'finish_city': self.finish_city.to_dict(),
            'plane_model': self.plane.to_dict(),
            'date': self.date
        }
