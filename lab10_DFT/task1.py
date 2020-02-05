import numpy as np
import time


def F(n):
    return np.fromfunction(lambda i, j: np.exp(-2.j*np.pi*i*j/n), (n, n))


def dft(x):
    n = len(x)
    return F(n) @ x


def idft(y):
    n = len(y)
    return np.conj(F(n) @ np.conj(y)) / n


def fft(x):
    n = len(x)
    if n == 1:
        return x
    else:
        even = fft(x[0::2])
        odd = fft(x[1::2])
        T = [np.exp(-2.j*np.pi*k/n)*odd[k] for k in range(n//2)]
        return [even[k] + T[k] for k in range(n//2)] + \
               [even[k] - T[k] for k in range(n//2)]


x = np.random.rand(4)

start_time = time.time()
y = dft(x)
end_time = time.time()
print("DFT time: " + str(end_time-start_time) + "ns")
#print(y)

print()

start_time = time.time()
y = fft(x)
end_time = time.time()
print("FFT time: " + str(end_time-start_time) + "ns")
#print(y)

print()

start_time = time.time()
y = np.fft.fft(x)
end_time = time.time()
print("Library FFT time: " + str(end_time-start_time) + "ns")
#print(y)


print("\n")

#print(x)
#print(idft(y))
#print(np.fft.ifft(np.fft.fft(x)))
