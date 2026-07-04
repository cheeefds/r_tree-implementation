def union(mbr1,mbr2):
    return [min(mbr1[0],mbr2[0]),max(mbr1[1],mbr2[1]),min(mbr1[2],mbr2[2]),max(mbr1[3],mbr2[3])]

def area(mbr):
    return (mbr[1]-mbr[0])*(mbr[3]-mbr[2])

def Enlargement(mbr1,mbr2):
        original_area = area(mbr1)
        new_mbr = union(mbr1, mbr2)
        new_area = area(new_mbr)
        return new_area - original_area

def PickSeeds(N):
    Maxd = float('-inf')
    Seed1 = None
    Seed2 = None

    for i in range(N.children_count):
        for j in range(i+1, N.children_count):
            mbr1 = N.children[i].mbr
            mbr2 = N.children[j].mbr
            d = Enlargement(mbr1, mbr2)
            if d > Maxd:
                Maxd = d
                Seed1 = N.children[i]
                Seed2 = N.children[j]
    return Seed1, Seed2

def PickNext(remaining_children,g1mbr,g2mbr):
    Maxd = float('-inf')
    NextSeed = None
    for i in range(len(remaining_children)):
        D1 = area(union(g1mbr, remaining_children[i].mbr)) - area(g1mbr)
        D2 = area(union(g2mbr, remaining_children[i].mbr)) - area(g2mbr)
        d = abs(D1 - D2)
        if d > Maxd:
            Maxd = d
            NextSeed = remaining_children[i]
    return NextSeed

def is_overlap(mbr,searchmbr):
    
        if mbr[0] > searchmbr[1] or mbr[1] < searchmbr[0] or mbr[2] > searchmbr[3] or mbr[3] < searchmbr[2]:
            return False
        
        return True