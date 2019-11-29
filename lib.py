import os
import sys
import random
import math
from datetime import datetime, time

class log:
    """
    Class 'logs' manages any events occured during program execution.
    """

    def __init__(self, log_file, verbose):
        # Get current time and set it as program starting time
        self.start_time = datetime.now()
        # Get full path to log file (including it's name)
        self.log_file = log_file
        # Get log filepath without name
        self.log_file_path = log_file.rsplit("/", 1)[0]
        # Get log filename
        self.log_file_name = log_file.rsplit("/", 1)[1]
        self.verbose = verbose

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
        # Check log verbosity level
        if (self.verbose == 0 and log_type == "STAT") or \
        (self.verbose == 1 and log_type in ["STAT", "ERR", "WARN"]) or \
        (self.verbose == 2):
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

    def stat(self, object, message):
        # Shows log type
        log_type = "STAT"
        # Return __execute_log_data() execution as result
        return self.__execute_log_data(log_type, object, message)

class field:

    def __init__(self, width, height, log):
        self.width = width
        self.height = height
        self.clients_list = {}
        self.log = log

    def create_clients_list(self, clients_count, clients_list):
        if clients_list == []:
            for i in range(clients_count):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                self.clients_list[i] = [x, y]
            self.log.msg("GENERATE_CLIENTS_LIST", "clients_list was successfully generated. There are "+str(len(self.clients_list))+" new elements there.")
        else:
            for i in range(len(clients_list)):
                self.clients_list[i] = clients_list[i]
            self.log.msg("GENERATE_CLIENTS_LIST", "clients_list was successfully pulled from configuration. There are "+str(len(self.clients_list))+" elements there.")
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

    def set_scouting_area(self, field, bs_area_radius):
        scouting_area = {
            "type" : "scouting_area",
            "area_width" : field.width,
            "area_height" : field.height
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
        self.log.msg("scout".upper(), "\n### START OF SCOUT ITERATION ###\n")
        if self.hive.global_extremum == {}:
            self.location = self.set_new_location(scouting_area)
        else:
            self.location = self.set_new_location(self.hive.global_extremum)
        # self.clients_in_area_list = {}
        self.get_clients_in_area(self.location)
        clients_in_area = len(self.clients_in_area_list)

        self.log.msg("scout".upper(), "location: " + str(self.location))
        self.log.msg("scout".upper(), "clients_in_area: " + str(self.clients_in_area_list))
        self.log.msg("scout".upper(), "clients_in_area count: " + str(clients_in_area))
        self.log.msg("scout".upper(), "local_extremum: " + str(self.local_extremum))
        self.log.msg("scout".upper(), "global_extremum: " + str(self.hive.global_extremum))

        if self.local_extremum == {}:
            self.set_local_extremum(self.location, self.clients_in_area_list)
            self.log.msg("scout".upper(), "new_local_extremum: " + str(self.local_extremum))
        if self.hive.global_extremum == {}:
            self.set_global_extremum(self.local_extremum)
            self.log.msg("scout".upper(), "new_global_extremum: " + str(self.hive.global_extremum))

        if self.local_extremum["clients_in_area"] < clients_in_area:
            self.set_local_extremum(self.location, self.clients_in_area_list)
            self.log.msg("scout".upper(), "new_local_extremum: " + str(self.local_extremum))
        if self.local_extremum["clients_in_area"] > self.hive.global_extremum["clients_in_area"]:
            self.set_global_extremum(self.local_extremum)
            self.log.msg("scout".upper(), "new_global_extremum: " + str(self.hive.global_extremum))

        self.log.msg("scout".upper(), "\n### END OF SCOUT ITERATION ###\n")
        return self.hive.global_extremum

    def set_local_extremum(self, location, clients_in_area_list):
        self.local_extremum["type"] = "local_extremum"
        self.local_extremum["location"] = location
        self.local_extremum["clients_in_area"] = len(clients_in_area_list)
        self.local_extremum["clients_in_area_list"] = clients_in_area_list
        return self.local_extremum

    def set_global_extremum(self, local_extremum):
        self.hive.global_extremum = local_extremum
        self.hive.global_extremum["type"] = "global_extremum"
        return self.hive.global_extremum

    def set_new_location(self, data):
        if data["type"] == "scouting_area":
            from_x = 0
            to_x = data["area_width"]
            from_y = 0
            to_y = data["area_height"]
        # if data["type"] == "global_extremum":
        else:
            radius = self.hive.bs_area_radius * 2
            from_x = data["location"]["x"] - radius
            if from_x < 0:
                from_x = 0
            to_x = data["location"]["x"] + radius
            if to_x > self.hive.field.width:
                to_x = self.hive.field.width
            from_y = data["location"]["y"] - radius
            if from_y < 0:
                from_y = 0
            to_y = data["location"]["y"] + radius
            if to_y > self.hive.field.height:
                to_y = self.hive.field.height

        x = random.randint(from_x, to_x)
        y = random.randint(from_y, to_y)

        new_location = {"x": x, "y": y}
        return new_location

    def get_clients_in_area(self, location):
        self.clients_in_area_list = {}
        for key, value in self.hive.clients_list.items():
            x1 = int(location["x"])
            x2 = int(value[0])
            y1 = int(location["y"])
            y2 = int(value[1])
            range_to_client = math.sqrt(abs((x1 - x2)**2 + (y1 - y2)**2))
            if range_to_client <= self.hive.bs_area_radius:
                self.clients_in_area_list[key] = value
        return self.clients_in_area_list

    def set_bs_location(self, global_extremum):
        key = len(self.hive.bs_locations_list)
        global_extremum["type"] = "bs"
        value = global_extremum
        new_bs_location = {key : value}
        if global_extremum["clients_in_area"] > 0:
            self.hive.bs_locations_list.update(new_bs_location)
            self.log.msg("set_bs_location".upper(), "new_bs_location: " + str(new_bs_location) + "")
            self.log.stat("set_bs_location".upper(), "New BS location: " + str(value["location"]) + ", clients in area: " + str(value["clients_in_area"]))
        else:
            self.log.stat("set_bs_location".upper(), "New BS wasn't created due to 0 clients around.")
