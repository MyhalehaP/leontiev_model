from os import truncate
import numpy as np

class Leont:

    def solve(self,matrix,Y,Yn):

        Xn = []

        for i in range(0,len(matrix)):
            sum = Y[i]
            for j in range(0,len(matrix[i])):
                sum+=matrix[i][j]
            Xn.append(sum)

        # direct costs matrix
        A = []
        for i in range(0,len(matrix)):
            tmp = []
            for j in range(0,len(matrix[i])):
                value = float(matrix[i][j] / Xn[j])
                tmp.append(round(value,5))
            A.append(tmp)

        A = np.array(A)


        # identity matrix
        E = np.identity(len(matrix))

        # costs - production
        E_new = np.subtract(E,A)

        # full costs matrix / inverse of E-A
        S = np.linalg.inv(E_new)

        # gross output volume
        X = np.dot(S,Yn)

        return X

    pass