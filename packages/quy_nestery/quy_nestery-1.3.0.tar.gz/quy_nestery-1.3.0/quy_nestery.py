""" Recursion function to print all elements of list-to-list """
def print_lol(the_list, indent = False, level=0):
    """ the_list: Nested list
        indent: Switch on/off indentation
        level: tap-stop times """
    for each_item in the_list:
        if(isinstance(each_item,list)): 
           print_lol(each_item, indent, level+1)
        else:
            if indent == True:
                for i in range(level):
                    print("\t", end='')
            print(each_item)
           
