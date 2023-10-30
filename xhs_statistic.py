from core.dataset_manager import DatasetManager


def print_xhs_statistic():
    print(f'Dataset (Xiaohongshu) Statistic Result')
    print(f'Total: {DatasetManager.xhs_statistic()}')


if __name__ == '__main__':
    print_xhs_statistic()
