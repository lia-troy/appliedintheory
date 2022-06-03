import numpy as np
import matplotlib.pyplot as plt

x1 = np.linspace(0.3,0.301,200)
x2 = np.linspace(0.8,0.801,200)

def logistic_map_func(x):
    return 3.95 * x * (1 - x)

logistic_map_vec = np.vectorize(logistic_map_func)

def iterate_to_t(t, x):
    input_size = x.size
    data = np.zeros((t + 1, input_size))

    data[0] = np.copy(x)
    for i in range(1, t + 1):
        new_data = logistic_map_vec(np.copy(data[i - 1]))
        data[i] = new_data

    return data

t = 15

data1 = iterate_to_t(t, x1)
data2 = iterate_to_t(t, x2)

input_size = x1.size
x = np.zeros((t + 1, input_size))
for i in range(1, t + 1):
    new_row = np.full((input_size,), i)
    x[i] = new_row

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.set_xlabel('Iteration number (t)')
ax.set_ylabel('Output at time t')
plt.title("Mixing of logistic map with r = 3.95")

plt.scatter(x.flatten(), data1.flatten(), c='#0000FF', alpha = 0.2)
plt.scatter(x.flatten(), data2.flatten(), c='#FF9912', alpha = 0.15)

ax.set_xticks(np.linspace(0,t,t+1), minor=False)
ax.set_yticks(np.linspace(0,1,11), minor=False)
plt.ylim([0, 1])
ax.xaxis.grid()
plt.show()

