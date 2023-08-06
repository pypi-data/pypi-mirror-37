"""The module provides a function called print_lol(), which returns or not the items
in lists that may or may not include nested lists, and can be used with up to 3 arguments:
default (list), indented (list, True) or indented from a value (list, True, 2)."""


def print_lol(the_list, indent=False, level=0):
    """We go through the list, if there is another list inside the list, it will be displayed by calling
     the function itself in if. Use the arguments (list, True) for indented output or a value (list, True, 2)."""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t', end='')
            print(each_item)
