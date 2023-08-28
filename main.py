"""This is going to serve as the entry point for the program

I think the best way to handle the log would be through tracking state changes.
Essentially, there would be an initial state at beginning of day,
then every important event would be logged to array. There would be corresponding array
with times of everything. The thought process behind this is that
in terms of use, it would be annoying in memory to keep the
complete list of package status for every 5 mins. There would be a low
 usage rate of complete status call. I would cache results in a  hash table though then
 have it start at state of closest but lower complete log then use the state
 change log up until that point"""
import hash_table
import package
import csv
import truck
import math
"""This will be where I initialize the csvs and objects in order for the algo to begin"""


def load_package(filename, hash_t):
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

            package_object = package.Package(pid, address, city, state, zip_code, delivery_deadline, weight,
                                             special_notes)

            hash_t.insert(pid, package_object)


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


init_package_table = hash_table.ChainingHashTable()

load_package('supporting_documentation/packageFile.csv', init_package_table)

address_list, distance_table_list = load_distances('supporting_documentation/WGUPS_distance_table.csv')

"""This will take a list and a term and return the index of the list that
the term is found"""


def list_search(list, term):
    for i in range(len(list)):
        if list[i] == term:
            return i
    return None


def distance_between(address1, address2, distance_table=distance_table_list, address_list=address_list,
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


def address_id_filler(address_list, package_table, packages_amount):
    testing_list = []
    for i in range(1, packages_amount + 1):
        p = package_table.search(i)
        for n in range(len(address_list)):
            if p.address == address_list[n]:
                testing_list.append(True)
                p.address_id = n
                break
            else:
                testing_list.append(False)
    return testing_list


def load_packages(packages, address_list=address_list, distance_table_list=distance_table_list):
    truck_capacity = 16
    departure_time1 = 0
    departure_time2 = 0
    departure_time3 = 0
    truck1 = truck.DeliveryTruck(1, departure_time1)
    truck2 = truck.DeliveryTruck(2, departure_time2)
    truck3 = truck.DeliveryTruck(3, departure_time3)
    trucks = [truck1, truck2, truck3]
    special_instructions_array = []
    deadline_array = []
    no_action_array = []
    follow = []
    hub_packages = []
    """This is in order to have all package id's in the 'hub' array"""
    for i in range(1, packages.packages_count):
        hub_packages.append(i)
    """I want it to go through every package in the package list"""
    for i in range(1, packages.packages_count):
        package = packages.search(i)
        if package.special_notes_exists:
            special_instructions_array.append(package)
            """The instructions state only truck 2 will be
            designated for the specific truck instruction
            but I would like for it to be expandable.
            I'm only addressing the truck and with 
            categories because the incorrect address
            and delayed categories end up putting 
            the package on hold status"""
            if package.special_notes[0] == 't':
                """This is ensuring that the package is still 
                in the hub to avoid double loading"""
                if list_search(hub_packages, package.pid):
                    hub_packages.remove(package.pid)
                    truck_number = int(package.special_notes[1])
                    truck_for_loading = trucks[truck_number - 1]
                    truck_for_loading.load_package(package)
                    truck_for_loading.address_id_array.append(package.address_id)

            elif package.special_notes[0] == 'w':
                intermediate_string = ''
                for ii in package.special_notes[1:]:
                    if ii == ' ':
                        continue
                    elif ii == ',':
                        follow.append(intermediate_string)
                        intermediate_string = ''
                    else:
                        intermediate_string = intermediate_string + str(ii)
                if list_search(hub_packages, package.pid):
                    hub_packages.remove(package.pid)
                    truck1.load_package(package)
                    truck1.address_id_array.append(package.address_id)
                for ii in follow:
                    if list_search(hub_packages, int(ii)):
                        additional_package = packages.search(int(ii))
                        truck1.load_package(additional_package)
                        hub_packages.remove(int(ii))
                        truck1.address_id_array.append(additional_package.address_id)
            elif package.special_notes[0] == 'i':
                truck3.load_package(package)
                hub_packages.remove(int(package.pid))
                truck3.address_id_array.append(package.pid)
            elif package.special_notes[0] == 'd':
                truck2.load_package(package)
                hub_packages.remove(int(package.pid))
                truck2.address_id_array.append(package.pid)
            else:
                print('Invalid input in special instructions field')
        elif package.delivery_deadline != 'EOD':
            if list_search(hub_packages, package.pid):
                print('TAKING CARE OF'+str(package.pid))
                truck1.load_package(package)
                hub_packages.remove(int(package.pid))
                truck1.address_id_array.append(package.pid)
            deadline_array.append(package)
        else:
            no_action_array.append(package)

    """This part is to ensure that it is pulling the all packages
    that are going to the same address"""
    for i in hub_packages:
        package = packages.search(i)
        if list_search(truck1.address_id_array, package.address_id):
            hub_packages.remove(package.pid)
            truck1.load_package(package)
        if list_search(truck2.address_id_array, package.address_id):
            hub_packages.remove(package.pid)
            truck2.load_package(package)
        if list_search(truck3.address_id_array, package.address_id):
            hub_packages.remove(package.pid)
            truck3.load_package(package)

    """This is the consoling module in order to 
    see if data is moving as expected"""
    print('truck1',len(truck1.packages_on))
    for i in truck1.packages_on:
        print(i)
    print(truck1.address_id_array)
    print('truck2',len(truck2.packages_on))
    for i in truck2.packages_on:
        print(i)
    print(truck2.address_id_array)
    print('truck3',len(truck3.packages_on))
    for i in truck3.packages_on:
        print(i)
    print(truck3.address_id_array)
    print(hub_packages)
    for i in deadline_array:
        print(i)

address_id_filler(address_list, init_package_table, init_package_table.packages_count)
load_packages(init_package_table)

# This while statement serves mostly for the console application
while True:
    break
