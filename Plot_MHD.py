import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# System constants and inital
# theta_i = 30/360*2*np.pi
# beta_i = 0.05
theta_i = 0.2 * np.pi
beta_i = 0.4
gamma = 5/3

#options:
Latex = True                    #use latex font
Titels = False                  #title for everyplot
Hypersoniclimit = False         #plots upto M1=20.3 (M1Range)
HypersoniclimitValue = 20.5     # M1 max
SavePic = False                 #saves the plot without showing 
SavePicName = 'Compilation.png'
Color = True                    #slow,fast,interm. regions colored (does not work with Goeldbloed=True)
Goeldbloed = False              #changes x axis to m1^2 for comparing with Goeldbloeds plots



#region Functions: M1, M2 and all ending in 2 (like theta2) can be arrays
def F(M1, M2, theta1, beta1, gamma):
    '''Longcope equation for F(M1,M2) (=0 taken later)'''
    equation = (- (gamma + 1) * M2**6 + 
                ((gamma - 1) * M1**2 + 2 * (gamma + 1) + (gamma * beta1) / np.cos(theta1)**2 + 
                 gamma * np.tan(theta1)**2) * M2**4 - 
                (2 * (gamma - 1) * M1**2 + ((gamma + 1) + 2 * gamma * beta1) / 
                 np.cos(theta1)**2 + (gamma - 2) * M1**2 * np.tan(theta1)**2) * M2**2 + 
                ((gamma - 1) * M1**2 + gamma * beta1) / np.cos(theta1)**2)
    return equation

def G(M1, M2, theta1, beta1):
    '''entropy condition G(M1,M2) (>= 0 taken later)'''
    # beta1 = beta1*(1+np.tan(theta1)**2)
    equation = (M2**2 - 1)**2 * (M1**2 - M2**2 - beta1/2*((M1**2/M2**2)**gamma - 1)) - np.tan(theta1)**2/2 * (M1**2 - M2**2)*(M1**2 + M2**2 - 2)
    # print('where nan', np.argwhere(np.isnan(equation)))
    return np.nan_to_num(equation, nan=-np.inf) #is nan at M2=0

def F2_theta2(M1,M2,theta1):
    '''returns theta2 analytically solved value'''
    return np.arctan((M1**2 - 1)/(M2**2 - 1) * np.tan(theta1))

def F3_Bratio(theta1, theta2):
    '''returns ratio B2/B1'''
    #return np.square(np.cos(theta1)/np.cos(theta2))
    return np.tan(theta2)/np.tan(theta1)
    

def F4_beta2(M1,M2, theta1, theta2, beta1):
    '''returns beta2 analytically solved value'''
    tan_th1_sqrd = np.square(np.tan(theta1))
    #tan_th2_sqrd = np.square(np.tan(theta1)*(np.square(M1)-1)/(np.square(M2)-1)) #theta2 w/ theta1,M1,M2
    tan_th2_sqrd = np.square(np.tan(theta2))
    beta2_n = 2*(np.square(M1)-np.square(M2))+tan_th1_sqrd-tan_th2_sqrd+beta1*(1+tan_th1_sqrd)
    return np.divide(beta2_n, 1+tan_th2_sqrd)
#endregion


if Latex: # Use latex text
    plt.rc('text.latex', preamble=r'\usepackage{lmodern}')
    # Options
    params = {'text.usetex': True,
            'font.size': 11,
            'font.family': 'lmodern'}
    plt.rcParams.update(params)

#reordeding the plot grid
if SavePic:
    fig, ((ax1, ax2, ax5), (ax3, ax4, ax6)) = plt.subplots(2, 3, figsize=(15, 8), dpi=900) #higher res for save
else:
    fig, ((ax1, ax2, ax5), (ax3, ax4, ax6)) = plt.subplots(2, 3, figsize=(15, 8))
plt.subplots_adjust(left=0.15, bottom=0.15, hspace=0.4)

