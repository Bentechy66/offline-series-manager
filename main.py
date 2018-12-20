from arbitrium import menu
import modules.subtitles
from os import chdir
from config import modules, modules_path
import json
from utils import log

def load_startup_modules():
    loaded_modules = []

    for module in modules:
        with open(modules_path + module + ".json") as f:
            module_data = json.load(f)
            if not "name" in module_data or not "menu_listing" in module_data:
                log("warning", f"Error in loading module '{module}'. It did not contain some of the correct keys.")
                continue
            loaded_modules.append(module_data)
    return loaded_modules

loaded_modules = load_startup_modules()
menu_options = []
for module in loaded_modules:
    menu_options.append(f"[{module['name']}] - {module['menu_listing']}")
menu_options.append("Quit")

@menu(menu_options)
def choice_handler(choice):
  # todo

# Calling the choice handler will also print the menu
choice_handler()
