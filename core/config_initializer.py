import logging
import os

from config import chat_spider_config as cfg

logging.debug(f'permissions.default.image is set to 2, images in the website will not be loaded.')


def select(prompt: str):
    logging.info(prompt)
    flag = input()
    if flag.lower() == 'n':
        return False
    return True


def xhs_init_config_from_py():
    xhs_save_path = cfg.xhs_save_path
    if not os.path.exists(xhs_save_path):
        if not select(prompt=f'❓️ "{xhs_save_path}" does not exist, shall we create it for you? [y]/N'):
            raise NotADirectoryError()
        else:
            os.makedirs(xhs_save_path)
    init_config_from_py()


def bili_init_config_from_py():
    save_path = cfg.save_path
    if not os.path.exists(save_path):
        if not select(prompt=f'❓️ "{save_path}" does not exist, shall we create it for you? [y]/N'):
            raise NotADirectoryError()
        else:
            os.makedirs(save_path)
    init_config_from_py()


def init_config_from_py():
    max_parallel_job_num = cfg.max_parallel_job_num
    if max_parallel_job_num > 36:
        logging.warning(
            f'⚠️ Argument "max_parallel_job_num" was set to {max_parallel_job_num} and self may cause your system crash.')

    sleep_time_before_job_launching = cfg.sleep_time_before_job_launching
    if sleep_time_before_job_launching > 60:
        logging.warning(
            f'⚠️ Argument "sleep_time_before_job_launching" was set to {sleep_time_before_job_launching} and self may '
            f'cause long time waiting.')

    sleep_time_after_job_launching = cfg.sleep_time_after_job_launching
    if sleep_time_after_job_launching > 60:
        logging.warning(
            f'⚠️ Argument "sleep_time_after_job_launching" was set to {sleep_time_after_job_launching} and self may '
            f'cause long time waiting.')

    firefox_profile_dir = cfg.firefox_profile_dir
    if not os.path.exists(firefox_profile_dir):
        logging.warning(
            f'⚠️ Argument "firefox_profile_dir" was set to "{firefox_profile_dir}" and it is not an accessible nor '
            f'valid'
            f'directory. This may cause selenium can not found sufficient replies from your web browser when your '
            f'login-info can not be pertained.')

    firefox_driver_dir = cfg.firefox_driver_dir
    if not os.path.exists(firefox_driver_dir):
        logging.error(
            f'❌️ Argument "firefox_driver_dir" was set to "{firefox_driver_dir}" and it is not an accessible nor '
            f'valid directory. Without setting a proper path, selenium can not start successfully.')
        raise NotADirectoryError()
