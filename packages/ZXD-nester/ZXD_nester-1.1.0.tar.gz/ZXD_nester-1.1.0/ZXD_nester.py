'''这是nester_New.py模块，提供了一个名为printf的函数用来打印列表，其中不包含或不包含嵌套列表'''

def printf(the_list,level=0):
    '''这个函数有一个位置参数，名为“the list”，这可以是任何python列表（包含或不包含嵌套列表），所提供列表中的各个数据项回打印到屏幕上，而且各占一方'''
    for each_item in the_list:
        if isinstance(each_item,list):
            printf(each_item,level+1)
        else:
            for tap_stop in range(level):
                print("\t",end="")
            print(each_item)