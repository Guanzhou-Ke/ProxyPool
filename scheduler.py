from multiprocessing import Process
from time import sleep
from datetime import datetime


class Scheduler():
    """
    调度器
    """

    def __init__(self, detector, booter, detect_minute=5, get_minute=20):
        self.detector = detector
        self.booter = booter
        self.detect_minute = detect_minute * 20
        self.get_minute = get_minute * 60
        self.DETECT = True
        self.GETTER = True
        self.API_SERVER = True


    def run_detector(self):
        while True:
            self.detector.run()
            sleep(self.detect_minute)

    
    def run_booter(self):
        while True:
            self.booter.run()
            sleep(self.get_minute)
    

    def run(self):
        if self.GETTER:
            booter_process = Process(target=self.run_booter)
            booter_process.start()

        if self.DETECT:
            detector_process = Process(target=self.run_detector)
            detector_process.start()

