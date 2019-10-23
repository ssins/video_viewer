import os
from flask_model_template import *

root_path = os.path.join(os.getcwd(), 'App')


def create_dir(path):
    try:
        if os.path.exists(path):
            return False
        os.makedirs(path)
        return True
    except:
        return False


def create_file(path, txt=None):
    try:
        if os.path.exists(path):
            return False
        f = open(path, 'w+')
        if txt:
            f.write(txt)
        f.close
        return True
    except:
        return False


def add_placeholder_line(path, placeholder, txt):
    try:
        lines = []
        hit = 0
        with open(path, 'r', encoding='UTF-8') as fin:
            lines = fin.readlines()
            for index, line in enumerate(lines):
                if line.find('>>'+placeholder+'<<') > 0:
                    hit = index
                    break
            if hit:
                lines.insert(hit, txt)
            fin.close
        with open(path, 'w', encoding='UTF-8') as fout:
            for line in lines:
                fout.write(line)
            fout.close
        return True
    except:
        return False


def create_model(name):
    name_l = name.lower()
    name_u = name.capitalize()
    print('create root folder: {}'.format(
        create_dir(os.path.join(root_path, name_u))))
    print('create static folder: {}'.format(
        create_dir(os.path.join(root_path, name_u, 'static'))))
    print('create template folder: {}'.format(
        create_dir(os.path.join(root_path, name_u, 'template'))))
    print('create __init__.py: {}'.format(create_file(
        os.path.join(root_path, name_u, '__init__.py'), txt=temp_init.format(name_l, name_l, name_u, name_u, name_u, name_u))))
    print('create controllers.py: {}'.format(create_file(
        os.path.join(root_path, name_u, 'controllers.py'), txt=temp_controllers.format(name_u))))
    print('create views.py: {}'.format(create_file(
        os.path.join(root_path, name_u, 'views.py'), txt=temp_views.format(name_u, name_l, name_l))))
    print('add import: {}'.format(add_placeholder_line(os.path.join(
        root_path, '__init__.py'), 'import', temp_import.format(name_u, name_l))))
    print('add register: {}'.format(add_placeholder_line(os.path.join(
        root_path, '__init__.py'), 'register', temp_register.format(name_l, name_l))))


if __name__ == "__main__":
    create_model('Permission')
