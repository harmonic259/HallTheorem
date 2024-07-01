x_vertices = set(input('Enter X part vertices (space seperated):\n').split())
y_vertices = set(input('Enter Y part vertices (space seperated):\n').split())

# Input edges of the graph
edges = []
edge_list_input = input('Enter edges in format "v1,v2" space seperated (example: a,b c,d a,c):\n').split()
for edge in edge_list_input:
   a, b = edge.split(',')
   edges.append((a, b))

# Input initial matching 
init_matching = set()
init_matching_list_input = input('Enter initial matches in format "v1,v2" space seperated (example: a,b c,d a,c):\n').split()
for match in init_matching_list_input:
   a, b = match.split(',')
   init_matching.add(frozenset({a, b}))

# Creating adjacency map of vertex to neigbors by edges   
adjacency = dict()
for edge in edges:
    a = edge[0]
    b = edge[1]
    if a not in adjacency:
        adjacency[a] = {}
    if b not in adjacency:
        adjacency[b] = {}
    adjacency.update({a : {b}.union(adjacency[a])})
    adjacency.update({b : {a}.union(adjacency[b])})
    
  
# The function that takes a set of vertices of the graph and returns union of their neighbors  
def N(x):
    s = set()
    for v in x:
        s = s.union(adjacency[v])
    return s

# The function takes a matching and some vertices as input and returns vertices that match input vertices by the input matching
def M(matches, vertices):
    s = set()
    for match in matches:
        a, b = list(match)
        if a in vertices:
            s.add(b)
        elif b in vertices:
            s.add(a)
    return s

# First initilize crrunt matching and update it in each outer loop until all X vertices covered
curr_matching = init_matching
while x_vertices.difference(M(curr_matching, y_vertices)) != set():
    # Finding a vertex u in X, not coveered by current matching
    u = list(x_vertices.difference(M(curr_matching, y_vertices)))[0]
    y_list = [] # List of Y_i s
    x_list = [{u}]
    
    # Finding a vertex v in Y, not covered by current matching but has a path to u by matching vertices   
    while N(x_list[-1]).difference(M(curr_matching, x_vertices)) == set(): # Continue the loop until N(M(Y_k)) - Y' != {} 
        #Y_k = N(M(Y_(k-1))) - Union_(0 < i < k) [(Y_i)]
        y_list_union = set()
        for s in y_list:
            y_list_union = y_list_union.union(s)
        y_list.append(N(x_list[-1]).difference(y_list_union))
        x_list.append(M(curr_matching, y_list[-1]))
        
    v = list(N(x_list[-1]).difference(M(curr_matching, x_vertices)))[0]
    
    deleted_match_list = []
    added_match_list = []
    
    # Finding a path from v to u (vertex in Y not covered by current matching)
    curr_y_vertex = v
    curr_x_vertex = list(N(v).intersection(x_list[-1]))[0]
    added_match_list.append(frozenset({curr_x_vertex, curr_y_vertex}))
    x_list.pop()
    x_list.reverse()
    
    # Making a list of edges in the founded path, that must be deleted from or added to the matching
    for xset in x_list:
        curr_y_vertex = list(M(curr_matching, {curr_x_vertex}))[0]
        deleted_match_list.append(frozenset({curr_x_vertex, curr_y_vertex}))
        curr_x_vertex = list(N({curr_y_vertex}).intersection(xset))[0]
        added_match_list.append(frozenset({curr_x_vertex, curr_y_vertex}))
        
    # Deleting the edges in deleted_match_list from the current matching and
    # Adding the edges of added_match_list to the current matching
    # To update the current matching by incrementing its size
    while len(deleted_match_list) != 0:
        curr_matching.add(added_match_list.pop())
        curr_matching.remove(deleted_match_list.pop())
        
    curr_matching.add(added_match_list.pop())
  
# Printing the final matching determined by the algorithm (which covers all vertices in X)
print('Final matching is: | ', end='')
c_match = 1  
for match in curr_matching:
    a, b = list(match)
    print(f'Match{c_match}: ({a},{b}) | ', end='')
    c_match += 1

        
    
        
        
        
   
   


