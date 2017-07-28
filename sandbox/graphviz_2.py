# Based on http://matthiaseisen.com/articles/graphviz/

import graphviz as gv


styles = {
    'graph': {
        'fontname' : 'sans',
        'fontsize': '16',
        'fontcolor': 'black',
        'bgcolor': '#dddddd',
        'rankdir': 'LR',
        'margin': '20',
    },
    'nodes': {
        'fontname': 'sans',
        'fontsize': '10',
        'shape': 'box',
        #'fontcolor': 'white',
        #'color': '#006699',
        #'style': 'filled',
        #'fillcolor': '#006699',
        #'margin': '0.4',
    },
    'edges': {
        'style': 'solid',
        'color': 'green',
        'arrowhead': 'open',
        'fontname': 'sans',
        'fontsize': '8',
        'fontcolor': 'black',
    }
}


def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph


def add_switch_node(graph, name, model=' ', ip=' '):
    graph.node(name, shape='none', margin='0',
           label="""<
<table border="0" cellborder="1" cellpadding="7" cellspacing="0">
<tr>
<td bgcolor="#006699">
<font color="#ffffff"><b>"""+name+"""</b></font>
</td>
</tr><tr>
<td bgcolor="#ffffff">
<font color="#000000">"""+ip+"""</font>
</td>
</tr><tr>
<td bgcolor="#ffffff">
<font color="#000000">"""+model+"""</font>
</td>
</tr>
</table>>""")


def draw_topology(topology_dict, output_filename='img/topology'):
    nodes = set([key[0] for key in list(topology_dict.keys()) + list(topology_dict.values())])

    g1 = gv.Graph(format='svg')
    g1 = apply_styles(g1, styles)

    with g1.subgraph(name='cluster-core') as c:
        c = apply_styles(c, styles)
        c.attr(rank='same', label='Core')

        add_switch_node(c, 'sss-core-digi', ip='192.168.100.17')
        add_switch_node(c, 'sss-core-main', ip='192.168.100.7')

        c.edge('sss-core-digi', 'sss-core-main', headlabel='D8', taillabel='D1')

    with g1.subgraph(name='cluster-powell') as c:
        c = apply_styles(c, styles)
        c.attr(rankdir='LR', label='Powell House')

        add_switch_node(c, 'sss-hse-powell-1', ip='192.168.100.59')
        add_switch_node(c, 'sss-hse-powell-2', ip='192.168.100.55')
        add_switch_node(c, 'sss-hse-powell-3', ip='192.168.100.82')
        add_switch_node(c, 'sss-hse-powell-4', ip='192.168.100.58')

    for key, value in list(topology_dict.items()):
        head, t_label = key
        tail, h_label = value
        g1.edge(head, tail, headlabel=h_label, taillabel=t_label, label=" "*12)
        # headport='nw' tailport='s'

    print(g1.source)
    filename = g1.render(filename=output_filename)
    print("Graph saved in", filename)

diag5 = {('sss-core-digi', 'D2'): ('sss-hse-powell-1', 'A1'),
         ('sss-hse-powell-1', '41'): ('sss-hse-powell-2', '50'),
         ('sss-core-main', 'B22'): ('sss-hse-powell-3', '52'),
         ('sss-hse-powell-3', '49'): ('sss-hse-powell-4', '48')}

draw_topology(diag5)