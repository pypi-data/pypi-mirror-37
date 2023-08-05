def print_list(the_list,level):
    ''' 这是一个打印出嵌套列表所有项的函数
    '''
    for item in the_list:
        if isinstance(item,list):
            print_list(item,level+1)
        else:
            for tab_shop in range(level):
                print('\t',end="")
            print(item)