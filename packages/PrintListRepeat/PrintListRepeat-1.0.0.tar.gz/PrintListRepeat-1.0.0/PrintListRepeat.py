"""这是PrintListRepeat.py模块，提供了一个名为print_lol_re()的函数，这个函数的作用是打印列表，其中有可能包含（也有可能不包含）嵌套列表"""
def print_lol_re(the_list):
        """这个函数取一个位置参数，名为“the_list”，着可以是任何python列表。所制定的列表中的每一个数据项都会（递归地）输出到屏幕上，各个数据项各占一行"""
	for i in the_list:
		if isinstance(i,list):
			print_lol_re(i)
		else:
			print(i)
