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
        self.log.msg("GENERATE_CLIENTS_LIST", "clients_list was sucessfully generated. There are "+str(len(self.clients_list))+" new elements there.")
        return self.clients_list

class hive:

    def __init__(self, field, log):
        self.bees_list = {}
        self.global_extremum = {}
        self.field = field
        self.clients_list = dict(self.field.clients_list)
        self.log = log

    def set_scouting_area(self, bs_area_radius):
        try:
            client = next(iter(self.field.clients_list.values()))
        except Exception:
            self.log.msg("SET_SCOUTING_AREA", "There are no clients left in list")
            return False
        else:
            start_x = client[0] - bs_area_radius
            end_x = client[0] + bs_area_radius
            start_y = client[1] - bs_area_radius
            end_y = client[1] + bs_area_radius
            scouting_area = [[start_x, end_x], [start_y, end_y]]
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

    def set_bee_location(self, scouting_area):
        pass

    def get_clients_in_range(self):
        pass

    def compare_local_extremum(self):
        if self.local_extremum:
            pass

    def compare_global_extremum(self):
        if self.hive.global_extremum:
            pass

    def change_clients_list(self):
        pass
