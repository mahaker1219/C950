"""Serves as the class for every individual package"""
import datetime


class Package:
    # Constructor to pull all needed values from csv
    def __init__(self, pid, address, city, state, zip_code, delivery_deadline, weight, special_notes=''):
        def derive_special_notes():
            if self.special_notes != '':
                print('special note true')
                spec = str(self.special_notes)
                if spec[0] == 't':
                    self.truck_preference = spec[1]
                    print('truck preference')

                elif spec[0] == 'w':
                    output_array = []
                    active_number = ""
                    for i in spec[1:]:
                        if i == ",":
                            output_array.append(int(active_number))
                            active_number = ""
                        else:
                            active_number += i
                    print('Following ' + str(output_array))
                    self.follow = output_array

                elif spec[0] == 'i':
                    print('incorrect address')
                    self.hold = True

                elif spec[0] == 'd':
                    self.hold = True
                    self.hold_time = datetime.datetime.strptime(spec[1:], '%H:%M').time()
                    print('Delayed until: ' + str(self.hold_time))

        self.pid = pid
        self.address = "%s, %s, %s %s" % (address, city, state, zip_code)
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.hold = False
        self.hold_time = datetime.time(0, 0, 0, )
        self.status = 'at the hub'
        self.delivery_time = datetime.time(0, 0, 0)
        self.truck_preference = 0
        self.follow = []
        derive_special_notes()

    def update_address(self, new_address):
        if self.special_notes != '':
            if self.special_notes[0] == 'i':
                self.address = new_address

    def load(self, truck):
        self.status = "en route on truck " + str(truck)

    def deliver(self, time):
        self.status = "Delivered"
        self.delivery_time = datetime.datetime.strptime(time, '%H:%M:%S').time()

    def __str__(self):
        return ("%s, %s, Delivery Deadline: %s Weight: %s, %s, Hold: %s, Hold Time: %s, "
                "Status: %s, Delivery Time: %s" % (
                    self.pid, self.address, self.delivery_deadline, self.weight,
                    self.special_notes, self.hold, self.hold_time, self.status, self.delivery_time
                ))



