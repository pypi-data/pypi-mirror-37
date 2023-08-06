"""这是"nester.py"模块，提供一个名为pirnt_lol()得函数，这个函数得作用是打印列表，
其中有可能包含（也可能不包含）嵌套列表。"""
def print_lol(the_list, level):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for num in range(level):
                print("\t", end='')
            print(each_item)
            
