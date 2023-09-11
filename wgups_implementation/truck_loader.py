from wgups_implementation.truck import DeliveryTruck
from wgups_implementation.list_search import list_search


def load_packages_to_truck(packages, address_list, distance_table_list):
    truck_capacity = 16
    departure_time1 = 8
    departure_time2 = 0
    departure_time3 = 0
    truck1 = DeliveryTruck(1, departure_time1, address_list, distance_table_list)
    truck2 = DeliveryTruck(2, departure_time2, address_list, distance_table_list)
    truck3 = DeliveryTruck(3, departure_time3, address_list, distance_table_list)
    trucks = [truck1, truck2, truck3]
    special_instructions_array = []
    deadline_array = []
    no_action_array = []
    follow = []
    hub_packages = []
    """This is in order to have all package id's in the 'hub' array"""
    for i in range(1, packages.packages_count + 1):
        hub_packages.append(int(i))
    """I want it to go through every package in the package list"""
    for i in range(1, packages.packages_count + 1):
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
                """This module is for the packages that are to be on the same delivery truck as others"""
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
                truck3.address_id_array.append(package.address_id)
            elif package.special_notes[0] == 'd':
                truck2.load_package(package)
                hub_packages.remove(int(package.pid))
                truck2.address_id_array.append(package.address_id)
            else:
                print('Invalid input in special instructions field')
        elif package.delivery_deadline != 'EOD':
            if list_search(hub_packages, package.pid) is not None:
                truck1.load_package(package)
                hub_packages.remove(int(package.pid))
                truck1.address_id_array.append(package.address_id)
            deadline_array.append(package)
        else:
            no_action_array.append(package)

    """This part is to ensure that it is pulling the all packages
    that are going to the same address"""
    for i in hub_packages:
        package = packages.search(i)
        if list_search(truck1.address_id_array, package.address_id) is not None:
            if len(truck1.packages_on) < 16:
                hub_packages.remove(int(package.pid))
                truck1.load_package(package)
            else:
                hub_packages.remove(package.pid)
                truck3.load_package(package)
                truck3.address_id_array.append(package.address_id)
        if list_search(truck2.address_id_array, package.address_id) is not None:
            truck2.load_package(package)
            hub_packages.remove(int(package.pid))

        if list_search(truck3.address_id_array, package.address_id) is not None:
            if list_search(hub_packages, package.pid):
                hub_packages.remove(package.pid)
                truck3.load_package(package)

    for i in hub_packages:
        package = packages.search(i)
        truck3.load_package(package)

    """
    This is the consoling module in order to 
    see if data is moving as expected
    """
    """
    print('truck1', len(truck1.packages_on))
    for i in truck1.packages_on:
        print(i)
    print('truck2', len(truck2.packages_on))
    for i in truck2.packages_on:
        print(i)
    print('truck3', len(truck3.packages_on))
    for i in truck3.packages_on:
        print(i)
    """
    return trucks
