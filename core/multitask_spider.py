import logging
from multiprocessing import Process

from core.single_task_spider import SingleTaskSpider
from dataset_manager import DatasetManager
from history import HistoryManager
from driver_initilizer import DriverInitializer


class MultitaskSpider:

    @staticmethod
    def __run_single_task(history: HistoryManager, uid: str, bv: str):
        logging.debug(f'Task {bv} executing...')
        driver = DriverInitializer.get_firefox_driver()
        data = SingleTaskSpider(driver).get_reply_records(bv)
        DatasetManager().save_single_task(uid=uid, bv=bv, data=data)
        history.single_task_completed(uid=uid, bv=bv)
        driver.close()
        driver.quit()
        logging.debug(f'Task {bv} completed.')

    @staticmethod
    def run(uid: str):

        # If the job is completed then return straightly
        if HistoryManager.is_job_completed(uid):
            return

        # If the job is not completed,
        # Get the uncompleted bv list.
        processes = []
        for bv in HistoryManager.get_uncompleted_tasks(uid):
            process = Process(target=MultitaskSpider.__run_single_task, args=(HistoryManager, uid, bv))
            processes.append(process)

        # Start all processes.
        for process in processes:
            process.start()

        # Waiting for all processes completed.
        for process in processes:
            process.join()
