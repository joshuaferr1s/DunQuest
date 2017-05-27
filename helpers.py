import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory: ' + directory)
        os.makedirs(directory)

def create_configs_file():
    configs = 'configs.txt'
    if not os.path.isfile(configs):
        write_file(configs, '')

def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)

def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def delete_file_contents(path):
    open(path, 'w').close()

def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(links, file_name):
    with open(file_name,"w") as f:
        for l in links:
            f.write(str(l) + "\n")

def get_save_files(directory):
    saves = os.listdir(directory)
    save_files = list()
    for _ in saves:
        save_files.append(_.replace('.txt', ''))
    return save_files

def print_list(list_a):
    for li in list_a:
        print(li)