def plotDefs():
    '''plot appearance'''
    # Set x and y limits 
    if Hypersoniclimit:
        xRange = (0, HypersoniclimitValue - 0.2)  # x-axis range for both plots
    else:
        xRange = (0, 2.3)
    yRangeTheta2 = (-0.5, 0.5)  # y-axis range for the second plot (theta2/pi)
    ax1.set_xlim(xRange)
    ax1.set_ylim(xRange)
    ax2.set_xlim(xRange)
    ax2.set_ylim(yRangeTheta2)
    ax5.set_xlim(xRange)
    if not Hypersoniclimit:
        ax5.set_ylim(xRange)
        ax3.set_ylim((-2,3))
    ax4.set_xlim(xRange)
    ax6.set_ylim(xRange)
    ax6.set_xlim(xRange)
    ax3.set_xlim(xRange)
    

    #grid
    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    ax5.grid(True)
    ax6.grid(True)

    # Label the axes
    ax1.set_xlabel("M1")
    ax1.set_ylabel("M2", rotation=0)
    ax2.set_xlabel("M1")
    ax2.set_ylabel(r'$\theta_2 / \pi$', rotation=0)
    ax3.set_xlabel('M1')
    ax3.set_ylabel(r'$B_{2\perp}/B_{1\perp}$', rotation=0)
    ax4.set_xlabel('M1')
    ax4.set_ylabel(r'$\beta_2$', rotation=0)
    ax5.set_xlabel('M1')
    ax5.set_ylabel(r'$\rho_2 / \rho_1$', rotation=0)
    ax6.set_xlabel('M1')
    ax6.set_ylabel('M2', rotation=0)

    # Fill the area where M2 > M1 with grey color in ax1
    ax1.fill_between(M1Range, M1Range, color='grey', alpha=0.5)

    # title
    if Titels:
        ax1.set_title('Contour F(M1, M2)=0')
        ax2.set_title(r'Contour for $\theta_2$')
        ax3.set_title('B ratio as func of M1')
        ax4.set_title(r'$\beta_2$')
        ax5.set_title(r'$\rho_2 / \rho_1$')
        ax6.set_title('Contour F(M1, M2)=0, w/ entropy allowed area as gray')


# Sliders
axcolor = 'yellow'
ax_theta = plt.axes([0.05, 0.1225, 0.0225, 0.8], facecolor=axcolor)
ax_beta = plt.axes( [0.08, 0.1225, 0.0225, 0.8], facecolor=axcolor)
ax_m1 = plt.axes(   [0.02, 0.1225, 0.0225, 0.8], facecolor=axcolor)

thetaSlider = Slider(ax_theta, 'theta1', -0.5 * np.pi, 0.5 * np.pi, valinit=theta_i, orientation='vertical')
betaSlider =  Slider(ax_beta, 'beta',            0.01,         5.0, valinit=beta_i,  orientation='vertical')
samplesSlider =Slider(ax_m1, 'samples',           400,        5000, valinit=1400,    orientation='vertical')

