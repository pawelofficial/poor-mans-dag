import json
from snowflake.snowpark import Session
import pandas as pd 

# read connection parameters from file 
connection_parameters=json.load(open('./sf_connection_config.json'))



# read object_dependencies from snowflake 
def read_sf(table_name='object_dependencies',ref_col='REF',fp=''):
    session = Session.builder.configs(connection_parameters).create()
    df=session.sql(f"select *, 'foo' as REF from {table_name}").to_pandas()
    df['SRC']=df['REFERENCED_DATABASE']+'__'+df['REFERENCED_SCHEMA']+'__'+df['REFERENCED_OBJECT_NAME']
    df['TGT']=df['REFERENCING_DATABASE']+'__'+df['REFERENCING_SCHEMA']+'__'+df['REFERENCING_OBJECT_NAME']
    df['REF']='' if ref_col is None else df[ref_col]
    df.to_csv(f'{fp}{table_name}.csv',index=False,header=True,sep='|',quoting=1,quotechar='"')
    tree= df[['SRC','TGT','REF']].values.tolist()
    return df ,tree 

def read_csv(fp='./static/data/',table_name='object_dependencies'):
    df=pd.read_csv(f'{fp}{table_name}.csv',sep='|',quoting=1,quotechar='"')
    tree= df[['SRC','TGT','REF']].values.tolist()
    return df ,tree


#finds roots and counts descendants
def find_roots(tree):
    def count_descendants(node, tree):
        children = [edge[1] for edge in tree if edge[0] == node]
        count = len(children)
        for child in children:
            count += count_descendants(child, tree)
        return count
    
    children = [edge[1] for edge in tree]
    roots = []
    descendants_count = {}
    for edge in tree:
        if edge[0] not in children:
            roots.append(edge[0])
            descendants_count[edge[0]] = count_descendants(edge[0], tree)
    return roots, descendants_count


# finds leafs and counts ancestors
def find_leafs(tree):
    def count_ancestors(node, tree):
        parents = [edge[0] for edge in tree if edge[1] == node]
        count = len(parents)
        for parent in parents:
            count += count_ancestors(parent, tree)
        return count
    parents = [edge[0] for edge in tree]
    leafs = []
    ancestors_count = {}
    for edge in tree:
        if edge[1] not in parents:
            leafs.append(edge[1])
            ancestors_count[edge[1]] = count_ancestors(edge[1], tree)
    return leafs, ancestors_count


def print_tree_from_root(node, edges, indent='', is_root=True):
    tree_str = f'*{indent}{node}*\n' if is_root else ''
    children = [(edge[1], edge[2]) for edge in edges if edge[0] == node]
    for i, (child, ref_type) in enumerate(children):
        if i == len(children) - 1:  # last child
            tree_str += indent + '└──>*' + f'{child}* ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_root(child, edges, indent + '    ', is_root=False)
        else:
            tree_str += indent + '├──>*' + f'{child}* ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_root(child, edges, indent + '│   ', is_root=False)
    return tree_str


def print_tree_from_leaf(node, edges, indent='', is_root=True):
    tree_str = f'*{indent}{node}*\n' if is_root else ''
    parents = [(edge[0], edge[2]) for edge in edges if edge[1] == node]
    for i, (parent, ref_type) in enumerate(parents):
        if i == len(parents) - 1:  # last parent
            tree_str += indent + '└<──*' + f'{parent}* ( {ref_type} ) ' + '\n'
            tree_str += print_tree_from_leaf(parent, edges, indent + '    ', is_root=False)
        else:
            tree_str += indent + '├<──*' + f'{parent}* ( {ref_type} )' + '\n'
            tree_str += print_tree_from_leaf(parent, edges, indent + '│   ', is_root=False)
    return tree_str


def save_string_to_file(s,fp='./tree.txt'):
    with open(fp, 'w',encoding="utf-8" ) as f:
        f.write(s)
    
    
def wrap_in_html(s):
    return f'<html><body><pre>{s}</pre></body></html>'


if __name__ == '__main__':
    df,tree=read_sf()
    
    roots,desc=find_roots(tree)

    s=print_tree_from_root(roots[0], tree)
    print(s)
    
    leafs,ancestors_count=find_leafs(tree)
    
    for l in leafs:
        print(l)
        s=print_tree_from_leaf(l, tree)
        print(s)
