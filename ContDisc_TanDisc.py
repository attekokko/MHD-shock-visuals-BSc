import numpy as np
import matplotlib.pyplot as plt
ContDisc = False     #if False draws TanDisc


#use latex font
if True: 
    plt.rc('text.latex', preamble=r'\usepackage{lmodern}')
    params = {'text.usetex': True,
            'font.size': 11,
            'font.family': 'lmodern'}
    plt.rcParams.update(params)

# step start and end
x1Start, x1End = 3, 5
x2Start, x2End = 3, 5

# start and end levels for the steps [0 - 1]
a = 0.3
b = 0.4
B1 = 1.0 -a  # first level
B2 = 0.5 -a  # second level
p1 = 0.5 -b  # first level
p2 = 1.0 -b  # second level

# sigmoid function, error function = smooth step function
def SmoothStep(x, xStart, xEnd):
    xCenter = (xStart + xEnd) / 2   #center of the step
    return 1 / (1 + np.exp(-10 * (x - xCenter)))    #the step and steepness

x = np.linspace(0, 7, 500)

# two stepfunc
step1 = SmoothStep(x, x1Start, x1End)
step2 = SmoothStep(x, x2Start, x2End)

# shift the start and end levels => complete step functions
B_field = B1 * (1 - step1) + B2 * step1
pressure = p1 * (1 - step2) + p2 * step2

# plot
fig, ax = plt.subplots(figsize=(6, 2), dpi=300)
ax.plot(x, B_field, 'g', label=r'$B^2/8\pi$', linewidth=2)
ax.plot(x, pressure, 'b', label=r'$p$', linewidth=2)

# annotations
o = 0.05 #offset
if ContDisc:
    ax.text(2, B1+o, r'$\rho_1$', color='green', fontsize=12)
    ax.text(6, B2+o, r'$\rho_2$', color='green', fontsize=12)
    ax.text(2, p1+o, r'$T_1$', color='blue', fontsize=12)
    ax.text(6, p2+o, r'$T_2$', color='blue', fontsize=12)
else: #tandisc
    ax.text(2, B1+o, r'$B_1^2/8\pi$', color='green', fontsize=12)
    ax.text(6, B2+o, r'$B_2^2/8\pi$', color='green', fontsize=12)
    ax.text(2, p1+o, r'$p_1$', color='blue', fontsize=12)
    ax.text(6, p2+o, r'$p_2$', color='blue', fontsize=12)

# Customize and show the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

# boundary box at the step
ax.axvspan(x1Start+0.5, x1End-0.5, color='lightblue', alpha=0.5)

# arrows for axis
ax.annotate("", xy=(7.5, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='black'))  # x-axis 
ax.annotate("", xy=(0, 0.9), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='black'))  # y-axis
ax.set_xlim(0, 7.5) # limits exact so arrows are shown
ax.set_ylim(0, 0.9)

plt.show()