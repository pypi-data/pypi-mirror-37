from numba import jit, int64, complex128 as complex

@jit((complex[:,:,:], complex[:,:,:], int64, int64), fastmath=True)
def backward_padding(padded_array, trunc_array, axis, Ns):
    padded_array.fill(0)
    N = trunc_array.shape[axis]
    s = [slice(0, n) for n in trunc_array.shape]
    #padded_array[tuple(s)] = trunc_array[tuple(s)]
    for i in range(trunc_array.shape[0]):
        for j in range(trunc_array.shape[1]):
            for k in range(trunc_array.shape[2]):
                padded_array[i, j, k] = trunc_array[i, j, k]

    if Ns % 2 == 0:  # Symmetric Fourier interpolator
        s[axis] = slice(N-1, N)
        for i in range(s[0].start, s[0].stop):
            for j in range(s[1].start, s[1].stop):
                for k in range(s[2].start, s[2].stop):
                    padded_array[i, j, k] = padded_array[i, j, k].real*0.5

