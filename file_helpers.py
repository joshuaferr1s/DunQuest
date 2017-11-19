import os, json


def load_dungeon(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
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


def create_save_dir(savename):
    if not os.path.exists('saves'):
        os.makedirs('saves')
    if not os.path.exists('saves/' + savename):
        os.makedirs('saves/' + savename)


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def create_save_files(savename):
    write_file('saves/' + savename + '/dungeons.txt', '')
    write_file('saves/' + savename + '/equipped.txt', '')
    write_file('saves/' + savename + '/inventory.txt', '')
    write_file('saves/' + savename + '/player.txt', '')
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
    inva = [
        '#', '%', '&', '{', '}', "\\", '<', '>', '*', '?', '/', ' ', '$', '!',
        "'", '"', ':', '@'
    ]
    for i in inva:
        if i in file_name:
            return False
    return True


def get_market_files(savename):
    market = os.listdir('saves/' + savename + '/')
    markets = list()
    for _ in market:
        markets.append('saves/' + savename + '/' + _)
    return markets


def get_dirs(path):
    dirs = os.listdir(path)
    return dirs


def get_files(path):
    raw_files = os.listdir(path)
    files = list()
    result = list()
    for _ in raw_files:
        files.append(_.replace('.txt', ''))
    for _ in files:
        result.append(_.replace('.json', ''))
    result.remove('.DS_Store')
    return result
