from datetime import datetime

from abc import abstractmethod

from mobio.libs.Singleton import Singleton
import schedule
import time

from mobio.libs.thread_pool import ThreadPool


class BaseScheduler:
    thread_pool = ThreadPool(num_workers=8)
    logger = None
    is_running = False

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_schedule(self):
        """
        hàm xác định thời điểm chạy của scheduler, bằng cách xử dụng thư viện schedule
        Các ví dụ hướng dẫn cách xác định thời gian chạy
        1. scheduler chỉ thực hiện công việc một lần duy nhất.
            return None
        2. scheduler sẽ thực hiện mỗi 10 phút một lần.
            return schedule.every(10).minutes
        3. scheduler sẽ thực hiện hàng ngày vào lúc 10h 30 phút.
            return schedule.every().day.at("10:30")
        4. scheduler sẽ thực hiện sau mỗi giờ.
            return schedule.every().hour
        5. scheduler sẽ thực hiện vào mỗi thứ 2 hàng tuần.
            return schedule.every().monday
        6. scheduler sẽ thực hiện vào mỗi thứ 5 hàng tuần và vào lúc 13h 15'.
            return schedule.every().wednesday.at("13:15")
        """
        pass

    @abstractmethod
    def owner_do(self):
        """
        đây là hàm sẽ thực hiện công việc của scheduler,
        hàm này sẽ được gọi tự động và tự động bắt lỗi ghi log
        """
        pass

    def set_logger(self, logger):
        self.logger = logger

    @thread_pool.thread
    def do(self):
        try:
            if not self.is_running:
                # print(datetime.now(), " I'll start my job. ", self.name)
                self.is_running = True
                self.owner_do()
                # print(datetime.now(), " I'm finished my job. ", self.name)
                self.is_running = False
            else:
                # print(datetime.now(), " Please waiting, i'm busy. ", self.name)
                pass
        except Exception as e:
            if self.logger:
                self.logger.exception("run job error:%s!" % e)
            else:
                print("run job error:%s!" % e)
            return None


@Singleton
class SchedulerFactory:
    # thread_pool = ThreadPool(num_workers=8)

    def __init__(self):
        self.schedulers = {}
        self.tasks = {}
        self.logger = None

    def set_logger(self, logger):
        self.logger = logger

    def add(self, scheduler: BaseScheduler, scheduler_name=None):
        name = scheduler_name if scheduler_name else scheduler.__class__.__name__
        sq = self.schedulers.get(name, None)
        if sq is None:
            scheduler.set_logger(self.logger)
            the_schedule = scheduler.get_schedule()
            if the_schedule:
                the_schedule.do(scheduler.do)
                self.schedulers[name] = scheduler
            else:
                self.tasks[name] = scheduler
            return scheduler
        return sq

    def run(self):
        for stack in self.schedulers.values():
            stack.do()

        while True:
            schedule.run_pending()
            time.sleep(1)

    # @thread_pool.thread
    # def owner_run_scheduler(self, scheduler: BaseScheduler):
    #     scheduler.do()


if __name__ == '__main__':
    class TestScheduler1(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(1).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)

    class TestScheduler2(BaseScheduler):
        def __init__(self, name):
            super().__init__(name)

        def get_schedule(self):
            return schedule.every(2).seconds

        def owner_do(self):
            print(datetime.now(), " I'm working. ", self.name)
            time.sleep(3)

    fac = SchedulerFactory()
    fac.add(TestScheduler1('Test1'), 'TestScheduler1')
    fac.add(TestScheduler1('Test2'), 'TestScheduler2')
    fac.run()
