import pytest
from wgups_implementation.truck import DeliveryTruck
from wgups_implementation.data_loader import load_packages, load_distances
from wgups_implementation.list_search import list_search


# This initialization will be used for multiple different tests to quickly use sample data
@pytest.fixture
def initialization():
    package_list = load_packages("../supporting_documentation/packageFile.csv")
    address_list, distance_table = load_distances("../supporting_documentation/WGUPS_distance_table.csv")
    truck = DeliveryTruck(1, 8, address_list, distance_table)
    return package_list, address_list, distance_table, truck


@pytest.fixture()
def loaded_truck(initialization):
    package_list, address_list, distance_table, truck = initialization
    for i in range(1, 11):
        truck.load_package(package_list.search(i))
    return truck


class TestDeliveryTruck:

    def test_load_package(self, initialization):
        """Ensure proper input type handling, the package status is updated, and the truck inventory (packages on and
        ) is updated"""
        package_list, address_list, distance_table, truck = initialization
        valid_package = package_list.search(3)
        initial_packages_length = len(truck.packages_on)
        truck.load_package(valid_package)
        # The following checks are for a valid input
        assert len(truck.packages_on) == initial_packages_length + 1
        assert valid_package in truck.packages_on
        assert valid_package.status == "loaded on truck " + str(truck.truck_label)
        # The following checks are for invalid input
        invalid_package = 7
        with pytest.raises(TypeError):
            truck.load_package(invalid_package)
        with pytest.raises(TypeError):
            truck.load_package(None)

        assert invalid_package not in truck.packages_on

    def test_deliver_package(self, initialization, loaded_truck):
        """Ensure the package is delivered, the package status is updated, and the truck inventory (packages on and
        packages delivered) is updated"""
        package_list, address_list, distance_table, truck = initialization
        loaded_truck = loaded_truck
        # checking the fixture properly loaded expected packages
        initial_length_on = len(loaded_truck.packages_on)
        initial_length_delivered = len(loaded_truck.packages_delivered)
        assert initial_length_on == 10
        assert initial_length_delivered == 0
        package_for_delivery = package_list.search(4)
        loaded_truck.deliver_package(package_for_delivery)
        # checking to see if truck's arrays were updated
        assert len(loaded_truck.packages_on) == initial_length_on - 1
        assert len(loaded_truck.packages_delivered) == initial_length_delivered + 1
        assert package_for_delivery not in loaded_truck.packages_on
        assert package_for_delivery in loaded_truck.packages_delivered
        # Ensure package's status has been updated
        assert package_for_delivery.status == "Delivered"
        # Checks for invalid input
        invalid_package = 7
        with pytest.raises(TypeError):
            truck.deliver_package(invalid_package)
        with pytest.raises(TypeError):
            truck.deliver_package(None)
        assert invalid_package not in truck.packages_on
        # Checks to make sure doesn't deliver a package that isn't on there
        unavailable_package = package_list.search(15)
        with pytest.raises(ValueError):
            truck.deliver_package(unavailable_package)
        assert unavailable_package not in truck.packages_delivered

    def test_fill_address_id_onboard(self, initialization, loaded_truck):
        address_list = initialization[1]
        loaded_truck = loaded_truck
        loaded_truck.fill_address_id_onboard()
        for package in loaded_truck.packages_on:
            assert package.address_id is not None
            package_address_id = list_search(address_list, package.address)
            assert package_address_id == package.address_id

    def test_distance_between(self, initialization, loaded_truck):
        """Ensure the distance between two points is calculated correctly"""
        loaded_truck = loaded_truck
        # Ensures return value for testing cases
        testing_combinations = [[1, 5], [8, 6], [3, 7], [0, 8], [5, 4]]
        for i in range(len(testing_combinations)):
            line = testing_combinations[i]
            p1 = loaded_truck.packages_on[line[0]]
            p2 = loaded_truck.packages_on[line[1]]
            distance_between = loaded_truck.distance_between(p1, package2=p2)
            assert distance_between is not None

        # Ensures table lookup is acting as expected
        assert loaded_truck.distance_between(loaded_truck.packages_on[0], loaded_truck.packages_on[1]) == 1.5

        # Ensures address id lookup operates correctly
        assert loaded_truck.distance_between(loaded_truck.packages_on[0], starter_index=2) == 2.8

        # Ensures properly handles invalid input
        invalid_package = 7
        with pytest.raises(TypeError):
            loaded_truck.distance_between(invalid_package, package2=loaded_truck.packages_on[8])

    def test_min_distance_from(self, initialization, loaded_truck):
        """Ensure the minimum distance from a point to a list of points is calculated correctly"""
        truck = loaded_truck
        address_list = initialization[1]

        # Ensures properly handles invalid input
        invalid_package_list = 85
        invalid_package_list2 = [5, 6, 7]
        invalid_address_list = 54
        invalid_address_list2 = [6, 7, 8]
        invalid_address = 'Not a legitimate address'
        invalid_address2 = 31
        with pytest.raises(TypeError):
            truck.min_distance_from(truck.current_location_id, invalid_package_list, address_list)
        with pytest.raises(TypeError):
            truck.min_distance_from(truck.current_location_id, invalid_package_list2, address_list)
        with pytest.raises(TypeError):
            truck.min_distance_from(truck.current_location_id, truck.packages_on, invalid_address_list)
        with pytest.raises(TypeError):
            truck.min_distance_from(truck.current_location_id, truck.packages_on, invalid_address_list2)
        with pytest.raises(TypeError):
            truck.min_distance_from(invalid_address, truck.packages_on, address_list)
        with pytest.raises(ValueError):
            truck.min_distance_from(invalid_address2, truck.packages_on, address_list)

        # Function should return the package that is the closest then the length in miles it is away
        assert truck.min_distance_from(truck.current_location_id, truck.packages_on, address_list)[0] == \
               truck.packages_on[1]
        assert truck.min_distance_from(truck.current_location_id, truck.packages_on, address_list)[1] == 2.8
