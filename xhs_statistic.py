from core.dataset_manager import DatasetManager


def print_xhs_statistic():
    print(f'Dataset (Xiaohongshu) Statistic Result')
    total, leaf_nodes_count = DatasetManager.xhs_statistic()
    print(f'Total nodes: {total}')
    print(f'Leaf nodes count: {leaf_nodes_count}')


if __name__ == '__main__':
    print_xhs_statistic()
