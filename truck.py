""""""
import package
import datetime

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
        self.event_array = []

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

    def distance_between(address1, address2, distance_table, address_list,
                         starter_index=None):
        if starter_index is None:
            ind1 = None
            ind2 = None
            if list_search(address_list, address1) is not None:
                ind1 = list_search(address_list, address1)
            if list_search(address_list, address2) is not None:
                ind2 = list_search(address_list, address2)
            if ind1 is not None and ind2 is not None:
                if distance_table[ind1][ind2] != '':
                    return distance_table[ind1][ind2]
                else:
                    return distance_table[ind2][ind1]
            else:
                print('Problem with index derivation')
                return None
        else:
            ind1 = starter_index
            ind2 = None
            if list_search(address_list, address2) is not None:
                ind2 = list_search(address_list, address2)
            if ind1 is not None and ind2 is not None:
                if distance_table[ind1][ind2] != '':
                    return distance_table[ind1][ind2]
                else:
                    return distance_table[ind2][ind1]
            else:
                print('Problem with index derivation')
                return None

    """
    Finds the index of the nearest package based on the current address.
    """

    def min_distance_from(address_currently_at, packages):
        current_address_index = list_search(packages, address_currently_at)
        min_distance = 1000
        index_min_value = None
        for i in range(len(packages)):
            package_distance = distance_between(address_currently_at, packages[i], starter_index=current_address_index)
            if package_distance << min_distance:
                min_distance = package_distance
                index_min_value = i
        return index_min_value, min_distance