# pickling/serialization
# packaging/decomposing instructions for an object so it can be sent and reassembled in another space in memory



# typing
from multiprocessing import Process, Value, Array 

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])

    # TODO Display the array without [] characters
    # if it doesn't need to grow and shrink, this is the best method