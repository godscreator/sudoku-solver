def input_sudoku():
    M = []
    for i in range(9):
        k = input().split()
        if len(k) != 9:
            raise Exception("Not a valid sudoku.")
        M.append(k)
    return M


def print_sudoku(M):
    for i in range(9):
        print(' '.join(M[i]))
    print()


class solver:
    def __init__(self):
        self.M = [["-"] * 9 for i in range(9)]
        self.S = "123456789-"

    def set_from(self, M):
        self.M = [[M[i][j] for j in range(9)] for i in range(9)]

    def is_valid_move(self, i, j, k):
        x1 = False
        for r in range(9):
            if r != j and self.S[k] == self.M[i][r]:
                x1 = True
                break
        if not x1:
            x2 = False
            for q in range(9):
                if q != i and self.S[k] == self.M[q][j]:
                    x2 = True
                    break
            if not x2:
                x3 = False
                for q in range(3 * (i // 3), 3 * (i // 3) + 3):
                    for r in range(3 * (j // 3), 3 * (j // 3) + 3):
                        if not (q == i and r == j) and self.S[k] == self.M[q][r]:
                            x3 = True
                        if x3:
                            break
                    if x3:
                        break
                if not x3:
                    return True
        return False

    def next_move(self, sr=0, sc=0, sk=-1):
        """ searches for next valid move"""
        for i in range(sr, 9):
            ssc = sc if i == sr else 0
            for j in range(ssc, 9):
                if self.M[i][j] == self.S[-1]:
                    m = sk + 1 if i == sr and j == sc else 0
                    for k in range(m, 9):
                        if self.is_valid_move(i, j, k):
                            return (i, j, k)
                    return (-1, -1, -1)  # no valid move possible for next empty box
        return (9, 9, 9)  # game completed.

    def sudoku_solver_inner(self, is_pausable=False):
        """this function will use dfs search for solving
            sudoku
            n is size of smaller grids"""
        st = []
        nm = self.next_move(0, 0, -1)
        if nm != (-1, -1, -1) and nm != (9, 9, 9):
            self.M[nm[0]][nm[1]] = self.S[nm[2]]
            if is_pausable:
                yield nm[0], nm[1], self.S[nm[2]]
            st.append(nm)
        while st:
            nm = self.next_move(nm[0], nm[1], nm[2])
            if nm == (-1, -1, -1):
                nm = st.pop()
                self.M[nm[0]][nm[1]] = self.S[-1]
                if is_pausable:
                    yield nm[0], nm[1], self.S[-1]
                nm = self.next_move(nm[0], nm[1], nm[2])
                while st and nm == (-1, -1, -1):
                    nm = st.pop()
                    self.M[nm[0]][nm[1]] = self.S[-1]
                    if is_pausable:
                        yield nm[0], nm[1], self.S[-1]
                    nm = self.next_move(nm[0], nm[1], nm[2])
                if nm == (-1, -1, -1):
                    yield -1
                else:
                    self.M[nm[0]][nm[1]] = self.S[nm[2]]
                    if is_pausable:
                        yield nm[0], nm[1], self.S[nm[2]]
                    st.append(nm)
            elif nm == (9, 9, 9):
                yield 1
            else:
                self.M[nm[0]][nm[1]] = self.S[nm[2]]
                if is_pausable:
                    yield nm[0], nm[1], self.S[nm[2]]
                st.append(nm)

    def solve(self, is_pausable=False):
        if is_pausable:
            return self.sudoku_solver_inner(is_pausable)
        else:
            k = self.sudoku_solver_inner(is_pausable)
            if next(k) == 1:
                return True
            else:
                return False


if __name__ == "__main__":
    M = input_sudoku()
    s = solver()
    s.set_from(M)
    k = s.solve()
    if k:
        print_sudoku(s.M)
    else:
        print("Not solvable")
