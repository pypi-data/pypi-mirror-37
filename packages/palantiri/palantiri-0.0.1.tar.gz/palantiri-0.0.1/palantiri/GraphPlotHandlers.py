from palantiri.BasePlotHandlers import PlotHandler

import networkx as nx

import plotly.graph_objs as go
from plotly.offline import iplot


class GraphPlotHandler(PlotHandler):

    def __init__(self, graph, **params):
        self._graph = graph

        super(GraphPlotHandler, self).__init__(**params)

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph

    def _get_edge_trace(self, pos):
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in self.graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        return edge_trace

    def _get_node_trace(self, pos):
        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='none',
            marker=dict(
                showscale=False,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=17,
                line=dict(width=2)))

        for node, node_data in self.graph.nodes(data=True):
            x, y = pos[node]

            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        return node_trace

    def plot_graph(self, pos=None):

        if not pos:
            pos = nx.spring_layout(self._graph)

        data = [self._get_edge_trace(pos), self._get_node_trace(pos)]
        iplot(go.Figure(data=data))
