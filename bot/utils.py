import math


def chunked(arr, batch_size=1):
    for i in range(math.ceil(len(arr) / batch_size)):
        new_arr = arr[i * batch_size : i * batch_size + batch_size]

        yield new_arr
