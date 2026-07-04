def show_rtree(root,level = 0):
    if root is None:
        return
    print("Level", level, ":", end=" ")
    for entry in root.children:
        if entry.is_leaf_entry():
            print(entry.data, end=" ")
            
        else:
            print(f"Node({len(entry.child.children)})", end=" ")
    print()
    for entry in root.children:
        if entry.child is not None:
            show_rtree(entry.child, level + 1)
    
    
def show_rtree_mbr(root,level = 0):
    if root is None:
        return
    print("Level", level, ":", end=" ")
    for entry in root.children:
        if entry.is_leaf_entry():
            print(f"MBR:{entry.mbr},Data", end=" ")
        else:
            print(f"MBR:{entry.mbr},Link", end=" ")
    print()
    for entry in root.children:
        if entry.child is not None:
            show_rtree_mbr(entry.child, level + 1)

