""""""
import datetime as dt
from wgups_implementation.package import Package


class DeliveryTruck:
    def __init__(self, truck_label, departure_time, address_list, distance_table):
        self.truck_label = truck_label
        self.packages_on = []
        self.packages_delivered = []
        self.current_location = '4001 South 700 East'
        self.destination = ''
        self.distance_to_destination = 0
        self.departure_time = dt.time(departure_time)
        self.current_time = dt.time(departure_time)
        self.address_id_array = []
        self.event_array = []
        self.address_list = address_list
        self.distance_table = distance_table

    def load_package(self, p):
        """This function will load a package 'p' onto truck, and update required fields for package and truck"""
        # Input check
        if p is None:
            raise TypeError("Package cannot be None")
        if not isinstance(p, Package):
            raise TypeError("Input must be instance of Package class")
        # append packages_on
        self.packages_on.append(p)
        p.load(self.truck_label)

    def deliver_package(self, p):
        # Input check
        if p is None:
            raise TypeError("Package cannot be None")
        if not isinstance(p, Package):
            raise TypeError("Input must be instance of Package class")
        if p not in self.packages_on:
            raise ValueError("Package is not available for delivery since it is not loaded to truck")
        p.deliver(self.current_time)
        self.packages_delivered.append(p)
        self.packages_on.remove(p)

    def distance_between(self, address1, address2, starter_index=None):
        print(3)

    """
    Finds the index of the nearest package based on the current address.
    """

    def min_distance_from(self, address_currently_at, packages, address_list):
        print(4)

    @staticmethod
    def distance_to_time(distance):
        return dt.timedelta(hours=distance / 18)

    def log_event(self, event):
        self.event_array.append([self.current_time, self.truck_label, event])

    def delivery_route(self):
        print(5)
