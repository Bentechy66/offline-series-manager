from arbitrium import menu
from os import path
from config import modules, modules_path
import json
from utils import log

def load_startup_modules():
    loaded_modules = []

    for module in modules:
        with open(modules_path + module + ".json") as f:
            module_data = json.load(f)
            if module_data["name"] != module:
                log("warning", f"Error in loading module '{module}'. 'name' key did not match filename.")
                continue
            if not "name" in module_data or not "menu_listing" in module_data:
                log("warning", f"Error in loading module '{module}'. It did not contain some of the correct keys.")
                continue
            if not path.exists(modules_path + module + ".py"):
                log("warning", f"Error in loading module '{module}'. Could not find '{module}.py'.")
                continue
            loaded_modules.append(module_data)
    return loaded_modules

def select_video():
    # TODO: Better video selection system
    print("Welcome! To begin, please select a video.")
    return input("Please enter video name>> ")

loaded_modules = load_startup_modules()
menu_options = []
for module in loaded_modules:
    menu_options.append(f"[{module['name'].capitalize()}] - {module['menu_listing']}")
menu_options.append("Quit")

video = select_video()

@menu(menu_options)
def choice_handler(choice):
    if choice != 99:
        module_name = loaded_modules[choice - 1]["name"]
        import_string = "import modules." + module_name
        # TODO: Escape strings, probably not a problem since filenames but something to consider
        exec(import_string)
        exec("modules." + module_name + ".main(video)")

# Calling the choice handler will also print the menu
choice_handler()
