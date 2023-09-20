# Marshall Haker WGU Student ID: 003935083
from wgups_implementation.data_loader import load_packages, load_distances
from wgups_implementation.truck_loader import load_packages_to_truck
from wgups_implementation.merge import merge_three
from wgups_implementation.PackageTracker import PackageTracker


def address_id_filler(input_address_list, package_table, packages_amount):
    testing_list = []
    for i in range(1, packages_amount + 1):
        p = package_table.search(i)
        for n in range(len(input_address_list)):
            if p.address == input_address_list[n]:
                testing_list.append(True)
                p.address_id = n
                break
            else:
                testing_list.append(False)
    return testing_list


# Initialize the package table
package_table, initial_state = load_packages('supporting_documentation/packageFile.csv')
# Load distance data
address_list, distance_table_list = load_distances('supporting_documentation/WGUPS_distance_table.csv')
address_id_filler(address_list, package_table, package_table.packages_count)
trucks = load_packages_to_truck(package_table, address_list, distance_table_list)

total_mileage = 0
trucks_event_log = []
for i in trucks:
    trucks_event_log.append(i.delivery_route())
    total_mileage += i.mileage_traveled
total_event_log = merge_three(trucks_event_log[0], trucks_event_log[1], trucks_event_log[2])
p_tracker = PackageTracker(total_event_log, initial_state)
# Console application loop
welcome_message = ("Welcome to WGUPS Implementation\n1. See Total Mileage\n2. See Final Package Status\n3. See All "
                   "Package Status By Time\n4. See Single Package Status By Time\n5. See All Events\n6. List All "
                   "States Cached Within PackageTracking Object\n7. See Number Of Packages Per Truck\n8.Exit Program")

while True:
    print(welcome_message)
    user_input = input("Select option by number: ")
    if user_input == '1':
        print("Total mileage for all trucks is " + str(total_mileage))
    elif user_input == '2':
        print(p_tracker.retrieve_state_time_all('23:00'))
    elif user_input == '3':
        user_time = input("Please type in time in following format HH:MM: ")
        print(p_tracker.retrieve_state_time_all(user_time))
    elif user_input == '4':
        user_time = input("Please type in time in following format HH:MM: ")
        user_package = input("Please type in package by id number: ")
        print(p_tracker.retrieve_state_time_package(user_time, user_package))
    elif user_input == '5':
        for event in total_event_log:
            print(event[0])
    elif user_input == '6':
        print(p_tracker.list_states_cached())
    elif user_input == '7':
        print('Number of packages on truck 1: ' + str(len(trucks[0].packages_delivered)))
        print('Number of packages on truck 2: ' + str(len(trucks[1].packages_delivered)))
        print('Number of packages on truck 3: ' + str(len(trucks[2].packages_delivered)))
    elif user_input == '8':
        print("Thank you for your time!")
        break
    else:
        print('Invalid input detected')
