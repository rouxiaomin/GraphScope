import os
import graphscope
from graphscope.framework.loader import Loader
import sys


def run(output_path):
    k8s_volumes = {
        "data": {
            "type": "hostPath",
            "field": {
                "path": os.path.expanduser("/perf_data"),
                "type": "Directory"
            },
            "mounts": {
                "mountPath": "/perfdata"
            }
        }
    }

    graphscope.set_option(show_log=True)
    sess = graphscope.session(k8s_volumes=k8s_volumes, k8s_vineyard_mem="10G", num_workers=10)

    graph = sess.g(directed=False)
    graph = graph.add_edges('/perfdata/part-00000-e8c33886-0250-49b0-8e51-c97aaa96f431-c000.csv', label='likes',
                            src_label='person', dst_label='person')

    res_louvain = graphscope.louvain(graph, min_progress=1000, progress_tries=1)
    res_louvain.output("hdfs://10.58.16.185:8020/" + output_path, {"node": "v.id", "result": "r"})


if __name__ == "__main__":
    output_path = sys.argv[1]
    print(output_path)
    run(output_path)
