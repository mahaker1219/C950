""""""
import datetime as dt
import list_search as ls


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
        # need to add state change functionality here
        self.packages_on.append(p)
        p.load(self.truck_label)

    def deliver_package(self, p):
        # need to add state change functionality here
        # need to add a search then delete function
        self.packages_delivered.append(p)
        p.deliver(self.current_time)
        packages_on = []
        for i in self.packages_on:
            if i.pid != p.pid:
                packages_on.append(i)
        self.packages_on = packages_on

    def distance_between(self, address1, address2, starter_index=None):
        if starter_index is None:
            ind1 = None
            ind2 = None
            if ls.list_search(self.address_list, address1) is not None:
                ind1 = ls.list_search(self.address_list, address1)
            if ls.list_search(self.address_list, address2) is not None:
                ind2 = ls.list_search(self.address_list, address2)
            if ind1 is not None and ind2 is not None:
                if self.distance_table[ind1][ind2] != '':
                    return self.distance_table[ind1][ind2]
                else:
                    return self.distance_table[ind2][ind1]
            else:
                print('Problem with index derivation')
                return None
        else:
            ind1 = starter_index
            ind2 = None
            if ls.list_search(self.address_list, address2) is not None:
                ind2 = ls.list_search(self.address_list, address2)
            if ind1 is not None and ind2 is not None:
                if self.distance_table[ind1][ind2] != '':
                    return self.distance_table[ind1][ind2]
                else:
                    return self.distance_table[ind2][ind1]
            else:
                print('Problem with index derivation')
                return None

    """
    Finds the index of the nearest package based on the current address.
    """

    def min_distance_from(self, address_currently_at, packages, address_list):
        """My big holdup is right here"""
        current_address_index = ls.list_search(address_list, address_currently_at)
        min_distance = 1000
        index_min_value = None
        for i in range(len(packages)):
            package_distance = self.distance_between(address_currently_at, packages[i].address,
                                                     starter_index=current_address_index)
            if float(package_distance) < float(min_distance):
                min_distance = package_distance
                index_min_value = i
        print(index_min_value, min_distance)
        return index_min_value, min_distance

    @staticmethod
    def distance_to_time(distance):
        return dt.timedelta(hours=distance / 18)

    def log_event(self, event):
        self.event_array.append([self.current_time, self.truck_label, event])

    def delivery_route(self):
        """The first action is being singled
        out in order to update all the packages
        status and to add to event log that the truck
        is departing"""
        print(self.current_location)
        if self.current_time == self.departure_time:
            for i in self.packages_on:
                i.depart(self.truck_label)
            self.log_event("Truck is departing from hub")

        print((self.current_location, len(self.packages_on), self.address_list))
        next_add_index, next_add_distance = self.min_distance_from(self.current_location, self.packages_on, self.address_list)
        self.destination = self.address_list[next_add_index]
        print(self.packages_delivered)
        self.current_time = dt.datetime.combine(dt.date.today(), self.departure_time) + self.distance_to_time(float(next_add_distance))
        for i in self.packages_on:
            if int(i.address_id) == int(next_add_index):
                self.log_event('Delivered Package %s to %s' % (str(i.pid), i.address))
                self.deliver_package(i)
        self.current_location = self.destination

        print((self.current_location, len(self.packages_on), self.address_list))
        next_add_index, next_add_distance = self.min_distance_from(self.current_location, self.packages_on, self.address_list)
        print(self.destination)
        self.destination = self.address_list[next_add_index]
        print(self.destination)
        self.current_time = dt.datetime.combine(dt.date.today(), self.departure_time) + self.distance_to_time(
            float(next_add_distance))
        for i in self.packages_on:
            if int(i.address_id) == int(next_add_index):
                self.log_event('Delivered Package %s to %s' % (str(i.pid), i.address))
                self.deliver_package(i)
        self.current_location = self.destination
        print(self.destination)
        print(self.packages_delivered)

        """
        while True:
            next_add_index, next_add_distance = self.min_distance_from(self.current_location, self.packages_on, self.address_list)
            print(next_add_distance)
            self.destination = self.address_list[next_add_index]
            print(self.destination)
            self.current_time = dt.datetime.combine(dt.date.today(), self.departure_time) + self.distance_to_time(float(next_add_distance))
            print(self.current_time)
            self.current_location = self.destination
            print(self.current_location)
            for i in self.packages_on:
                if int(i.address_id) == int(next_add_index):
                    self.log_event('Delivered Package %s to %s' % (str(i.pid), i.address))
                    self.deliver_package(i)
                    print(i)

            if len(self.packages_on)<1:
                break
            """
