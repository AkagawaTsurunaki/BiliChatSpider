import argparse
import logging
import time
import schedule
from core.pro_spider import ProSpider
from core.multitask_spider import MultitaskSpider
from core.config_initializer import init_config_from_py


def run(args):
    init_config_from_py()
    logging.info('Custom configuration loaded.')

    logging.info('🕐 Waiting for timer...')
    schedule.every().day.at("00:01").do(job_func=__run, args=args)

    while True:
        schedule.run_pending()
        time.sleep(1)


def __run(args):
    for uid in args.list:
        ProSpider().update_job(uid=uid, force_create_job=args.force.lower() != 'n')
        MultitaskSpider().run(uid=uid)


if __name__ == '__main__':

    print('Bili Chat Spider')

    # Initialize arguments parser.
    parser = argparse.ArgumentParser(prog='Bili Chat Spider',
                                     description='A spider script which can get replies from bilibili.',
                                     epilog=''
                                     )
    parser.add_argument('-l', '--list', nargs='+', type=str)
    parser.add_argument('-f', '--force', type=str, default=False)
    parser.add_argument('-t', '--time', type=str, default="00:01")

    args = parser.parse_args()

    run(args)
