import os
import graphscope
from graphscope.framework.loader import Loader
import sys
import time

def run(output_path):

    graphscope.set_option(show_log=True)
    sess = graphscope.session(num_workers=10,k8s_vineyard_mem="20G")

    graph = sess.g(directed=False)
    d3 = Loader("hdfs://10.58.16.185:8020/yuntu_perf/dg_e_csv/part")
    graph = graph.add_edges(d3,label='likes', src_label='person', dst_label='person')

    res_louvain = graphscope.louvain(graph, min_progress=1000, progress_tries=1)
    res_louvain.output("hdfs://10.58.16.185:8020/" + output_path, {"node": "v.id", "result": "r"})
    sess.close()

if __name__ == "__main__":
    start_time = time.time()
    output_path = sys.argv[1]
    print(output_path)
    run(output_path)
    end_time = time.time()
    print("Duration time = " + str(end_time - start_time))
