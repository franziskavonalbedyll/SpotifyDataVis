import datetime
from src.config import *

def get_current_date_and_time():
    return datetime.datetime.now().strftime("%m.%d.%Y_%H.%M.%S")

def year_to_filepath(year: int):
    return f'{PREPROCCESSED_DATA_DIR}/{str(year)}.csv'