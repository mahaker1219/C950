""""""
import datetime as dt
from wgups_implementation.package import Package


class DeliveryTruck:
    """All the main functionality happens here. Created to output an event array to use for state based rendering"""
    def __init__(self, truck_label, departure_time, address_list, distance_table):
        self.truck_label = truck_label
        self.packages_on = []
        self.packages_delivered = []
        self.current_location = '4001 South 700 East'
        self.current_location_id = 0
        self.destination = ''
        self.distance_to_destination = 0
        self.departure_time = dt.datetime.strptime(departure_time,'%H:%M')
        self.current_time = dt.datetime.strptime(departure_time,'%H:%M')
        self.address_id_array = []
        self.event_array = []
        self.address_list = address_list
        self.distance_table = distance_table
        self.mileage_traveled = 0
        self.delivery_deadline = []



    def load_package(self, p):
        """This function will load a package 'p' onto truck, and update required fields for package and truck"""
        # Input check
        if p is None:
            raise TypeError("Package cannot be None")
        if not isinstance(p, Package):
            raise TypeError("Input must be instance of Package class")
        # append packages_on
        self.packages_on.append(p)
        self.address_id_array.append(p.address_id)
        self.log_event("Package %s loaded onto Truck %s" % (p.pid, self.truck_label), p.pid, 'Load')
        p.load(self.truck_label)

    def deliver_package(self, p):
        # Input check
        if p is None:
            raise TypeError("Package cannot be None")
        if not isinstance(p, Package):
            raise TypeError("Input must be instance of Package class")
        if p not in self.packages_on:
            raise ValueError("Package is not available for delivery since it is not loaded to truck")
        p.deliver(self.current_time, self.truck_label)
        self.packages_delivered.append(p)
        self.packages_on.remove(p)
        if p in self.delivery_deadline:
            self.delivery_deadline.remove(p)

    def fill_address_id_onboard(self):
        for package in self.packages_on:
            package.fill_address_id(self.address_list)

    def distance_between(self, package1, package2=None, starter_index=None):
        if package2 is None:
            packages = [package1]
        else:
            packages = [package1, package2]

        for i in packages:
            if i is None:
                raise TypeError("Package cannot be None")
            if not isinstance(i, Package):
                raise TypeError("Input must be instance of Package class")
            if i not in self.packages_on:
                raise ValueError("Package is not available for delivery since it is not loaded to truck")

        self.fill_address_id_onboard()

        if starter_index is not None:
            p2 = int(starter_index)
        else:
            p2 = int(package2.address_id)

        if str(self.distance_table[package1.address_id][p2]) != '':
            return float(self.distance_table[package1.address_id][p2])
        elif str(self.distance_table[p2][package1.address_id]) != '':
            return float(self.distance_table[p2][package1.address_id])
        else:
            return None

    """
    Finds the index of the nearest package based on the current address.
    """

    def min_distance_from(self, address_currently_at, packages, address_list):
        """Iterates through all available packages to find which one is closest"""
        # Ensures proper input types
        if type(address_currently_at) != int:
            raise TypeError('address_currently_at must be an int representing the address_id')
        if type(packages) != list:
            raise TypeError('packages must be a list of instances of the Package class')
        if type(address_list) != list:
            raise TypeError('address_list must be a list of strings')
        for i in packages:
            if not isinstance(i, Package):
                raise TypeError("Input must be instance of Package class")
        for i in address_list:
            if type(i) != str:
                raise TypeError("address_list must only contain strings")
        if address_currently_at > len(address_list):
            raise ValueError("Address currently at must be within address_list")

        # Starts with maximum distance then iterates through all packages to find which has the min
        min_distance = 999
        closest_package = None
        for package in packages:
            distance = self.distance_between(package, starter_index=self.current_location_id)
            if distance < min_distance:
                min_distance = distance
                closest_package = package
        return closest_package, min_distance

    @staticmethod
    def distance_to_time(distance):
        return dt.timedelta(hours=distance / 18)

    def log_event(self, event, package_id=None, action=None):
        self.event_array.append([event, self.current_time.time(), package_id, action, self.truck_label])

    def delivery_route(self):
        for package in self.packages_on:
            package.depart(self.truck_label)
            self.log_event("Package %s departed on truck %s" % (package.pid, self.truck_label),
                           package.pid, 'Depart')
            if package.delivery_deadline != 'EOD':
                self.delivery_deadline.append(package)
        while len(self.packages_on) > 0:
            if len(self.delivery_deadline)>0:
                destination_package, distance_to_package = self.min_distance_from(self.current_location_id,
                                                                              self.delivery_deadline,
                                                                              self.address_list)
            else:
                destination_package, distance_to_package = self.min_distance_from(self.current_location_id,
                                                                                  self.packages_on,
                                                                                  self.address_list)
            # This part will update the time
            self.mileage_traveled += distance_to_package
            travel_time = self.distance_to_time(distance_to_package)
            self.current_time = self.current_time + travel_time
            self.deliver_package(destination_package)
            self.log_event("Delivered Package %s to %s" % (destination_package.pid, destination_package.address),
                           destination_package.pid, 'Deliver')
            self.current_location_id = destination_package.address_id
            self.current_location = destination_package.address
            # Ensures packages of the same address will be delivered as well
            for i in self.packages_on:
                if i.address_id == self.current_location:
                    self.deliver_package(i)
                    self.log_event("Delivered Package %s to %s" % (i.pid, i.address), i.pid,
                                   'Deliver')
        trip_to_hub_distance = float(self.distance_table[self.current_location_id][0])
        self.mileage_traveled += trip_to_hub_distance
        trip_to_hub_time = self.distance_to_time(trip_to_hub_distance)
        self.current_time = self.current_time + trip_to_hub_time
        self.current_location_id = 0
        self.current_location = self.address_list[0]
        self.log_event("Truck %s arrives back to hub" % self.truck_label)
        return self.event_array
