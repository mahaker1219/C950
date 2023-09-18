import csv
from wgups_implementation.package import Package
from wgups_implementation.hash_table import ChainingHashTable

# Importing all packages from CSV
# CSV import code inspired by web lecture
# C950 - Webinar-2 - Getting Greedy, who moved my data?
# W-2_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Ref: zyBooks: 3.3.1: MakeChange greedy algorithm.
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

# Importing distance data and addresses from the distance table csv
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

