"""This is 'nester.py' module,it provides a function named print_lol() can print
the list may include nested list"""
def print_lol(the_list,level=0):
    """The function get a positional parameter called the_list can be any list(include
nested list),every element will be print in screen with every element in a line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,level+1)
        else:
            for tab_stop in range(level):
                print("\t",end='')
            print(each_item)
