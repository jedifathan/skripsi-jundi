from pycallgraph2 import PyCallGraph
from pycallgraph2.output import GraphvizOutput
import main

def generate_call_graph():
    config = {
        "group_functions": True,
        "font_size": 10,
    }

    graphviz = GraphvizOutput(output_file="flow_graph.png", **config)

    with PyCallGraph(output=graphviz):
        main.main()

if __name__ == "__main__":
    generate_call_graph()
