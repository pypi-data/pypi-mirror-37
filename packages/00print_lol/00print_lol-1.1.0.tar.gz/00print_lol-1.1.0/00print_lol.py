"""
This is the "print_lol.py" module,and it offers one function named print_lol()
which prints lists that may or may not include nested lists

"""




def print_lol(the_list,level):

    """
This function takes a positional argument called "the_list",which is any Python list(of,possibly,nested lists).Each data item in
the provided list is (recursively) printed to the screen on its own line;anther argument named "level",which is used
表示要缩进几个TAP
    """
    for item in the_list:
        if isinstance(item,list):
            print_lol(item,level+1)
        else:
            for num in range(level):
                print("\t",end="")
            print(item)
