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
                print(len(a[1:]))
                counter += 1
    print(len(distance_table_list[0]))
    return address_list, distance_table_list


init_package_table = hash_table.ChainingHashTable()

load_package('supporting_documentation/packageFile.csv', init_package_table)

address_list, distance_table_list = load_distances('supporting_documentation/WGUPS_distance_table.csv')


# This while statement serves mostly for the console application
while True:
    break
