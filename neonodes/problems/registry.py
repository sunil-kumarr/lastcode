TOPICS = ["all", "grid", "tree", "graph", "array", "string", "dp"]
DIFFICULTIES = ["all", "easy", "medium", "hard"]

PROBLEMS = [
    {"id": "count_islands",     "title": "Count Islands",                  "topic": "grid",   "difficulty": "medium", "renderer": "grid",  "available": True},
    {"id": "number_of_islands", "title": "Number of Islands II",           "topic": "grid",   "difficulty": "hard",   "renderer": "grid",  "available": False},
    {"id": "bt_inorder",        "title": "Binary Tree Inorder Traversal",  "topic": "tree",   "difficulty": "easy",   "renderer": "tree",  "available": True},
    {"id": "bt_preorder",       "title": "Binary Tree Preorder Traversal", "topic": "tree",   "difficulty": "easy",   "renderer": "tree",  "available": True},
    {"id": "bt_postorder",      "title": "Binary Tree Postorder Traversal", "topic": "tree",  "difficulty": "easy",   "renderer": "tree",  "available": True},
    {"id": "bt_max_depth",      "title": "Maximum Depth of Binary Tree",   "topic": "tree",   "difficulty": "easy",   "renderer": "tree",  "available": True},
    {"id": "bt_path_sum",       "title": "Binary Tree Path Sum",           "topic": "tree",   "difficulty": "easy",   "renderer": "tree",  "available": True},
    {"id": "bt_level_order",    "title": "Binary Tree Level Order BFS",    "topic": "tree",   "difficulty": "medium", "renderer": "tree",  "available": False},
    {"id": "two_sum",           "title": "Two Sum",                        "topic": "array",  "difficulty": "easy",   "renderer": "array", "available": True},
    {"id": "merge_intervals",   "title": "Merge Intervals",                "topic": "array",  "difficulty": "medium", "renderer": "array", "available": False},
    {"id": "valid_parens",      "title": "Valid Parentheses",              "topic": "string", "difficulty": "easy",   "renderer": "array", "available": True},
    {"id": "dijkstra",          "title": "Dijkstra Shortest Path",         "topic": "graph",  "difficulty": "medium", "renderer": "graph", "available": False},
    {"id": "bfs_graph",         "title": "Graph BFS",                      "topic": "graph",  "difficulty": "easy",   "renderer": "graph", "available": True},
    {"id": "lcs",               "title": "Longest Common Subsequence",     "topic": "dp",     "difficulty": "medium", "renderer": "dp",    "available": False},
]

# Map renderer name → module path for dynamic loading
RENDERER_MAP = {
    "grid":  "neonodes.renderers.grid.GridRenderer",
    "tree":  "neonodes.renderers.tree.TreeRenderer",
    "array": "neonodes.renderers.array.ArrayRenderer",
    "graph": "neonodes.renderers.graph.GraphRenderer",
    "dp":    "neonodes.renderers.tree.TreeRenderer",  # stub
}

# Map problem id → module path for dynamic loading
PROBLEM_MAP = {
    "count_islands": "neonodes.problems.count_islands",
    "bt_inorder":    "neonodes.problems.bt_inorder",
    "bt_preorder":   "neonodes.problems.bt_preorder",
    "bt_postorder":  "neonodes.problems.bt_postorder",
    "bt_max_depth":  "neonodes.problems.bt_max_depth",
    "bt_path_sum":   "neonodes.problems.bt_path_sum",
    "two_sum":       "neonodes.problems.two_sum",
    "valid_parens":  "neonodes.problems.valid_parens",
    "bfs_graph":     "neonodes.problems.bfs_graph",
}
