import os
import json
import sqlparse
from sqlparse.tokens import Keyword, DML, DDL
from sqlparse.sql import IdentifierList, Identifier, Function

# Extracts relations between tables for mapping/graphing
def get_relations(path):
    
    def is_subselect(parsed):
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is DML and item.value.upper() == 'SELECT':
                return True
        return False


    def extract_from_part(parsed):
#         print('instanceID: ' + str(round(random.random()*100)))
        from_seen = False
        for item in parsed.tokens:
            if item.is_group:
                if ( isinstance(item, Identifier) and isinstance(item.tokens[0], Function) ):
                    if item.tokens[0].get_name().upper() in ['EXTRACT']:
                        continue
                    else:
                        for x in extract_from_part(item):
                            yield x
                else:
                    for x in extract_from_part(item):
                        yield x
            if from_seen:
                if is_subselect(item):
                    for x in extract_from_part(item):
                        yield x
                elif item.ttype is Keyword and item.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING', 'UNION', 'ON', 'USING']:
                    from_seen = False
                    StopIteration
                else:
                    yield item
            if item.ttype is Keyword and item.value.upper() in ['FROM', 'JOIN']:
                from_seen = True


    def extract_table_identifiers(token_stream):
        for item in token_stream:
            if isinstance(item, IdentifierList):
                for identifier in item.get_identifiers():
                    value = identifier.value.replace('"', '').lower()
                    yield value
            elif isinstance(item, Identifier):
                value = item.value.replace('"', '').lower()
                if not 'select' in value:
                    value = value[:value.index(' ')] if ' ' in value else value
                    yield value


    def extract_build_name(parsed):
        tokens = parsed.tokens
        modify_seen = False
        for item in tokens:
            if ( item.ttype is DDL and item.value.upper() in ['CREATE', 'UPDATE'] ) or \
                        ( item.ttype is DML and item.value.upper() == 'INSERT' ):
                modify_seen = True
            if modify_seen == True and isinstance(item, Identifier):
                for value in item:
#                     print(item)
#                     return item.get_real_name()
                    return item.get_parent_name() + '.' + item.get_real_name()
            else: continue


    def extract_tables(sql):
        # let's handle multiple statements in one sql string
        extracted_tables = {}
        statements = list(sqlparse.parse(sql))
        for statement in statements:
            build_name = extract_build_name(statement)
            if statement.get_type() != 'UNKNOWN' and build_name:
                stream = extract_from_part(statement)
                extracted_tables[build_name] = list(set(list(extract_table_identifiers(stream))))
        return extracted_tables

    
    sql = ' '.join([open(path + f).read() for f  in os.listdir(path) if f[-3:] == 'sql'])
    
    return extract_tables(sql)

# OBS get_relations methods
#def getrefs(q):
#    from_clauses = re.findall('from [\w._]* ', q, flags=re.IGNORECASE)
#    join_clauses = re.findall('join [\w._]* ', q, flags=re.IGNORECASE)
#    join_and_from = list(set([f[5:-1] for f in from_clauses] + [f[5:-1] for f in join_clauses]))
#    refs = [r for r in join_and_from if '.' in r]
#    return refs


#def get_relations(path):
#    filenames = [f for f  in os.listdir(path) if f[-3:] == 'sql']
#    relations = {}
#    for fname in filenames:
#        q = open(path + fname).read()
#        relations['quality.qlab_' + fname[:-4]] = getrefs(q)
#    return relations


# Position Nodes in Diagram
def get_coords():
    
    def next_gen(gen_num):
        parents = [t for t in node_names if generations[t] == gen_num - 1]
        all_children = []
        for p in parents:
            for child,pars in relations.items():
                if p in pars:
                    all_children.append(child)
        gen_children = []
        for c in all_children:
            if None not in [generations[p] for p in relations[c]]:
                gen_children.append(c)
        gen_children = list(set(gen_children))
        for c in gen_children:
            generations[c] = gen_num
    #     return gen_children
        return all_children

    # building generations dict ------------
    generations = {t:None for t in node_names}
    
    no_parents = []
    for t in node_names:
        if t not in relations.keys():
            no_parents.append(t)
        elif relations[t] == []:
            no_parents.append(t)
    for t in no_parents:
        generations[t] = 0
            
    i = 1
    while True:
        gen = next_gen(i)
        if gen == []:
            break
        else: i += 1
    # ---------------------------
            
    gen_pivot = {}
    for g in set(generations.values()):
        gen_pivot[g] = [t.encode("utf-8") for t,gen in generations.items() if gen == g]
        gen_pivot[g].sort()

    # building coords dict
    coords = {}
    for k,v in generations.items():
        coords[k] = (
            v * 300,
            gen_pivot[v].index(k) * 45
        )
    return coords


def gen_diagram(path):
    global node_names, relations
    
    # Generate nodes and edges jsons
    relations = get_relations(path)
    
    node_names = relations.keys()
    for n in relations.keys():
        node_names += relations[n]
    node_names = list(set(node_names))
    
    coords = get_coords()
    
    nodes = []
    for i,n in enumerate(node_names):
        nodes.append({'id':i, 'label':n, 'x':coords[n][0], 'y':coords[n][1]})
        nodes_json = json.dumps(nodes)
        
    edges = []
    for n,rels in relations.items():
        for t in rels:
            edges.append({'from':node_names.index(t), 'to':node_names.index(n)})
    edges_json = json.dumps(edges)
    
    
    network_diagram_script = """
        // create an array with nodes
        var nodes = new vis.DataSet(""" + nodes_json + """);
    
        // create an array with edges
        var edges = new vis.DataSet(""" + edges_json + """);
    
        // create a network
        var container = document.getElementById('mynetwork');
    
        // provide the data in the vis format
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {
            physics: {enabled: false},
            edges: {arrows: 'to', smooth: {enabled: false}},
            layout: {
                randomSeed: undefined,
                improvedLayout:true,
                hierarchical: {enabled:false}
            }
        };
    
        // initialize your network!
        var network = new vis.Network(container, data, options);
    """
    
    network_diagram = """
    <html>
    <head>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    
        <style type="text/css">
            #mynetwork {
                width: 800px;
                height: 700px;
                border: 1px solid lightgray;
            }
        </style>
    </head>
    <body>
    <div id="mynetwork"></div>
    
    <script type="text/javascript">
    """ + network_diagram_script + """
    </script>
    </body>
    </html>
    """
    
    with open('network_diagram.html', 'w') as nd:
        nd.write(network_diagram)
            
    return network_diagram