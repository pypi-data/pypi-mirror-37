def print_entire_list(argument_list):
        for each_element in argument_list:
            if isinstance(each_element,list):
                print_entire_list(each_element)
            else:
                print(each_element)