import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

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



# plot
fig, ax = plt.subplots(figsize=(6, 2), dpi=300)
# ax.plot(x, B_field, 'g', label=r'$B^2/8\pi$', linewidth=2)
# ax.plot(x, pressure, 'b', label=r'$p$', linewidth=2)

# annotations
o = 0.04 #offset
# ax.text(2, B1+o, r'$B_1^2/8\pi$', color='green', fontsize=12)
# ax.text(6, B2+o, r'$B_2^2/8\pi$', color='green', fontsize=12)
# ax.text(2, p1+o, r'$p_1$', color='blue', fontsize=12)
# ax.text(6, p2+o, r'$p_2$', color='blue', fontsize=12)

# Customize and show the plot
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_xticks([]); ax.set_yticks([])

# boundary box at the step
ax.axvspan(x1Start+0.5, x1End-0.5, color='lightblue', alpha=0.5)

# arrows
c = (x1End+x1Start)/2 #center
lo = 0.2 # offset for arrows to the left
ro = 0    # no offset for right arrows
ax.arrow(c,           0.6,  -0.7,    0,  color='b', width=0.01) # shock
ax.text( c-0.7-lo,    0.6+o,  r'$v_s$')
ax.arrow(c+2,         0.6,  -0.5,    0,  color='b', width=0.01) # post shock init
ax.text( c+2-0.5-lo,  0.6+o,  r'$v_i$')
# ax.arrow(c+2-0.7,     0.45,  0.1,    0, color='g', width=0.01) # post shock rf
# ax.text( c+2-0.7+0.1, 0.45+o, r'$v_2$')
# ax.arrow(c-2,         0.45,  0.7,    0, color='g', width=0.01) # pre shock rf
# ax.text( c-2+0.7,     0.45+o, r'$v_1$')
ax.arrow(c,           0.78,  -0.2,    0, color='black', width=0.01) # normal
ax.text( c-0.15-lo,   0.78+o, r"$\hat n$")

# text
ax.text(1.3, 0.8, r"pre-shock", fontsize=11)
ax.text(5.7, 0.8, r"post-shock", fontsize=11)

# arrows for axis
ax.annotate("", xy=(7.5, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='black'))  # x-axis 
ax.annotate("", xy=(0, 0.9), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='black'))  # y-axis
ax.set_xlim(0, 7.5) # limits exact so arrows are shown
ax.set_ylim(0, 0.9)
# ax.add_patch(FancyBboxPatch(
#         (c-0.75, 0.1), 1.5, 0.25,
#         boxstyle=f"round,pad=0,rounding_size={0}",
#         edgecolor='black', facecolor='none')) #rounded square

plt.show()