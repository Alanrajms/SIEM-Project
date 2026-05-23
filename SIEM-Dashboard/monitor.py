from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from detector import detect_threat
from blocker import extract_ip, block_ip
import time


class LogHandler(FileSystemEventHandler):

    def on_modified(self, event):

        if event.src_path.endswith("live_logs.txt"):

            with open(event.src_path, "r") as file:

                lines = file.readlines()

                if lines:

                    latest_log = lines[-1]

                    print("[NEW LOG]", latest_log)

                    if detect_threat(latest_log):

                        print("[ALERT] Threat Detected!")

                        ip = extract_ip(latest_log)

                        if ip:
                            block_ip(ip)

def start_monitor():

    path = "./sample_logs"

    event_handler = LogHandler()
    observer = Observer()

    observer.schedule(event_handler, path, recursive=False)

    observer.start()

    print("[*] Real-Time Monitoring Started...")

    try:
     while True:
      time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()