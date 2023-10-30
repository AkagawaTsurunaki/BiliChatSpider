import argparse
import logging

from bilibili2 import multitask_spider
from core.config_initializer import init_config_from_py


def run(args):
    init_config_from_py()
    logging.info('⚙️ Custom configuration loaded.')

    if args.bv is not None and args.uid is not None and len(args.bv) != 0:
        multitask_spider.collect_by_bv_list(args.uid, args.bv)

    if args.list is not None and (args.list) != 0:
        for uid in args.list:
            upname, bv_list = multitask_spider.scan_space_by_uid(uid)
            logging.info(f'🪹 {upname} (uid={uid}): Scanning completed.')
            multitask_spider.collect_by_bv_list(uid, bv_list)


if __name__ == '__main__':

    try:
        print('🍺 Bili Chat Spider 🍺')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Initialize arguments parser.
        parser = argparse.ArgumentParser(prog='Bili Chat Spider',
                                         description='A spider script which can get replies from bilibili.',
                                         epilog=''
                                         )
        parser.add_argument('-l', '--list', nargs='+', type=str)
        parser.add_argument('-b', '--bv', nargs='+', type=str)
        parser.add_argument('-u', '--uid', type=str)
        parser.add_argument('-f', '--force', type=str, default='Y')

        args = parser.parse_args()

        run(args)

        logging.info(f'✅ All tasks completed.')
    except Exception as e:
        logging.fatal(f'💥 {e.__class__.__name__} is the chief culprit!')
        raise e
