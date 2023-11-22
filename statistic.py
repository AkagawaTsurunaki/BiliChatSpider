from bili_statistic import print_bili2_statistic
from xhs_statistic import print_xhs_statistic

if __name__ == '__main__':
    total_bili, leaf_nodes_count_bili = print_bili2_statistic()
    total_xhs, leaf_nodes_count_xhs = print_xhs_statistic()
    print(f'Total Dataset Statistic')
    print(f'Total nodes: {total_bili+total_xhs}')
    print(f'Leaf nodes count: {leaf_nodes_count_bili + leaf_nodes_count_xhs}')