# Reset button
resetax = plt.axes([0, 0, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

#Goedbloed button
gbx = plt.axes([0.1, 0, 0.1, 0.04])
button2 = Button(gbx, 'Goedbloed1', color=axcolor, hovercolor='0.975')

gbx3 = plt.axes([0.2, 0, 0.1, 0.04])
button3 = Button(gbx3, 'Goedbloed2', color=axcolor, hovercolor='0.975')

# Init plots and Plot vars
M1Range = np.linspace(0, 2.5, 400)  # init setup, changes nothing
theta2_range = np.linspace(-np.pi/2, np.pi/2, 400)  # y for second plot (theta2/pi)
plotDefs()
ax1.plot(1,1)
ax2.plot(1,1)
ax3.plot(1,1)
ax4.plot(1,1)
ax5.plot(1,1)
ax6.plot(1,1)
#endregion

# draw plots and update them
def update(val):
    if isDragging: 
        return
    #slider values
    theta1 = thetaSlider.val
    beta1 = betaSlider.val
    fig.suptitle(r'$\Theta_1 /\pi$ = ' + str(theta1/np.pi) + r', $\beta_1$ ' + str(beta1))
    if Hypersoniclimit:
        M1Range = np.linspace(0, HypersoniclimitValue, int(samplesSlider.val))
    else:
        M1Range = np.linspace(0, 2.5, int(samplesSlider.val))
    if True: #clear
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax4.clear()
        ax5.clear()
        ax6.clear()
        plotDefs()
    
    #1st plot: evaluate F
    M1Mesh, M2Mesh = np.meshgrid(M1Range, M1Range)  
    FMesh = F(M1Mesh, M2Mesh, theta1, beta1, gamma)
    contourF = ax1.contour(M1Mesh, M2Mesh, FMesh, levels=[0], colors='black', linewidth=0.001)
    
    #get M1 and M2 values from contour
    M1Arr, M2Arr = contourF.allsegs[np.where(contourF.levels == 0)[0][0]][0][::-1].T  # (has [[M1,M2],[],...] in ascending order ^).T or now [[M1,...],[M2,...]]


    #2nd plot: entropy G(m1,m2) to ax1
    GMesh = G(M1Mesh, M2Mesh, theta1, beta1)
    ax6.contour(M1Mesh, M2Mesh, FMesh, levels=[0], colors='black', linestyles='dashed')
    ax6.contourf(M1Mesh, M2Mesh, GMesh, levels=[0, GMesh.max()], colors=['gray'], alpha=0.5) #entropy allowed reagion colored as gray, some inaccuracies at the corners when zoomed

    #3rd plot: theta2
    if Goeldbloed:
        '''square M1 and M2'''
        M1Arr = np.square(M1Arr)
        M2Arr = np.square(M2Arr)
        ax1.plot(M1Arr, M2Arr, colors='black')    #replot ax1
        fig.suptitle("x-axis $M1^2$ suqared on blues (M2^2 too)")
    theta2Arr = F2_theta2(M1Arr, M2Arr, theta1)
    ax2.plot(M1Arr, theta2Arr/np.pi, color='black', linestyle='dashed')

    #4th plot: B ratio
    BratioArr = F3_Bratio(theta1, theta2Arr)      #(B2/B1)^2
    ax3.plot(M1Arr, BratioArr, color='Black', linestyle='dashed')

    #5th plot: beta2
    beta2 = F4_beta2(M1Arr, M2Arr, theta1, theta2Arr, beta1)
    ax4.plot(M1Arr, beta2, color='black', linestyle='dashed')

    #6th plot: rho2/rho1
    rho2DivRho1 = np.divide(M1Arr**2, M2Arr**2)
    ax5.plot(M1Arr, rho2DivRho1, color='black', linestyle='dashed')
    fig.canvas.draw_idle()

    if Color:
        #three regions for color (slow, intermediate, fast):
        r1S = (M1Arr >= M2Arr) & (M1Arr < 1)
        r2I = (M1Arr > 1) & (M2Arr < 1)
        r3F = (M1Arr >= M2Arr) & (M2Arr > 1)

        #1st 
        ax1.plot(M1Arr[r1S], M2Arr[r1S], color='blue')
        ax1.plot(np.append(M1Arr[r2I], 1), np.append(M2Arr[r2I], 1), color='green') #add the 1,1 point as there we have discontinuity in F
        ax1.plot(M1Arr[r3F], M2Arr[r3F], color='red')

        #2nd
        ax6.plot(M1Arr[r1S], M2Arr[r1S], color='blue')
        ax6.plot(np.append(M1Arr[r2I], 1), np.append(M2Arr[r2I], 1), color='green') #add the 1,1 point as there we have discontinuity in F
        ax6.plot(M1Arr[r3F], M2Arr[r3F], color='red')

        #3rd
        ax2.plot(M1Arr[r1S], theta2Arr[r1S]/np.pi, color='blue')
        ax2.plot(M1Arr[r2I], theta2Arr[r2I]/np.pi, color='green')
        ax2.plot(M1Arr[r3F], theta2Arr[r3F]/np.pi, color='red')

        #4th
        ax3.plot(M1Arr[r1S], BratioArr[r1S], color='blue')
        ax3.plot(M1Arr[r2I], BratioArr[r2I], color='green')
        ax3.plot(M1Arr[r3F], BratioArr[r3F], color='red')

        #5th
        ax4.plot(M1Arr[r1S], beta2[r1S], color='blue')
        ax4.plot(M1Arr[r2I], beta2[r2I], color='green')
        ax4.plot(M1Arr[r3F], beta2[r3F], color='red')

        #6th
        ax5.plot(M1Arr[r1S], rho2DivRho1[r1S], color='blue')
        ax5.plot(M1Arr[r2I], rho2DivRho1[r2I], color='green')
        ax5.plot(M1Arr[r3F], rho2DivRho1[r3F], color='red')


#region Update only after mouse release
isDragging = False
def on_press(event):
    global isDragging
    if event.inaxes == thetaSlider.ax or event.inaxes == betaSlider.ax or event.inaxes == samplesSlider.ax:
        isDragging = True

def on_release(event):
    global isDragging
    if isDragging:
        isDragging = False
        update(None)  # Trigger an update on release
#endregion
#region Buttons and sliders setup
def reset(event):
    thetaSlider.reset()
    betaSlider.reset()
button.on_clicked(reset)
def setgb(event):#Goeldbloeds 1st params
    thetaSlider.set_val(0.2*np.pi)
    betaSlider.set_val(0.4)
def setgb2(event):#Goeldbloeds 2nd params
    thetaSlider.set_val(0.1*np.pi)
    betaSlider.set_val(0.3)

button2.on_clicked(setgb)
button3.on_clicked(setgb2)
fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)

thetaSlider.on_changed(update)
betaSlider.on_changed(update)
samplesSlider.on_changed(update)
update(None)
#endregion

if SavePic:
    fig.savefig(SavePicName)   # save the figure to file
    plt.close(fig)
else:
    plt.show()