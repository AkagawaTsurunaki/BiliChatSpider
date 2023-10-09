import argparse
import logging
import time
import schedule
from core.pro_spider import ProSpider
import core.multitask_spider
from core.config_initializer import init_config_from_py


def run(args):
    init_config_from_py()
    logging.info('Custom configuration loaded.')

    if args.time.lower() != 'now':
        logging.info('🕐 Waiting for timer...')
        schedule.every().day.at(args.time).do(job_func=__run, args=args)

        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        __run(args)


def __run(args):
    for uid in args.list:
        ProSpider().update_job(uid=uid, force_create_job=args.force.lower() != 'n')
        core.multitask_spider.run(uid=uid)


if __name__ == '__main__':
    print('🕷️ Bili Chat Spider 🕷️')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize arguments parser.
    parser = argparse.ArgumentParser(prog='Bili Chat Spider',
                                     description='A spider script which can get replies from bilibili.',
                                     epilog=''
                                     )
    parser.add_argument('-l', '--list', nargs='+', type=str)
    parser.add_argument('-f', '--force', type=str, default='Y')
    parser.add_argument('-t', '--time', type=str, default='now')

    args = parser.parse_args()

    run(args)

    logging.info(f'✅ All tasks completed.')
