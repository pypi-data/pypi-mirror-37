""" Recursion function to print all elements of list-to-list """
def print_lol(the_list):
    """ Pass all elements then check whether it's a list,
        if not prints that element, if yes recurs """
    for each_item in the_list:
        if(isinstance(each_item,list)):
           print_lol(each_item)
        else:
           print(each_item)
           
