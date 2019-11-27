# -*- coding: utf-8 -*-
from lib import *

###
# Config section

# Count of bees per iteration
bees_count = 5

# Max scouting retries before finishing algorithm iteration 
max_retries_count = 10

# Number of clients located on field
clients_count = 5

# Number of clients are possible to connect to single basic station
bs_max_clients_count = 50

# Basic station working area radius
bs_area_radius = 100

# Field width
field_width = 100000

# Field height
field_height = 100000

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
hive = hive(field, log)

scouting_area = hive.set_scouting_area(bs_area_radius)

bees = [bee(hive, log) for i in range(bees_count)]
for bee in bees:
    bee.set_bee_location(scouting_area)

###
# TEST

# print(field.clients_list)

# x = hive.clients_list[3][0]
# y = hive.clients_list[3][1]
# hive.modify_clients_list({3:[x,y]})

# print(field.clients_list)
# print(hive.clients_list)
