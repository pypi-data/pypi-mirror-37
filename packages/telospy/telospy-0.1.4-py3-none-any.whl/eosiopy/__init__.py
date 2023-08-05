#                             _                      _ __    _  _
#    ___     ___     ___     (_)     ___     ___    | '_ \  | || |
#   / -_)   / _ \   (_-<     | |    / _ \   |___|   | .__/   \_, |
#   \___|   \___/   /__/_   _|_|_   \___/   _____   |_|__   _|__/
# _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|     |_|"""""|_| """"|
# "`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'


import logging

logger = logging.getLogger()
# TODO: setup a method for switching the code from development to production
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

