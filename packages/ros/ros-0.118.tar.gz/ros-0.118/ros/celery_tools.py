'''
A python script which starts celery worker and auto reload it when any code change happens.  
I did this because Celery worker's "--autoreload" option seems not working for a lot of people. 
'''
import time
from watchdog.observers import Observer  ##pip install watchdog
from watchdog.events import PatternMatchingEventHandler  
import psutil  ##pip install psutil
import os
import subprocess

'''
code_dir_to_monitor = "/path/to/your/code/dir"
celery_working_dir = code_dir_to_monitor #happen to be the same. It may be different on your machine
celery_cmdline = 'celery worker -A some_project -l INFO'.split(" ")
'''

class LibUpdateHandler(PatternMatchingEventHandler):

    def __init__(self, patterns, runner):
        self.runner = runner
        super(LibUpdateHandler, self).__init__(patterns)

    def on_any_event(self, event):
        print("detected change. event = {}".format(event))

        for proc in psutil.process_iter():
            proc_cmdline = self._get_proc_cmdline(proc)
            if not proc_cmdline or len(proc_cmdline) < len(celery_cmdline):
                continue

            is_celery_worker = 'python' in proc_cmdline[0].lower() \
                               and celery_cmdline[0] == proc_cmdline[1] \
                               and celery_cmdline[1] == proc_cmdline[2]
            
            if not is_celery_worker:
                continue

            proc.kill()
            print("Just killed {} on working dir {}".format(proc_cmdline, proc.cwd()))

        self.runner.start()

    def _get_proc_cmdline(self, proc):
        try:
            return proc.cmdline()
        except Exception as e:
            return []

'''
def run_worker():

    print("Ready to call {} ".format(celery_cmdline))
    os.chdir(celery_working_dir)
    subprocess.Popen(celery_cmdline)
    print("Done callling {} ".format(celery_cmdline))

if __name__ == "__main__":

    run_worker()

    event_handler = LibUpdateHandler(patterns = ["*.py"])
    observer = Observer()
    observer.schedule(event_handler, code_dir_to_monitor, recursive=True)
    observer.start()
    print("file change observer started")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
'''

class CeleryManager:
    
    def __init__(self,
                 code_dir_to_monitor,
                 celery_working_dir, #happen to be the same. It may be different on your machine
                 celery_cmdline):
        self.code_dir_to_monitor = code_dir_to_monitor
        self.celery_working_dir = celery_working_dir
        self.celery_cmdline = celery_cmdline

    def run (self):
        self.run_worker()
        event_handler = LibUpdateHandler(patterns = ["*.py"],
                                         runner = self)
        observer = Observer()
        observer.schedule(event_handler, self.code_dir_to_monitor, recursive=True)
        observer.start()
        print("file change observer started")        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    def start (self):
        print("Ready to call {} ".format(self.celery_cmdline))
        os.chdir(self.celery_working_dir)
        subprocess.Popen(self.celery_cmdline)
        print("Done callling {} ".format(self.celery_cmdline))        
        
        
