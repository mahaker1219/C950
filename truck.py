""""""
import package

class DeliveryTruck:
    def __init__(self, truck_label, departure_time):
        self.truck_label = truck_label
        self.packages_on = []
        self.packages_delivered = []
        self.current_location = ''
        self.destination = ''
        self.distance_to_destination = 0
        self.departure_time = departure_time
        self.current_time = departure_time
        self.address_id_array = []

    def load_package(self, p):
        # need to add state change functionality here
        self.packages_on.append(p)
        p.load(self.truck_label)

    def deliver_package(self, p):
        # need to add state change functionality here
        # need to add a search then delete function
        self.packages_on.pop(p)
        self.packages_delivered.append(p)
        p.deliver(self.current_time)
