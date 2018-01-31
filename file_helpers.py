import os, json


def load_dungeon(file_name):
    dict_from_file = {}
    with open(file_name, 'r') as inf:
        dict_from_file = json.load(inf)
    return dict_from_file


def write_dict_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


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


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def delete_file_contents(path):
    open(path, 'w').close()


def get_market_files(savename):
    market = os.listdir('saves/' + savename + '/')
    markets = list()
    for _ in market:
        markets.append('saves/' + savename + '/' + _)
    return markets
