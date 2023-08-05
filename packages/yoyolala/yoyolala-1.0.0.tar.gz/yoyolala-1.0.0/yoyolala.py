"""This is 'nester.py' module,it provides a function named print_lol() can print
the list may include nested list"""
def print_lol(the_list):
    """The function get a positional parameter called the_list can be any list(include
nested list),every element will be print in screen with every element in a line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
