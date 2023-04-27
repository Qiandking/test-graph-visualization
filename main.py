import networkx as nx
import csv
import numpy as np
from matplotlib import pyplot as plt
def _get_pos_dict(idx) -> dict:
    postitonfile = ".\\Iridium_position_datas_" + str(idx) + ".csv"
    pos = {}
    with open(postitonfile) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)  # 读取第一行每一列的标题 跳过表头
        for row in csv_reader:  # 将csv 文件中的数据保存到data中
            position_list = str(row[0]).split()
            pos[int(position_list[0])] = (float(position_list[1]), float(position_list[2]), float(position_list[3]))
    return pos

def draw_graph(graph: nx.Graph) -> None:
    nodePos = nx.get_node_attributes(graph, 'pos')

    node_xyz = np.array([nodePos[v] for v in sorted(graph)])
    edge_xyz = np.array([(nodePos[u], nodePos[v]) for u, v in graph.edges()])
    # Create the 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the nodes - alpha is scaled by "depth" automatically
    ax.scatter(*node_xyz.T, s=100, ec="w")

    for i in range(len(nodePos)):
        ax.text(nodePos[i][0], nodePos[i][1], nodePos[i][2],i)
    # Plot the edges
    for vizedge in edge_xyz:
        ax.plot(*vizedge.T, color="tab:gray")

    # path_edges = []
    # for p in range(len(path) - 1):
    #     path_edges.append((pos[path[p]], pos[path[p + 1]]))
    # path_edge = np.array(path_edges)
    # for w in path_edge:
    #     ax.plot(*w.T, color="tab:red")

    def _format_axes(ax):
        """Visualization options for the 3D axes."""
        # Turn gridlines off
        ax.grid(False)
        # Suppress tick labels
        for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
            dim.set_ticks([])

        # Set axes labels
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    _format_axes(ax)
    fig.tight_layout()
    plt.axis('off')  # 去掉坐标轴
    plt.show()



def create_graph() -> nx.Graph:
    # idx = random.randint(0,59)
    # random.seed(0)
    # np.random.seed(0)
    idx = 0
    position = _get_pos_dict(idx)
    filepath = '.\\'
    file_name = "Iridium_link_datas_"
    filename = filepath + file_name + str(idx) + '.csv'
    G = nx.Graph()
    with open(filename) as csvfile:
        for i in range(66):
            G.add_node(i, pos=position[i])
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        header = next(csv_reader)  # 读取第一行每一列的标题 跳过表头
        for row in csv_reader:  # 将csv 文件中的数据保存到data中
            link_list = str(row[0]).split()

            G.add_edge(int(link_list[0]), int(link_list[1]), weight=eval(link_list[2]) / (3 * 10 ** 4),
                       capacity=200)
            # print(eval(link_list[2]) / (3 * 10 ** 4))
            # print(200)
        edges_num = G.number_of_edges()

    return G


def show_path(G, path):
    nodePos = nx.get_node_attributes(G,'pos')

    node_xyz = np.array([nodePos[v] for v in sorted(G)])
    edge_xyz = np.array([(nodePos[u], nodePos[v]) for u, v in G.edges()])
    # Create the 3D figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the nodes - alpha is scaled by "depth" automatically
    ax.scatter(*node_xyz.T, s=100, ec="w")
    for i in range(len(nodePos)):
        ax.text(nodePos[i][0], nodePos[i][1], nodePos[i][2], i)
    # Plot the edges
    for vizedge in edge_xyz:
        ax.plot(*vizedge.T, color="tab:gray")
    for i in path:
        path_edges = []
        for p in range(len(i) - 1):
            path_edges.append((nodePos[i[p]], nodePos[i[p + 1]]))
        path_edge = np.array(path_edges)
        for w in path_edge:
            ax.plot(*w.T, color="tab:red")

    def _format_axes(ax):
        """Visualization options for the 3D axes."""
        # Turn gridlines off
        ax.grid(False)
        # Suppress tick labels
        for dim in (ax.xaxis, ax.yaxis, ax.zaxis):
            dim.set_ticks([])
        # Set axes labels
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    _format_axes(ax)
    fig.tight_layout()
    plt.axis('off')  # 去掉坐标轴
    plt.show()
if __name__ == '__main__':
    graph = create_graph()
    draw_graph(graph)
    # path = nx.shortest_path(graph,5,13)
    # print(path)

    # print([p for p in nx.all_shortest_paths(graph, source=22, target=53) ])

    # show_path(graph, path)
    paths = []
    X = nx.shortest_simple_paths(graph, source=22, target=53)  # K 最短路径
    k = 5
    for counter, path in enumerate(X):
        # print(path)
        paths.append(path)
        if counter == k - 1:
            break
    show_path(graph,paths)

