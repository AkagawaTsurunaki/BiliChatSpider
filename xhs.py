import argparse
import logging
import time

from core.dataset_manager import DatasetManager
from xiaohongshu import multitask_spider

if __name__ == '__main__':

    channels = dict()
    channels['recommend'] = 'homefeed_recommend'
    channels['fashion'] = 'homefeed.fashion_v3'
    channels['food'] = 'homefeed.food_v3'
    channels['cosmetics'] = 'homefeed.cosmetics_v3'
    channels['movie_and_tv'] = 'homefeed.movie_and_tv_v3'
    channels['career'] = 'homefeed.career_v3'
    channels['love'] = 'homefeed.love_v3'
    channels['household_product'] = 'homefeed.household_product_v3'
    channels['gaming'] = 'homefeed.gaming_v3'
    channels['travel'] = 'homefeed.travel_v3'
    channels['fitness'] = 'homefeed.fitness_v3'

    try:
        print('🍠 Xhs Chat Spider 🍠')
        print(f'''
        You can choose {[v for k, v in enumerate(channels)]}
        ''')
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Initialize arguments parser.
        parser = argparse.ArgumentParser(prog='Xhs Chat Spider',
                                         description='A spider script which can collect replies from Xiaohongshu.',
                                         epilog=''
                                         )
        parser.add_argument('-i', '--ids', nargs='+', type=str)
        parser.add_argument('-ch', '--channel', type=str)
        parser.add_argument('-cls', '--clazz', type=str)
        parser.add_argument('-thr', '--threshold', type=int)

        args = parser.parse_args()

        if args.ids is None and args.channel is None and args.clazz is None:
            print('No arguments were input.')
            exit(0)

        pre_total, _ = DatasetManager.xhs_statistic()
        start_time = time.time()

        if args.ids is not None and args.clazz is not None:
            multitask_spider.collect_by_post_id_list(args.clazz, args.ids)

        if args.ids is None and args.channel is not None and args.clazz is not None:
            multitask_spider.collect_by_channel_id(cls=args.clazz, channel_id=channels[args.channel], task_count=8)

        end_time = time.time()
        elapsed_time = end_time - start_time
        cur_total, _ = DatasetManager.xhs_statistic()
        delta = cur_total - pre_total

        logging.info(f'📊 {delta} records totally collected.')
        logging.info(f'⌛️ {elapsed_time} seconds costed.')
        logging.info(f'🛞 Average {delta / elapsed_time} records per second.')

        logging.info(f'✅ All tasks completed.')

    except Exception as e:
        logging.fatal(f'💥 {e.__class__.__name__} is the chief culprit!')
        raise e
