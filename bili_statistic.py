from core.dataset_manager import DatasetManager


def print_bili2_statistic():
    print(f'Dataset (Bilibili) Statistic Result')
    print(f'Total: {DatasetManager.bili2_statistic()}')


if __name__ == '__main__':
    print_bili2_statistic()
