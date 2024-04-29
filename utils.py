import os
from configparser import ConfigParser, NoSectionError
from config.settings import BASE_DIR

git
def get_data_from_config(name_section: str):
    """This method gets a dictionary with data from the config.ini file"""
    filename = os.path.join(BASE_DIR, "config.ini")
    parser = ConfigParser()
    try:
        parser.read(filename)
        return dict(parser.items(name_section))
    except NoSectionError as err_:
        raise Exception(f"Section '{name_section}' not found in '{filename}'") from err_
