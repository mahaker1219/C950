"""Serves as the class for every individual package"""
import datetime
from wgups_implementation.list_search import list_search

class Package:
    # Constructor to pull all needed values from csv
    def __init__(self, pid, address, city, state, zip_code, delivery_deadline, weight, special_notes=''):
        def derive_special_notes():
            if self.special_notes != '':
                self.special_notes_exists = True
                spec = str(self.special_notes)
                if spec[0] == 't':
                    self.truck_preference = spec[1]

                elif spec[0] == 'w':
                    output_array = []
                    active_number = ""
                    for i in spec[1:]:
                        if i == ",":
                            output_array.append(int(active_number))
                            active_number = ""
                        else:
                            active_number += i
                    self.follow = output_array

                elif spec[0] == 'i':
                    self.hold = True

                elif spec[0] == 'd':
                    self.hold = True
                    self.hold_time = datetime.datetime.strptime(spec[1:], '%H:%M').time()
            else:
                self.special_notes_exists = False

        self.pid = pid
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.hold = False
        self.hold_time = datetime.time(0, 0, 0, )
        self.status = 'at the hub'
        self.delivery_time = datetime.time(0, 0, 0)
        self.truck_preference = 0
        self.follow = []
        self.address_id = None
        derive_special_notes()

    def update_address(self, new_address):
        if self.special_notes != '':
            if self.special_notes[0] == 'i':
                self.address = new_address

    def load(self, truck):
        self.status = "loaded on truck " + str(truck)

    def depart(self, truck):
        self.status = "en route on truck  " + str(truck)

    def deliver(self, time, truck):
        self.status = "Delivered by Truck "+str(truck)
        self.delivery_time = time

    def fill_address_id(self, address_list):
        self.address_id = list_search(address_list, self.address)

    def __str__(self):
        return ("%s, %s, Delivery Deadline: %s, Special Notes: %s, Status: %s, Delivery Time: %s " % (
                    self.pid, self.address, self.delivery_deadline,
                    self.special_notes, self.status, self.delivery_time.strftime("%H:%M:%S")
                ))
