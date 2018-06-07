def write_to_file(file, data):
    i = 1
    for c in data:
        if i == 61:
            file.write('\n    ')
            i = 1
        file.write(c)
        i += 1


def get_data(file_path, type_of_data):
    type_of_data = type_of_data + ':\n'
    file = open(file_path, encoding='utf-8')
    data = ''
    found = False
    for line in file:
        if found and line != '\n':
            data += line.strip()
        if found and line == '\n':
            found = False
        if line == type_of_data:
            found = True
    return data


def get_methods(file_path):
    file = open(file_path, encoding='utf-8')
    data = ''
    found = False
    for line in file:
        if found and line != '\n':
            data += line.strip() + ':'
        if found and line == '\n':
            found = False
        if line == 'Method:\n':
            found = True
    return data


def get_mode(mode):
    if (mode == 'ECB'):
        mode = 1
    elif (mode == 'OFB'):
        mode = 5
    elif (mode == 'CFB'):
        mode = 3
    else:
        mode = 2
    return mode
