from sqlalchemy import create_engine
import json
from snowflake.snowpark import Session

# Define your Snowflake connection parameters
connection_parameters = json.load(open('./sf_connection_config.json'))

def read_dag():
    with open("./dag.json", "r") as file:
        return json.load(file)['commands']

# Create a SQLAlchemy engine
# makes account usage dummy table 
def make_tables(type='make_object_dependencies_dummy'):
    engine = create_engine(f"snowflake://{connection_parameters['user']}:{connection_parameters['password']}@{connection_parameters['account']}/{connection_parameters['database']}/{connection_parameters['schema']}?warehouse={connection_parameters['warehouse']}&role={connection_parameters['role']}")
    dic = read_dag()
    with engine.connect() as connection:
        for d in dic:
            ddl = d['ddl']
            
            if d['type']==type:
                connection.execute(ddl)





import pandas as pd 

def read_csv(table_name='object_dependencies'):
    df= pd.read_csv(f'{table_name}.csv', sep='|', quoting=1, quotechar='"')
    df['TGT'] = df['REFERENCING_DATABASE']+'__'+df['REFERENCING_SCHEMA']+'__'+df['REFERENCING_OBJECT_NAME']
    df['SRC'] = df['REFERENCED_DATABASE']+'__'+df['REFERENCED_SCHEMA']+'__'+df['REFERENCED_OBJECT_NAME']

    df['REF']='(r)'
    # make a tree 
    tree= df[['SRC','TGT','REF']].values.tolist()
    

    return df ,tree

### # make dummy object dep table on sf     
### make_tables()
### 
# 
# 
# # read it to csv like you would
### 
# 
# 
# read_sf()


import random 

    
    
    
def generate_tree(num_nodes=10):
    dag = [(0, 1)]
    for i in range(2, num_nodes):
        parent = random.choice([tup[1] for tup in dag])
        dag.append((parent, i))
    return dag
    
    

#def print_tree(node, edges, indent=''):
#    children = [edge[1] for edge in edges if edge[0] == node]
#    if children:
#        last_child = children[-1]
#    for child in children:
#        if child == last_child:
#            print(indent + '└── ' + str(child))
#            print_tree(child, edges, indent + '    ')
#        else:
#            print(indent + '├── ' + str(child))
#            print_tree(child, edges, indent + '│   ')
            

#def print_tree(node, edges, indent=''):
#    tree_str = ''
#    children = [edge[1] for edge in edges if edge[0] == node]
#    if children:
#        last_child = children[-1]
#    for child in children:
#        if child == last_child:
#            tree_str += indent + '└── ' + str(child) + '\n'
#            tree_str += print_tree(child, edges, indent + '    ')
#        else:
#            tree_str += indent + '├── ' + str(child) + '\n'
#            tree_str += print_tree(child, edges, indent + '│   ')
#    return tree_str




#def print_tree(node, edges, indent='', is_root=True):
#    tree_str = f'{indent}{node}\n' if is_root else ''
#    children = [edge[1] for edge in edges if edge[0] == node]
#    for child in children:
#        if child == children[-1]:  # last child
#            tree_str += indent + '└── ' + str(child) + '\n'
#            tree_str += print_tree(child, edges, indent + '    ', is_root=False)
#        else:
#            tree_str += indent + '├── ' + str(child) + '\n'
#            tree_str += print_tree(child, edges, indent + '│   ', is_root=False)
#    return tree_str
#

def print_tree_from_root(node, edges, indent='', is_root=True):
    tree_str = f'{indent}{node}\n' if is_root else ''
    children = [(edge[1], edge[2]) for edge in edges if edge[0] == node]
    for i, (child, ref_type) in enumerate(children):
        if i == len(children) - 1:  # last child
            tree_str += indent + '└──>' + f'{child} ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_root(child, edges, indent + '    ', is_root=False)
        else:
            tree_str += indent + '├──>' + f'{child} ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_root(child, edges, indent + '│   ', is_root=False)
    return tree_str


