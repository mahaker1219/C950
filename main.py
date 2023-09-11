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
from wgups_implementation import hash_table
from wgups_implementation.data_loader import load_packages, load_distances
from wgups_implementation.truck_loader import load_packages_to_truck

"""
This will be where I initialize the csvs and objects in order for the algo to begin
"""

"""This will take a list and a term and return the index of the list that
the term is found"""

"""
Calculates the distance between two addresses using the distance_table.
"""

"""
Fills the address_id field in the package_table based on address_list.
"""


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


"""
Loads packages onto trucks based on special instructions, deadlines, and addresses.
"""

"""This is going to input the 3 loaded trucks and output an ordered array of events"""

# Initialize the package table
init_package_table = hash_table.ChainingHashTable()
package_table = load_packages('supporting_documentation/packageFile.csv')

# Load distance data
address_list, distance_table_list = load_distances('supporting_documentation/WGUPS_distance_table.csv')
address_id_filler(address_list, package_table, init_package_table.packages_count)
trucks = load_packages_to_truck(package_table, address_list, distance_table_list)

truck1 = trucks[0]
truck1.delivery_route()
# Console application loop
while True:
    break
