import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(-1.1, 1.1, num=100, endpoint=True)
y = x ** 4 - x ** 2

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')

plt.title("Plot with two minima: x^4 - x^2")
plt.plot(x,y)
plt.show()
