import pytest
from wgups_implementation.truck import DeliveryTruck
from wgups_implementation.data_loader import load_packages, load_distances


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

    def test_distance_between(self, initialization):
        """Ensure the distance between two points is calculated correctly"""
        package_list, address_list, distance_table, truck = initialization
        print(3)

    '''
    def test_min_distance_from(self):
        """Ensure the minimum distance from a point to a list of points is calculated correctly"""
        # Your test code for calculating the minimum distance goes here
        print(4)

    def test_delivery_route(self):
        """Ensure the delivery route is generated correctly"""
        # Your test code for generating a delivery route goes here
        print(5)
'''
