import logging
import time, datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

#переопределения класса-обработчика событий файловой системы
class CustomEventHandler(FileSystemEventHandler):

    def __init__(self, log_path):
        self.log_path = log_path

    def on_moved(self, event):
        super().on_moved(event)
        now = datetime.datetime.now()
        current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
        what = 'каталог' if event.is_directory else 'файл'
        with open(self.log_path, 'a+') as log:
            log.write(f"{current_time} Переименован {what}: из {event.src_path} в {event.dest_path}\n")
        print(f"{current_time} Переименован {what}: из {event.src_path} в {event.dest_path}\n")

    def on_created(self, event):
        super().on_created(event)
        now = datetime.datetime.now()
        current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
        what = 'каталог' if event.is_directory else 'файл'
        with open(self.log_path, 'a+') as log:
            log.write(f"{current_time} Создан {what}: {event.src_path}\n")
        print(f"{current_time} Создан {what}: {event.src_path}\n")

    def on_deleted(self, event):
        super().on_deleted(event)
        now = datetime.datetime.now()
        current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
        what = 'каталог' if event.is_directory else 'файл'
        with open(self.log_path, 'a+') as log:
            log.write(f"{current_time} Удалён {what}: {event.src_path}\n")
        print(f"{current_time} Удалён {what}: {event.src_path}\n")

    def on_modified(self, event):
        super().on_modified(event)
        now = datetime.datetime.now()
        current_time = str(now.strftime("%d-%m-%Y %H:%M:%S"))
        what = 'каталог' if event.is_directory else 'файл'
        with open(self.log_path, 'a+') as log:
            log.write(f"{current_time} Изменён {what}: {event.src_path}\n")
        print(f"{current_time} Изменён {what}: {event.src_path}\n")

def log(log_path, source):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    path = Path(source).resolve()
    event_handler = CustomEventHandler(log_path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()