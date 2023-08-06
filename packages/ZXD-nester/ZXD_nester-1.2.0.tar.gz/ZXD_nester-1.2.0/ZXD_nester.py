'''这是nester_New.py模块，提供了一个名为printf的函数用来打印列表，其中不包含或不包含嵌套列表'''

def printf(the_list,indent=False,level=0):
    '''这个函数有一个位置参数，名为“the list”，这可以是任何python列表（包含或不包含嵌套列表），所提供列表中的各个数据项回打印到屏幕上，而且各占一行
    一个选择参数，如果需要缩进打印，则应输入Ture,第三个参数用来在遇到嵌套列表时插入制表符'''
    for each_item in the_list:
        if isinstance(each_item,list):
            printf(each_item,indent,level+1)
        else:
            if indent:
              for tap_stop in range(level):
                print("\t",end="")
            print(each_item)
