" " "这是nester.py模块，提供了一个名为printf()的函数，函数的作用是打印列表，其中有可能包含（也有可能不包含）嵌套列表" " "

def printf (the_list):

    " " "参数是一个列表（可以嵌套也可以不嵌套)" " "
    for each in the_list:
        if isinstance(each,list):
            printf (each)
        else:
            print(each)


