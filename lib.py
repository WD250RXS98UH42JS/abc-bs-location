import os
import sys
import random
from datetime import datetime, time

class log:
    """
    Class 'logs' manages any events occured during program execution.
    """

    def __init__(self, log_file):
        # Get current time and set it as program starting time
        self.start_time = datetime.now()
        # Get full path to log file (including it's name)
        self.log_file = log_file
        # Get log filepath without name
        self.log_file_path = log_file.rsplit("/", 1)[0]
        # Get log filename
        self.log_file_name = log_file.rsplit("/", 1)[1]

        # Check if log directory already exists
        if not os.path.isdir('./'+self.log_file_path):
            # If not, try to create
            try:
                os.mkdir(self.log_file_path)
            # In case of failing show err msg and exit
            except OSError:
                print ("ERR: Log directory creation failed: '%s'" % self.log_file_path)
                sys.exit(1)

    """Collects log data, converts it to human-readable string, prints it and saves to 
    predefined file.
    
    Returns:
        nothing
    """
    def __execute_log_data(self, log_type, object, message):
        # Get current time
        current_time = datetime.now()
        # Calculate seconds left during program running
        seconds_left = (current_time - self.start_time).seconds
        # Generate human-readable string
        log_msg = log_type + "\t" + \
                  str(current_time) + "\t" + \
                  object + "\t" + \
                  message + "\t" + \
                  " Seconds passed in total: " + str(seconds_left) + "\n"
        # Print log message
        print(log_msg)
        # Open log file in 'A+ (append)' mode and write log entry to it
        with open(self.log_file, 'a+') as file:
            file.write(log_msg)

    """msg(), warn(), err() methods
    
    It's wrappers defined for calling log-related functions. You can pass log data in this ways:
    Message:
    log.msg("<object>", "<log message>")
    Warning:
    log.warn("<object>", "<log message>")
    Error:
    log.err("<object>", "<log message>")

    Returns:
        nothing
    """
    def msg(self, object, message):
        # Shows log type
        log_type = "MSG"
        # Return __execute_log_data() execution as result
        return self.__execute_log_data(log_type, object, message)

    def warn(self, object, message):
        # Shows log type
        log_type = "WARN"
        # Return __execute_log_data() execution as result
        return self.__execute_log_data(log_type, object, message)

    def err(self, object, message):
        # Shows log type
        log_type = "ERR"
        # Return __execute_log_data() execution as result
        return self.__execute_log_data(log_type, object, message)

class field:
    """
    Class 'field' represents the whole area that able to locate clients. This area is rectangle
    with coords defined in run.py as that variables:
    start_width_pos - X-coord of starting point (left-bottom corner of field)
    start_height_pos - Y-coord of starting point (left-bottom corner of field)
    field_height - field height started from start_height_pos (on Y axle)
    field_width - field width started from start_width_pos (on X axle)
    """

    def __init__(self, width, height, start_width_pos, start_height_pos, log):
        # Field width
        self.width = width
        # Field height
        self.height = height
        # Field width start point coord
        self.start_width_pos = start_width_pos
        # Field height start point coord
        self.start_height_pos = start_height_pos
        # Clients list variable definition
        self.clients_list = {}
        # Log
        self.log = log

    """
    Takes clients count and generates clients_list with random coords that satisfy requirements
    such as field size.
    
    Returns:
        dict -- clients_list represented as dict
        Example:
        clients_list = {
            1: [83948, 44689],
            2: [49716, 94697],
            ...
            N: [60028, 72876]
        }
    """
    def generate_clients_list(self, clients_count):
        # Iterate over clients count to generate them all
        for i in range(clients_count):
            # Set random generated X-coord for current client
            x = random.randint(self.start_width_pos, self.width)
            # Set random generated Y-coord for current client
            y = random.randint(self.start_height_pos, self.height)
            # Add coords to clients_list as new client
            self.clients_list[i] = [x, y]
        # Create log entry
        self.log.msg("GENERATE_CLIENTS_LIST", "clients_list was successfully generated. There are "+str(len(self.clients_list))+" new elements there.")
        return self.clients_list

class hive:

    def __init__(self, field, bs_max_clients_count, bs_area_radius, log):
        self.bs_locations_list = {}
        self.global_extremum = {}
        self.field = field
        self.clients_list = dict(self.field.clients_list)
        self.bs_max_clients_count = bs_max_clients_count
        self.bs_area_radius = bs_area_radius
        self.log = log

    def set_scouting_area(self, bs_area_radius):
        try:
            client = next(iter(self.clients_list.values()))
        except Exception:
            self.log.msg("SET_SCOUTING_AREA", "There are no clients left in list")
            return False
        else:
            start_x = client[0] - bs_area_radius
            end_x = client[0] + bs_area_radius
            start_y = client[1] - bs_area_radius
            end_y = client[1] + bs_area_radius
            # scouting_area = [[start_x, end_x], [start_y, end_y]]
            scouting_area = {
                "start_x" : start_x,
                "end_x" : end_x,
                "start_y" : start_y,
                "end_y" : end_y
            }
            self.log.msg("SET_SCOUTING_AREA", "New scouting area was created: "+str(scouting_area))
            return scouting_area

    def modify_clients_list(self, element):
        key = list(element.keys())[0]
        if key in self.clients_list:
            del self.clients_list[key]

