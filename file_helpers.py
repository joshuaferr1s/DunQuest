import os

def load_dungeon(file_name):
	dict_from_file = {}
	with open(file_name,'r') as inf:
		dict_from_file = eval(inf.read())
	return dict_from_file

def borderfy_text(text):
	border = ''
	output_text = '# '
	counter = 0
	var = 4 + len(text)

	while counter < var:
		border += '#'
		counter += 1

	output_text += text
	output_text = output_text + ' #'

	print(border)
	print(output_text)
	print(border)