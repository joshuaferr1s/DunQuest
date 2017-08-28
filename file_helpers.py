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

def create_save_dir():
	if not os.path.exists('saves'):
		os.makedirs('saves')

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def create_save_files(savename):
	if not os.path.isfile('saves/dungeons.txt') and not os.path.isfile('saves/equipped.txt') and not os.path.isfile('saves/inventory.txt') and not os.path.isfile('saves/player.txt'):
		write_file('saves/' + savename + 'dungeons.txt', '')
		write_file('saves/' + savename + 'equipped.txt', '')
		write_file('saves/' + savename + 'inventory.txt', '')
		write_file('saves/' + savename + 'player.txt', '')
		return True

def append_to_file(path, data):
	with open(path, 'a') as file:
		file.write(str(data) + '\n')

def delete_file_contents(path):
	open(path, 'w').close()

def file_to_set(file_name):
	results = list()
	with open(file_name, 'rt') as f:
		for line in f:
			results.append(line.replace('\n', ''))
	return results

def valid_file_name(file_name):
	inva = ['#', '%', '&', '{', '}', "\\", '<', '>', '*', '?', '/', ' ', '$', '!', "'", '"', ':', '@']
	for i in inva:
		if i in file_name:
			return False
	return True

def get_save_files():
	saves = os.listdir('saves/')
	save_files = list()
	for _ in saves:
		save_files.append(_.replace('.txt', ''))
	return save_files