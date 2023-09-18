import csv
from wgups_implementation.package import Package
from wgups_implementation.hash_table import ChainingHashTable


def load_packages(filename):
    hash_t = ChainingHashTable()
    initial_state = []
    with open(filename) as package_list:
        package_data = csv.reader(package_list, delimiter=',')
        next(package_data)
        for p in package_data:
            pid = int(p[0])
            address = p[1]
            city = p[2]
            state = p[3]
            zip_code = p[4]
            delivery_deadline = p[5]
            weight = int(p[6])
            if p[7]:
                special_notes = p[7]
            else:
                special_notes = ''

            package_object = Package(pid, address, city, state, zip_code, delivery_deadline, weight,
                                     special_notes)
            package_object_init = Package(pid, address, city, state, zip_code, delivery_deadline, weight,
                                     special_notes)
            initial_state.append(package_object_init)
            hash_t.insert(pid, package_object)
    return hash_t, initial_state


"""
Loads distance data from CSV and prepares the address and distance tables.
"""


def load_distances(filename):
    counter = 0
    distance_table_list = [
        ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ]]
    with open(filename) as distances:
        data = csv.reader(distances, delimiter=',')
        for a in data:
            if counter == 0:
                address_list = a
                address_list.pop(0)
                for i in range(len(address_list)):
                    address_list[i] = address_list[i][1:]
                counter += 1
            else:
                distance_table_list.append(a[1:])
                counter += 1
    return address_list, distance_table_list

