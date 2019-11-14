import sys
sys.setrecursionlimit(10**6)
'''
Solves Ax=b. A has size n*m, b has size n*1
Returns x (size m*1) if unique solution exists,
otherwise 'multiple' or 'inconsistent'.

Time Complexity: O(n^3)
Space Complexity: O(n^2)
'''
def gcd(x,y):
    if x<0 or y<0: return gcd(abs(x),abs(y))
    return gcd(y,x%y) if y else x
def gauss(A,B):
    N,M = len(A),len(A[0])
    assert M <= N, 'Gauss not implemented for M<=N.'
    for col in range(M):
        imax = col
        for i in range(col+1,N):
            if abs(A[i][col]) > abs(A[imax][col]):
                imax = i
        if A[imax][col] == 0:
            if max([abs(aa) for aa in A[imax]]) > 0:
                continue
            for i in range(col+1,N):
                if max([abs(aa) for aa in A[i]]) > 0:
                    A[imax],A[i] = A[i],A[imax]
                    B[imax],B[i] = B[i],B[imax]
                    break
            continue

        A[col],A[imax] = A[imax],A[col]
        B[col],B[imax] = B[imax],B[col]
        for i in range(col+1,N):
            fu,fd = A[i][col],A[col][col]
            fu,fd = fu//gcd(fu,fd),fd//gcd(fu,fd)
            A[i][col] = 0
            for j in range(col+1,M):
                A[i][j] = fd*A[i][j] - fu*A[col][j]
            B[i] = fd*B[i] - fu*B[col]

    x = [-1]*M
    for row in range(M,N):
        if B[row] != 0: return None

    if A[M-1][M-1] == 0:
        if B[M-1] != 0: return None
        x[M-1] = 0
    elif B[M-1] % A[M-1][M-1]:
        return None
    else:
        x[M-1] = B[M-1]//A[M-1][M-1]

    for i in range(M-2,-1,-1):
        s = 0
        for j in range(i+1,M): s += A[i][j]*x[j]
        if A[i][i] == 0:
            if B[i] != s: return None
            x[i] = 0
        elif (B[i]-s) % A[i][i]: return None
        else: x[i] = (B[i]-s)//A[i][i]

    return x


if __name__ == '__main__':
    #DOES NOT WORK?????
    N = int(input())
    while N:
        A = [map(float,input().split()) for _ in range(N)]
        B = map(float,input().split())
        ans = gauss(A,B)
        if type(ans) == str:
            print(ans)
        else:
            print(' '.join(map(str,ans)))
        N = int(input())
