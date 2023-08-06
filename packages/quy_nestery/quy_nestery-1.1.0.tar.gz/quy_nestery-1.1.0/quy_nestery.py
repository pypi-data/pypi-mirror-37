""" Recursion function to print all elements of list-to-list """
def print_lol(the_list, level):
    """ Pass all elements then check whether it's a list,
        if not prints that element, if yes recurs """
    for each_item in the_list:
        if(isinstance(each_item,list)): 
           print_lol(each_item, level+1)
        else:
            for i in range(level):
                print("\t", end='')
            print(each_item)
           
