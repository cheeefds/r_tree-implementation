def show_rtree(root,level = 0):
    if root is None:
        return
    print("Level", level, ":", end=" ")
    for entry in root.children:
        if entry.is_leaf_entry():
            print(entry.mbr,entry.data, end=" ")
            
        else:
            print(entry.mbr, f"Node({len(entry.child.children)})", end=" ")
    print()
    for entry in root.children:
        if entry.child is not None:
            show_rtree(entry.child, level + 1)