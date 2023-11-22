from core.dataset_manager import DatasetManager


def print_bili2_statistic():
    print(f'Dataset (Bilibili) Statistic Result')
    total, leaf_nodes_count = DatasetManager.bili2_statistic()
    print(f'Total nodes: {total}')
    print(f'Leaf nodes count: {leaf_nodes_count}')
    return total, leaf_nodes_count


if __name__ == '__main__':
    print_bili2_statistic()