class bee:

    def __init__(self, hive, log):
        self.hive = hive
        self.log = log
        self.local_extremum = {}
        self.clients_in_area_list = {}
        self.location = []

    def scout(self, scouting_area):
        if not self.local_extremum and not self.hive.global_extremum:
            self.location = self.set_new_location(scouting_area)
            self.log.msg("scout".upper(), "location: " + str(self.location))
            self.clients_in_area_list = {}
            self.get_clients_in_area(self.location)
            self.log.msg("scout".upper(), "clients_in_area: " + str(self.clients_in_area_list))
            clients_in_area = len(self.clients_in_area_list)
            self.log.msg("scout".upper(), "clients_in_area count: " + str(clients_in_area))
            self.set_local_extremum(self.location, clients_in_area)
            self.set_global_extremum(self.local_extremum)
            self.log.msg("scout".upper(), "new_local_extremum: " + str(self.local_extremum))
            self.log.msg("scout".upper(), "new_global_extremum: " + str(self.hive.global_extremum)+ "\n\n")
        else:
            # self.location = self.set_new_location(self.hive.global_extremum)
            self.location = self.set_new_location(scouting_area)

            self.log.msg("scout".upper(), "location: " + str(self.location))
            self.clients_in_area_list = {}
            self.get_clients_in_area(self.location)
            clients_in_area = len(self.clients_in_area_list)

            self.log.msg("scout".upper(), "clients_in_area: " + str(self.clients_in_area_list))
            self.log.msg("scout".upper(), "clients_in_area count: " + str(clients_in_area))
            self.log.msg("scout".upper(), "local_extremum: " + str(self.local_extremum))
            self.log.msg("scout".upper(), "global_extremum: " + str(self.hive.global_extremum))
            
            if self.local_extremum["clients_in_area"] < clients_in_area:
                self.set_local_extremum(self.location, clients_in_area)
                self.log.msg("scout".upper(), "new_local_extremum: " + str(self.local_extremum))
                if self.local_extremum["clients_in_area"] > self.hive.global_extremum["clients_in_area"]:
                    self.set_global_extremum(self.local_extremum)
                    self.log.msg("scout".upper(), "new_global_extremum: " + str(self.hive.global_extremum) + "\n\n")
        self.log.msg("scout".upper(), "\n############### END OF SCOUT ITERATION ###############\n")
        # return self.hive.global_extremum

    def set_local_extremum(self, location, clients_in_area):
        # self.local_extremum.clear()
        self.local_extremum["location"] = location
        self.local_extremum["clients_in_area"] = clients_in_area
        return self.local_extremum

    def set_global_extremum(self, local_extremum):
        # self.hive.global_extremum.clear()
        self.hive.global_extremum["location"] = local_extremum["location"]
        self.hive.global_extremum["clients_in_area"] = local_extremum["clients_in_area"]
        return self.hive.global_extremum

    def set_new_location(self, data):
        if len(data) == 4:
            x = random.randint(data["start_x"], data["end_x"])
            y = random.randint(data["start_y"], data["end_y"])
        elif len(data) == 2:
            center_point_x = data["location"][0]
            center_point_y = data["location"][1]
            radius = self.hive.bs_area_radius * 2
            x = random.randint(center_point_x - radius, center_point_x + radius)
            y = random.randint(center_point_y - radius, center_point_y + radius)
        new_location = [x,y]
        return new_location

    def get_clients_in_area(self, location):
        start_x = location[0] - self.hive.bs_area_radius
        end_x = location[0] + self.hive.bs_area_radius
        start_y = location[1] - self.hive.bs_area_radius
        end_y = location[1] + self.hive.bs_area_radius
        for key, value in self.hive.clients_list.items():
            self.log.msg("get_clients_in_area".upper(), "x: " + str(value[0]) + "; y: " + str(value[1]))
            if value[0] in range(start_x, end_x) and value[1] in range(start_y, end_y):
                self.clients_in_area_list[key] = value
                self.log.msg("get_clients_in_area".upper(), "client in area: " + str({key : value}))
        # return self.clients_in_area_list

    def set_bs_location(self, global_extremum):
        key = len(self.hive.bs_locations_list)
        value = global_extremum
        new_bs_location = {key : value}
        if value["clients_in_area"] > 0:
            self.hive.bs_locations_list.update(new_bs_location)
            self.log.msg("set_bs_location".upper(), "\n\nnew_bs_location: " + str(new_bs_location) + "\n\n")
        else:
            self.log.msg("set_bs_location".upper(), "\n\nnew_bs_location wasn't created due to 0 clients around.\n\n")

    def change_clients_list(self):
        pass
