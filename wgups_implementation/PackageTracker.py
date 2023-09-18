# I know the initial state being a completely separate list seems redundant, but I am doing this in order to prevent
# generating the event array doesn't interfere with the user console
from datetime import time
from wgups_implementation.hash_table import ChainingHashTable
from wgups_implementation.package import Package


class PackageTracker:
    """This is created for state tracking, so it's easy for user console to calculate based off times"""
    def __init__(self, event_log, packages):
        self.event_log = event_log
        self.state = packages
        self.state_storage = ChainingHashTable()
        self.packages_count = len(self.state)

    def list_states_cached(self):
        return self.state_storage.get_all_keys()

    def __str__(self):
        r_string = "Package Tracker"
        for i in self.state:
            r_string += "\n" + str(i)
        return r_string

    def new_package_state(self, package_id):
        """Seems redundant but if I reuse a pointer, it will go based off last change, which defeats the purpose of
        state based rendering"""
        data = self.state[int(package_id) - 1]
        pid = data.pid
        address = data.address
        city = data.city
        state = data.state
        zip_code = data.zip_code
        delivery_deadline = data.delivery_deadline
        weight = data.weight
        special_notes = data.special_notes
        return Package(pid, address, city, state, zip_code, delivery_deadline, weight,
                       special_notes)

    @staticmethod
    def input_time_conversion(input_time):
        """Makes it easier to compare datetime objs by converting user input"""
        hours, minutes = map(int, input_time.split(':'))
        return time(hours, minutes)

    def retrieve_state_time_package(self, input_time, package):
        """It may be easier to just use the already baked in state functionality for this, but I'm looking to turn
        this in ASAP, may tweak in future to use at part of my personal coding portfolio (link-based sharing only so
        nobody can plagiarize)"""
        target_time = self.input_time_conversion(input_time)
        copy_package = self.new_package_state(int(package))
        for event in self.event_log:
            event_time = event[1]
            if event_time <= target_time and package == event[2]:
                if event[3] == 'Load':
                    copy_package.load(event[-1])
                    print('load')
                if event[3] == 'Depart':
                    copy_package.depart(event[-1])
                    print('depart')
                if event[3] == 'Deliver':
                    copy_package.deliver(event[1], event[-1])
                    print('deliver')
        return copy_package

    def retrieve_state_time_all(self, input_time):
        """See all package status at a certain point"""
        target_time = self.input_time_conversion(input_time)
        created_states = self.state_storage.get_all_keys()
        print(created_states)
        # This is all to check if the state has already been calculated or pull from the most recent state before the
        # input time

        if len(created_states) >= 1:
            starting_state_time = self.event_log[0][1]
            for i in range(len(created_states)):
                # Within the list, looking to find the state with the closest time to target time
                if created_states[i] == target_time:
                    starting_state_time = created_states[i]
                    starting_state = self.state_storage.search(starting_state_time)
                elif target_time > created_states[i] > starting_state_time:
                    starting_state_time = created_states[i]
                    starting_state = self.state_storage.search(starting_state_time)
                else:
                    starting_state = []
                    starting_state_time = self.event_log[0][1]
                    for pid in range(1, self.packages_count + 1):
                        starting_state.append(self.new_package_state(pid))
        else:
            starting_state = []
            starting_state_time = self.event_log[0][1]
            for pid in range(1, self.packages_count + 1):
                starting_state.append(self.new_package_state(pid))

        # this will generate time-based states
        for event in self.event_log:
            if target_time > event[1] >= starting_state_time:

                # This length check is in place in order to account for events that are not package specific
                if event[2] is not None:
                    iter_p = starting_state[event[2] - 1]
                    if event[3] == 'Load':
                        iter_p.load(event[-1])
                    if event[3] == 'Depart':
                        iter_p.depart(event[-1])
                    if event[3] == 'Deliver':
                        iter_p.deliver(event[1], event[-1])
        self.state_storage.insert(target_time, starting_state)
        r_string = "Package Tracker"
        for i in starting_state:
            r_string += "\n" + str(i)
        return r_string
