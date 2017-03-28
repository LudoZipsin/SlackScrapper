import sys

BASE_ERROR_MSG = "Exiting..."
ACTION_TO_IGNORE = {"__init__",
                    "activate",
                    "deactivate",
                    "actions"}
ACTION_PATTERN_TO_IGNORE = "_"


def error(msg: str, name: str=None, lst: list=None):
    print(msg)
    if name is not None and lst is not None:
        print("Please select a {name} from the available {name} list".format(name=name))
        list_printer(name, lst)
    print(BASE_ERROR_MSG)

    sys.exit(1)


def list_printer(name: str, lst: list) -> None:
    base_msg = "Available {name}: ".format(name=name)
    filler = " "*len(base_msg)
    fill = False
    for l in lst:
        if fill is False:
            print(base_msg + l)
            fill = True
        else:
            print(filler + l)


def simplify_list(lst: list):
    if type(lst) is list:
        if len(lst) == 1:
            return lst[0]
        else:
            error("The list '{lst}' contains more than one element".format(lst=lst))
    else:
        error("the provided element is not a list.")


def remove_action_to_ignore(lst: list) -> list:
    return [action[0] for action in lst if action[0] not in ACTION_TO_IGNORE and action[0][0] != "_"]
