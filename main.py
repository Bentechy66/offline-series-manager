from arbitrium import menu
from os import path
from config import modules, modules_path
import json
from utils import log

def load_startup_modules():
    loaded_modules = []

    for module in modules:
        log("info", "Loading module " + module)
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
            log("success", "Loaded module " + module)
    return loaded_modules

def select_video():
    # TODO: Better video selection system
    print("-=-Video Manager-=-\nAn extensible video modification system with plugin support, written by Ben Griffiths.\n\nWelcome! To begin, please select a video.\n")
    with open("series_aliases.json") as f:
        module_data = json.load(f)
        video = log("input", "Please enter either full video filepath or an alias").lower()
        log("info", "Looking up input in aliases file")
        if video in module_data:
            video = module_data[video]
            log("success", "Found input in aliases file!")
            video = video.replace("{series}", log("input", "Please enter season number"))
            video = video.replace("{episode}", log("input", "Please enter episode number"))
            # TODO: Check file exists
            log("success", "Video path successfully formed.")
            return video
        else:
            log("info", "Input not found in aliases. Assuming absolute path.")
            # TODO: Check file exists
            return video

video = select_video()

loaded_modules = load_startup_modules()
menu_options = []
for module in loaded_modules:
    menu_options.append(f"[{module['name'].capitalize()}] - {module['menu_listing']}")
menu_options.append("Quit")

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
