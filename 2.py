def a():
    m={}
    m['q']=1
    yield m
    print(m)
print([w for w in a()])