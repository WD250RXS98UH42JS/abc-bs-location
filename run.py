# -*- coding: utf-8 -*-
from lib import *

###
# Config section

# Count of bees per iteration
bees_count = 1

# Max scouting retries before finishing algorithm iteration 
max_retries_count = 20

# Number of clients located on field
clients_count = 20

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
log = log(log_file_path)

# Initialize 'field' instance
field = field(field_width, field_height, start_width_pos, start_height_pos, log)

# Generate 'clients_list' as part of 'field' instance
clients_list = field.generate_clients_list(clients_count)

# Initialize 'hive' instance
hive = hive(field, bs_max_clients_count, bs_area_radius, log)




log.msg("run".upper(), "clients_list items count: " + str(len(hive.clients_list)))
log.msg("run".upper(), "clients_list: " + str(hive.clients_list))

bees = [bee(hive, log) for i in range(bees_count)]
while len(hive.clients_list) > 0:
    bee.location = []
    bee.local_extremum = {}
    hive.global_extremum = {}
    scouting_area = hive.set_scouting_area(bs_area_radius)
    for _ in range(max_retries_count):
        for bee in bees:
            bee.scout(scouting_area)
    bee.set_bs_location(hive.global_extremum)
    for key, value in bee.clients_in_area_list.items():
        hive.modify_clients_list({key: value})
        log.msg("run".upper(), "deleted client from clients_list: " + str({key: value}))
    log.msg("run".upper(), "cleaned_clients_list items count: " + str(len(hive.clients_list)))
    bee.clients_in_area_list = {}
    log.msg("run".upper(), "\n############### END OF ITERATION ###############\n")
    
log.msg("run".upper(), "bs_locations_list: {")
for key, value in hive.bs_locations_list.items():
    log.msg("run".upper(), str(key)+" : "+str(value))


###
# TEST

# print(field.clients_list)

# x = hive.clients_list[3][0]
# y = hive.clients_list[3][1]
# hive.modify_clients_list({3:[x,y]})

# print(field.clients_list)
# print(hive.clients_list)
