import os, shutil
from log_thread import *
from threading import Thread

def get_timer():
    while True:
        timer = input('Введите интервал сбора статистики в секундах:\n')
        if timer.isdigit():
            return int(timer)
        else:
            print('Недопустимый формат ввода времени.')

def all_paths():
    while True:
        def get_path(num):
            while True:
                if num == 1:
                    text = 'Введите путь к каталогу-источнику.\n'
                elif num == 2:
                    text = 'Введите путь к каталогу-реплике.\n'
                else:
                    text = 'Введите путь к файлу логирования.\n'
                cpath = input(text)
                if os.path.exists(cpath):
                    return cpath
                else:
                    print('Указан неверный путь.')
        path1 = get_path(1)
        path2 = get_path(2)
        if path1 != path2:
            path3 = get_path(3)
            return path1, path2, path3
        else:
            print('Указано одинаковое расположение каталога-источника и каталога-реплики.')

def synchronization(source, replica):
    timer = get_timer()
    if not source.endswith('\\'):
        source += '\\'
    if not replica.endswith('\\'):
        replica += '\\'
    while True:
        files = os.listdir(source)
        files2 = files.copy()
        #удаление содержимого директории реплики
        for root, dirs, files in os.walk(replica):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))
        #синхронизация директории реплики с источником
        for f in files2:
            if '.' not in f:
                shutil.copytree(source + f, replica + f)
            else:
                shutil.copyfile(source + f, replica + f)
        time.sleep(timer)

source, replica, log_path = all_paths()
t1 = Thread(target=synchronization, args=(source, replica,))
t2 = Thread(target=log, args=(log_path, source, ))
t1.start()
t2.start()