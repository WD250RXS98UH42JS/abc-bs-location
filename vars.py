###
# Config section

# Log verbosity
# If -1, compact view will be used and only essential info will be showed
# If 0, only "STAT" entries will be showed
# If 1, "STAT", "ERR", "WARN" and "TEST" entries will be showed
# If 2, all entries will be showed
verbose = -1

# Relative path to log file (including filename)
log_file_path = "logs/log.txt"

# Basic station working area radius
bs_area_radius = 20

# List of variables maps
vars = [
    {
        # Field width
        'field_width': 3000,

        # Field height
        'field_height': 600,

        # Count of bees per iteration
        'bees_count': 55,

        # Max scouting retries before finishing algorithm iteration 
        'max_retries_count': 50,

        # Number of clients located on field
        'clients_count': 200,

        # If [], clients list will be generated automatically
        # If any values exists, they will become entries of clients list
        'clients_list': []
    },
    {
        'field_width': 20,
        'field_height': 20,
        'bees_count': 10,
        'max_retries_count': 5,
        'clients_count': 200,
        'clients_list': [
                            [15,15],
                            [14,14],
                            [14,15],
                            [1,1],
                            [2,2],
                            [2,1]
                        ]
    },
]