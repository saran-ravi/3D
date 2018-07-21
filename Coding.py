def fn(a, b):
        s = set()
        c = a + b
        c.sort()
        for i in range(len(c)):
                if c[i] == c[i-1]:
                        s.add(c[i]),
        s = list(s)
        s.sort()
        for i in s:
            print i,
        print'\n'
        for i  in a:
                if i not in b:
                        print i,
        

a = [4,5,8,5,3]
b = [2,3,7,2,9,0]

fn(a,b)
