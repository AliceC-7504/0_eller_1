import matplotlib.pyplot as plt
import numpy as np

max_correctness = 0.6
# Calculate for what sequence length 99% of random sequences have correctness under max_correctness
def calc_deviation(n):
    return 1 / (2 * np.sqrt(n))

def calc_percent(n):
    dev = calc_deviation(n)
    f = lambda x: (1 / (dev * np.sqrt(2 * np.pi))) * np.exp((-1/2) * ((x - 0.5) / dev)**2)
    x = np.linspace(0,max_correctness,1000)
    return (np.trapz(f(x), x)) * 100

x = []
y = []
found = False
for i in range(1,300):
    x.append(i)
    y.append(calc_percent(i))
    if not found and y[-1] >= 99:
        found = True
        print("Minsta längd där 99% av sekvenser har korrekthet under " + str(max_correctness * 100) + "%: " + str(x[-1]))
   
plt.plot(x, y)
plt.plot(x, y)
plt.ylabel('Andel (%) av slumpmässiga sekvenser med korrekthet under ' + str(max_correctness * 100) + '%')
plt.xlabel('Sekvenslängd')
plt.show()