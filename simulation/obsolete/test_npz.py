import numpy as np

data = [np.arange(8).reshape(2, 4), np.arange(10).reshape(2, 5)]
np.savez('mat.npz', *data)

container = np.load('2022-11-22_pgun_e-_wall_only_e0.01-10GeV_center_1prt_10000evt.npz')
keys = [key for key in container]
data = [container[key] for key in container]
print(keys)
#print(container["true_e"])
true_e = container["true_e"]
modules = container["modules"]
sum_e =np.sum(modules, axis=1)
print(len(sum_e))
for i in range(10):
     print(true_e[i], sum_e[i])


