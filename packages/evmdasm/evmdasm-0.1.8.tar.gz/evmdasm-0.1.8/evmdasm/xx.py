

class lala(list):

    def __iter__(self):
        print ("ITER")
        return super().__iter__()


x = lala([1,2,3,4,5])
for i in x:
    print(x)