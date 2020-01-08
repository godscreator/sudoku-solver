def input_sudoku(n = 3):
    M = []
    for i in range(n*n):
        k = input().split()
        if len(k)!=n*n:
            raise Exception("Not a valid sudoku.")
        M.append(k)
    return M

def print_sudoku(M,n = 3):
    for i in range(n*n):
        print(' '.join(M[i]))
    print()

def next_move(M,n = 3,c = '-' ,S = "123456789",sr=0,sc=0,sk=-1):
    """ to search for empty box
        sr,sc,sk is starting row , col index
        and  index in S  to search.
        if game is completed then returns (n*n,n*n,len(S))
        if no next move is possible return (-1,-1,-1)
        nodes represented by tuple(r,c,v)
        where r is row index, c is column index in M
        and v is values index in S are returned"""
    for i in range(sr,n*n):
        if i==sr:
            ssc = sc
        else:
            ssc = 0
        for j in range(ssc,n*n):
            if M[i][j]==c:
                if i==sr and j==sc:
                    m = sk+1
                else:
                    m = 0
                for k in range(m,len(S)):
                    x1 = S[k] in M[i]
                    if not x1:
                        x2 = False
                        for q in range(n*n):
                            if S[k]==M[q][j]:
                                x2 = True
                                break
                        if not x2:
                            x3 = False
                            for q in range(n*(i//n),n*(i//n)+n):
                                for r in range(n*(j//n),n*(j//n)+n):
                                    if S[k]== M[q][r]:
                                        x3 = True
                                    if x3:
                                        break
                                if x3:
                                    break
                            if not x3:
                                return (i,j,k)
                return (-1,-1,-1)
    return (n*n,n*n,len(S))
    
def sudoku_solver(M,n = 3,c = '-' ,S = "123456789"):
    """this function will use dfs search for solving
        sudoku
        n is size of smaller grids"""
    st = []
    nm = next_move(M,n,c,S,0,0,-1)
    if nm!=(-1,-1,-1) and nm!=(n*n,n*n,len(S)):
        M[nm[0]][nm[1]]=S[nm[2]]
        st.append(nm)
    while st:
        nm = next_move(M,n,c,S,nm[0],nm[1],nm[2])
        if nm == (-1,-1,-1):
            nm = st.pop()
            M[nm[0]][nm[1]]=c
            nm = next_move(M,n,c,S,nm[0],nm[1],nm[2])
            while st and nm==(-1,-1,-1):
                nm = st.pop()
                M[nm[0]][nm[1]]=c
                nm = next_move(M,n,c,S,nm[0],nm[1],nm[2])
            if nm==(-1,-1,-1):
                return False
            else:
                M[nm[0]][nm[1]]=S[nm[2]]
                st.append(nm)
        elif nm == (n*n,n*n,len(S)):
            if nm == (n*n,n*n,len(S)):
                return True
        else:
            M[nm[0]][nm[1]]=S[nm[2]]
            st.append(nm)
            
if __name__ == "__main__":
    M = input_sudoku()
##    M = ["2 4 - - - - 1 - 7",
##         "6 - 8 9 1 5 3 - 2",
##         "9 - - - 2 7 - 6 -",
##         "- 9 7 1 3 2 6 - 5",
##         "- - - 5 - 8 - 3 4",
##         "5 - - - - - - - -",
##         "7 - 2 3 - 9 8 - 1",
##         "- - - 8 - - - - -",
##         "- 1 9 - - - 4 7 -"]
##    M = [M[i].split() for i in range(9)]
##    M = """5 3 - - 7 - - - -
##6 - - 1 9 5 - - -
##- 9 8 - - - - 6 -
##8 - - - 6 - - - 3
##4 - - 8 - 3 - - 1
##7 - - - 2 - - - 6
##- 6 - - - - 2 8 -
##- - - 4 1 9 - - 5
##- - - - 8 - - 7 9"""
##    M = M.split()
##    M = [ M[9*i:9*i+9] for i in range(9)]
    #print_sudoku(M)
    sudoku_solver(M)
    print_sudoku(M)
    
