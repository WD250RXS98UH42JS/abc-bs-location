# -*- coding: utf-8 -*-
from lib import *
from vars import *

def abc_bs_location(field_width, field_height, bees_count, max_retries_count, clients_count, clients_list):

    global bs_area_radius, log_file_path, verbose

    # Initialize 'log' instance
    log = Log(log_file_path, verbose)

    # Initialize 'field' instance
    field = Field(field_width, field_height, log)

    # Initialize 'hive' instance
    hive = Hive(field, bs_area_radius, log)

    # Generate 'clients_list' as part of 'field' instance
    field.clients_list = field.create_clients_list(clients_count, clients_list)
    hive.clients_list = field.clients_list
    clients_count = len(field.clients_list)

    ### LOGGING
    log.stat("run".upper(), "Program started. All instances initialized.")
    log.stat("run".upper(), "There are " + str(len(hive.clients_list)) + " clients.")
    log.msg("run".upper(), "clients_list:")
    for key, value in hive.clients_list.items():
        log.msg("run".upper(), str(key)+" : "+str(value))
    ###

    bees = [Bee(hive, log) for i in range(bees_count)]
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

        ## LOGGING
            log.msg("run".upper(), "deleted client from clients_list: " + str({key: value}))
        log.msg("run".upper(), "cleaned_clients_list items count: " + str(len(hive.clients_list)))
        log.stat("run".upper(), "### Iteration #"+ str(iter_count) +" ended. ###")
        ##

        iter_count += 1

    ### LOGGING

    log.main("RESULT", "\n###" + \
        "\nField width: " + str(field_width) + \
        "\nField height: " + str(field_height) + \
        "\nClients number: " + str(clients_count) + \
        "\nBees count: " + str(bees_count) + \
        "\nRetries count: " + str(max_retries_count) + \
        "\n\nBS count: " + str(len(hive.bs_locations_list.items())) + "\n")
    log.time()

    log.stat("RESULT", "############################################################")
    log.stat("RESULT", "Program execution was finished.")
    log.stat("RESULT", "List of basic stations locations:")
    for key, value in hive.bs_locations_list.items():
        log.stat("RESULT", "BS #" + str(key) + \
        ": number of clients in area - " + str(value["clients_in_area"]) + \
        ", location: " + str(value["location"]) + ", clients in area: " + str(value["clients_in_area_list"]))
    
    ###

    if verbose != -1:
        graph = Graphic(field.clients_list, hive.bs_locations_list, bs_area_radius)


for set in vars:
    abc_bs_location(set["field_width"], 
                    set["field_height"], 
                    set["bees_count"], 
                    set["max_retries_count"], 
                    set["clients_count"], 
                    set["clients_list"])