def print_tree_from_leaf(node, edges, indent='', is_root=True):
    tree_str = f'{indent}{node}\n' if is_root else ''
    parents = [(edge[0], edge[2]) for edge in edges if edge[1] == node]
    for i, (parent, ref_type) in enumerate(parents):
        if i == len(parents) - 1:  # last parent
            tree_str += indent + '└<──' + f'{parent} ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_leaf(parent, edges, indent + '    ', is_root=False)
        else:
            tree_str += indent + '├<──' + f'{parent} ( {ref_type} )' + '\n'
            tree_str += print_tree_from_leaf(parent, edges, indent + '│   ', is_root=False)
    return tree_str


def generate_dag_sql(tree):
    l=[]
    d= lambda src,tgt: {
        "type": "make_object_dependencies_dummy",
        "name": "insert3",
        "ddl": f"""INSERT INTO object_dependencies VALUES ('database1', 'schema1', '{src}', 3, 'table', 'database1', 'schema1', '{tgt}', 4, 'table', 'DEPENDENCY')"""
      }    
    
    # make create table 
    l.append({
        "type": "make_object_dependencies_dummy",
        "name": "create_table",
        "ddl": f"""CREATE OR REPLACE TABLE object_dependencies (REFERENCED_DATABASE STRING, REFERENCED_SCHEMA STRING, REFERENCED_OBJECT_NAME STRING, REFERENCED_OBJECT_ID INTEGER, REFERENCED_OBJECT_TYPE STRING, REFERENCING_DATABASE STRING, REFERENCING_SCHEMA STRING, REFERENCING_OBJECT_NAME STRING, REFERENCING_OBJECT_ID INTEGER, REFERENCING_OBJECT_TYPE STRING, EDGE_TYPE STRING)"""
      })
    
    # make root 
    for edge in tree:
        src = 'table' + str(edge[0])
        tgt = 'table' + str(edge[1])
        l.append(d(src, tgt))

    with open('dag.json', 'w') as file:
        json.dump({"commands":l}, file, indent=4)    





def read_sf(table_name='object_dependencies',ref_col='EDGE_TYPE'):
    session = Session.builder.configs(connection_parameters).create()
# query sf to df 
    df=session.sql(f"select * from {table_name}").to_pandas()
    df['SRC']=df['REFERENCED_DATABASE']+'__'+df['REFERENCED_SCHEMA']+'__'+df['REFERENCED_OBJECT_NAME']
    df['TGT']=df['REFERENCING_DATABASE']+'__'+df['REFERENCING_SCHEMA']+'__'+df['REFERENCING_OBJECT_NAME']
    df['REF']='' if ref_col is None else df[ref_col]
    df.to_csv(f'{table_name}.csv',index=False,header=True,sep='|',quoting=1,quotechar='"')
    tree= df[['SRC','TGT','REF']].values.tolist()
    return df ,tree 



### tree = generate_tree()
### generate_dag_sql(tree)
### print_tree(0, tree)
### ### # make dummy object dep table on sf     
### make_tables()

df,tree=read_csv()


def count_descendants(node, tree):
    children = [edge[1] for edge in tree if edge[0] == node]
    count = len(children)
    for child in children:
        count += count_descendants(child, tree)
    return count

#finds roots and counts descendants
def find_roots(tree):
    children = [edge[1] for edge in tree]
    roots = []
    descendants_count = {}
    for edge in tree:
        if edge[0] not in children:
            roots.append(edge[0])
            descendants_count[edge[0]] = count_descendants(edge[0], tree)
    return roots, descendants_count


def count_ancestors(node, tree):
    parents = [edge[0] for edge in tree if edge[1] == node]
    count = len(parents)
    for parent in parents:
        count += count_ancestors(parent, tree)
    return count

# finds leafs and counts ancestors
def find_leafs(tree):
    parents = [edge[0] for edge in tree]
    leafs = []
    ancestors_count = {}
    for edge in tree:
        if edge[1] not in parents:
            leafs.append(edge[1])
            ancestors_count[edge[1]] = count_ancestors(edge[1], tree)
    return leafs, ancestors_count

df,tree=read_sf()
roots,desc=find_roots(tree)

leafs,parents=find_leafs(tree)
print(parents)

s=print_tree_from_root(roots[0], tree)
print(s)

s=print_tree_from_leaf(leafs[-1], tree)

print(s)