from Nodes import Entry, Node
from utils import area, Enlargement, union, PickSeeds, PickNext


class RTree:

    def __init__(self, maxentries=5, minentries=3):
        self.maxentries = maxentries
        self.minentries = minentries
        self.root = self.create_node(is_leaf = True)

    def create_node(self, is_leaf=True, parent=None):
        node = Node(is_leaf, parent)
        return node

    def create_entry(self, mbr, child=None, data=None):
        return Entry(mbr, child, data)

    # -------------------------
    # ChooseLeaf
    # -------------------------
    def ChooseLeaf(self, node, entry):
        if node.is_leaf:
            return node

        best_child = []
        for c in node.children:
            diff = Enlargement(c.mbr, entry.mbr)
            best_child.append((diff, area(c.mbr), c))

        best_child.sort(key=lambda x: (x[0], x[1]))

        return self.ChooseLeaf(best_child[0][2].child, entry)

    # -------------------------
    # Insert
    # -------------------------
    def insert_data(self, mbr, child=None, data=None):
        entry = self.create_entry(mbr, child, data)
        leafnode = self.ChooseLeaf(self.root , entry)

        leafnode.children.append(entry)
        leafnode.children_count += 1

        if leafnode.children_count > self.maxentries:
            
            LL = self.split_node(leafnode)
            # leafnode.children = L.children.copy()
            # leafnode.children_count = L.children_count
            # for e in L.children:
            #     print(e.mbr,"L")
            # for e in LL.children:
            #     print(e.mbr,"LL")

            return self.AdjustTree(leafnode, LL)
        else:
            return self.AdjustTree(leafnode, None)
    # -------------------------
    # Split Node (Quadratic Split)
    # -------------------------
    def split_node(self, node):

        entry1, entry2 = PickSeeds(node)
        
        remaining = [e for e in node.children if e != entry1 and e != entry2]


        
        g2 = self.create_node(node.is_leaf, None)

        node.children = [entry1]
        node.children_count = 1
        g1mbr = entry1.mbr

        g2.children.append(entry2)
        g2.children_count += 1
        g2mbr = entry2.mbr
        if entry2.child:
            entry2.child.parent = g2

        

        while remaining:

            if node.children_count + len(remaining) == self.minentries:
                for e in remaining:
                    node.children.append(e)
                    node.children_count += 1
                break

            if g2.children_count + len(remaining) == self.minentries:
                for e in remaining:
                    g2.children.append(e)
                    g2.children_count += 1
                    if e.child:
                        e.child.parent = g2
                break

            entry = PickNext(remaining, g1mbr, g2mbr)

            d1 = Enlargement(g1mbr, entry.mbr)
            d2 = Enlargement(g2mbr, entry.mbr)

            if d1 < d2:
                target = node
                g1mbr = union(g1mbr, entry.mbr)

            elif d2 < d1:
                target = g2
                g2mbr = union(g2mbr, entry.mbr)

            else:
                if area(g1mbr) < area(g2mbr):
                    target = node
                    g1mbr = union(g1mbr, entry.mbr)
                else:
                    target = g2
                    g2mbr = union(g2mbr, entry.mbr)

            target.children.append(entry)
            target.children_count += 1
            if target == g2 and entry.child:
                entry.child.parent = g2 
            remaining.remove(entry)

        return g2

# -------------------------
    # Adjust Tree (依照您提供的邏輯修改)
    # -------------------------
    def AdjustTree(self, N, NN=None):
        # 這裡的 root 用於比對是否到達當前樹的頂端，並在最後回傳
        
        # If N == Root : 
        # 如果已經處理到根節點，且根節點有分裂 (NN 不為 None)，
        # 代表需要長出新的根節點（樹長高一層）
        if N.parent is None: 
            if NN is not None:
                new_root = self.create_node(is_leaf=False)
                N.parent = new_root
                NN.parent = new_root
                # 計算 N 與 NN 的 MBR 並加入新根節點
                # 這裡假設你的 Node 物件或 Entry 可以透過計算其下所有 children 得到完整的 MBR
                # 或者從原本傳入的 MBR 處理。以下用通用的重新計算 MBR 邏輯：
                Nmbr = self.compute_node_mbr(N)
                NNmbr = self.compute_node_mbr(NN)
                
                new_root.children.append(self.create_entry(Nmbr, child=N))
                new_root.children.append(self.create_entry(NNmbr, child=NN))
                new_root.children_count = 2
                self.root = new_root  # 更新 RTree 的根節點
            return 
        # P = parent(N)
        P = N.parent

        # 更新 P 中指向 N 的 entry 的 MBR
        Nmbr = self.compute_node_mbr(N)
       
        for e in P.children:
            if e.child == N:
                
                e.mbr = Nmbr
                break

        # If NN != None:
        if NN is not None:
            # 產生一個，計算其 MBR 並插入 P
            NNmbr = self.compute_node_mbr(NN)
            P.children.append(self.create_entry(NNmbr, child=NN))
            P.children_count += 1
            NN.parent = P

            # If P > M (超過 maxentries):
            if P.children_count > self.maxentries:
                PP_split = self.split_node(P)
                # P.children = P_split.children.copy()
                # P.children_count = P_split.children_count
                # AdjustTree(P, PP)     
                return self.AdjustTree(P, PP_split)
            else:
                # Else: AdjustTree(P)
                return self.AdjustTree(P, None)
        else:
            # Else: AdjustTree(P)
            return self.AdjustTree(P, None)

    # 輔助函式：用來重新計算某個節點內所有 children 聯集後的最新 MBR
    def compute_node_mbr(self, node):
        if not node.children:
            return None
        current_mbr = node.children[0].mbr
        for e in node.children[1:]:
            current_mbr = union(current_mbr, e.mbr)
        return current_mbr
    

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root

        print("  " * level,
            "Node",
            self.compute_node_mbr(node),
            "leaf=", node.is_leaf)

        for e in node.children:
            print("  " * level, " Entry", e.mbr)
            if e.child:
                self.print_tree(e.child, level + 1)