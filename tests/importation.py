from wgups_implementation.truck import DeliveryTruck
from wgups_implementation.data_loader import load_packages, load_distances

package_list = load_packages("../supporting_documentation/packageFile.csv")
address_list, distance_table = load_distances("../supporting_documentation/WGUPS_distance_table.csv")
truck = DeliveryTruck(1, 8, address_list, distance_table)

print(truck)