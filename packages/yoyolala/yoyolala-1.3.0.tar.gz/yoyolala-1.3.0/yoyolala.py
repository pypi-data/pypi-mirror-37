"""This is 'yoyolala.py' module,it provides a function named print_lol() can print
the list may include nested list with idention if you want"""
def print_lol(the_list,indent=False,level=0):
    """The function get a positional parameter called the_list can be any list(include
nested list),every element will be print in screen with every element in a line"""
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t",*level,end='')
            print(each_item)
