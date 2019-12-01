# -*- coding: utf-8 -*-
from lib import *

###
# Config section

# Log verbosity
# If 0, only "STAT" entries will be showed
# If 1, "STAT", "ERR" and "WARN" entries will be showed
# If 2, all entries will be showed
verbose = 0

# Count of bees per iteration
bees_count = 10

# Max scouting retries before finishing algorithm iteration 
max_retries_count = 10

# Number of clients located on field
clients_count = 50

# If [], clients list will be generated automatically
# If any values exists, they will become entries of clients list
clients_list = [
    # [15,15],
    # [14,14],
    # [14,15],
    # [1,1],
    # [2,2],
    # [2,1]
]

# Number of clients are possible to connect to single basic station
bs_max_clients_count = 100

# Basic station working area radius
bs_area_radius = 3

# Field width
field_width = 15

# Field height
field_height = 15

# Y-coord which field height starts with
start_height_pos = 0

# X-coord which field width starts with
start_width_pos = 0

# Relative path to log file (including filename)
log_file_path = "logs/log.txt"



###
# Logic section

# Initialize 'log' instance
log = log(log_file_path, verbose)

# Initialize 'field' instance
field = field(field_width, field_height, log)

# Generate 'clients_list' as part of 'field' instance
clients_list = field.create_clients_list(clients_count, clients_list)

# Initialize 'hive' instance
hive = hive(field, bs_max_clients_count, bs_area_radius, log)

### LOGGING
log.stat("run".upper(), "Program started. All instances initialized.")
log.stat("run".upper(), "There are " + str(len(hive.clients_list)) + " clients.")
log.msg("run".upper(), "clients_list:")
for key, value in hive.clients_list.items():
    log.msg("run".upper(), str(key)+" : "+str(value))
###

bees = [bee(hive, log) for i in range(bees_count)]
iter_count = 0
while len(hive.clients_list) > 0:
    log.stat("run".upper(), "### Iteration #"+ str(iter_count) +" started. ###")
    for bee in bees:
        bee.local_extremum = {}
        bee.location = []
    hive.global_extremum = {}
    scouting_area = hive.set_scouting_area(field, bs_area_radius)
    for _ in range(max_retries_count):
        for bee in bees:
            bee.scout(scouting_area)
    bee.set_bs_location(hive.global_extremum)
    for key, value in hive.global_extremum["clients_in_area_list"].items():
        hive.modify_clients_list({key: value})

    ### LOGGING
        log.msg("run".upper(), "deleted client from clients_list: " + str({key: value}))
    log.msg("run".upper(), "cleaned_clients_list items count: " + str(len(hive.clients_list)))
    log.stat("run".upper(), "### Iteration #"+ str(iter_count) +" ended. ###")
    ###

    iter_count += 1

### LOGGING
log.stat("RESULT", "############################################################")
log.stat("RESULT", "Program execution was finished.")
log.stat("RESULT", "List of basic stations locations:")
for key, value in hive.bs_locations_list.items():
    log.stat("RESULT", "BS #" + str(key) + \
    ": number of clients in area - " + str(value["clients_in_area"]) + \
    ", location: " + str(value["location"]) + ", clients in area: " + str(value["clients_in_area_list"]))
###

graph = graphic(field.clients_list, hive.bs_locations_list, bs_area_radius)
