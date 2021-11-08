# %% [markdown]
# # Project 1 - Quality control for a clock manufacturing company [40 marks]
# 
# ---
# 
# Make sure you read the instructions in `README.md` before starting! In particular, make sure your code is well-commented, with sensible structure, and easy to read throughout your notebook.
# 
# ---
# 
# There is an imaginary clock manufacturing company that wants you to develop software to check the quality of its products. The clocks produced by this company have **two hands**:
# 
# - the small hand is **red** and indicates the **hour**,
# - the long hand is **green** and indicates the minutes.
# 
# We refer to these as *the hour hand* and *the minute hand* respectively. These clocks do not have any other hands (although some other clocks have a third hand indicating the seconds).
# 
# It is very important for these hands to be properly aligned. For example, if the hour hand is pointing to the hour `3` (being horizontal and pointing toward right), the minute hand should be pointing toward the hour `12` (vertical and pointing upward). Another example is when the hour hand is pointing to the hour `1:30` (making a 45 degree angle from the vertical line), the minute hand should be pointing toward hour `6` (vertical and downward).
# 
# | Correct `1:30`, the hour hand is halfway between 1 and 2. | Incorrect `1.30`, the hour hand is too close to 1. |
# |:--:|:--:|
# | ![Correct 1.30](graphics/one_thirty_correct.png) | ![Incorrect 1.30](graphics/one_thirty_incorrect.png) |
# 
# Due to production imprecisions, this is not the case all the time. Your software package will **quantify the potential misalignments** and help the company to return the faulty clocks back to the production line for re-adjustment.
# 
# You will achieve this goal in several steps during this project. Most steps can be done independently. Therefore, if you are struggling with one part, you can move on to other tasks and gain the marks allocated to them.
# 
# For most tasks, under "✅ *Testing:*", you will be given instructions on how to check that your function works as it should, even if you haven't done the previous task.
# 
# 
# ---
# 
# ## Task 1: Reading images into NumPy arrays [3 marks]
# 
# The company takes a picture of each clock, and saves it as a PNG image of 101x101 pixels. The folder `clock_images` contains the photos of all the clocks you need to control today.
# 
# In a PNG colour image, the colour of each pixel can be represented by 3 numbers between 0 and 1, indicating respectively the amount of **red**, the amount of **green**, and the amount of **blue** needed to make this colour. This is why we refer to colour images as **RGB** images.
# 
# - If all 3 values are 0, the pixel is black.
# - If all 3 values are 1, the pixel is white.
# - If all 3 values are the same, the pixel is grey. The smaller the values, the darker it is.
# - Different amounts of red, green, and blue correspond to different colours.
# 
# For example, select a few colours [using this tool](https://doc.instantreality.org/tools/color_calculator/), and check the RGB values for that colour in the *RGB Normalized decimal* box. You should see that, for instance, to make yellow, we need a high value of red, a high value of green, and a low value of blue.
# 
# If you'd like more information, [this page](https://web.stanford.edu/class/cs101/image-1-introduction.html) presents a good summary about RGB images.
# 
# ---
# 
# 🚩 Study the [documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html) for the functions `imread()` and `imshow()` from `matplotlib.pyplot`. Then, write code below to read the `clock_0` image from `batch_0` into a NumPy array, and display the image.
# 
# You will obtain a NumPy array with shape `(101, 101, 3)`, i.e. an array which is 3 layers deep. Each of these layers is a 101x101 array, where the elements represent the intensity of red, green, and blue respectively, for each pixel. For example, the element of this array with index `[40, 20, 2]` corresponds to the amount of blue in the pixel located in row 40, column 20.
# 
# Create a second figure, with 3 sets of axes, and use `imshow()` to display each layer separately on its own set of axes. Label your figures appropriately to clearly indicate what each image is showing.
# 
# *Note: you can use `ax.imshow()` to display an image on the axes `ax`, the same way we use `ax.plot()`.*

# %%
import numpy as np
import matplotlib.pyplot as plt
pMat=plt.imread(r'clock_images./batch_0./clock_0.png') # read the picture
fig=plt.figure()
ax=fig.add_subplot(131)
im=ax.imshow(pMat[:,:,0])
ax=fig.add_subplot(132)
ax.imshow(pMat[:,:,1])# 
ax=fig.add_subplot(133)
ax.imshow(pMat[:,:,2])# 
cb_ax = fig.add_axes([1.0, 0.1, 0.02, 0.8]) #set colarbar's location
cbar = fig.colorbar(im, cax=cb_ax)     #  share colorbar
plt.show()

# %% [markdown]
# ---
# ## Task 2: Clean up the images to extract data [6 marks]
# 
# Later in Task 3, we will use **linear regression** to find the exact position of both clock hands. To perform linear regression, we will need the **coordinates of the pixels** belonging to each hand; then, we will be able to fit a line through these pixels.
# 
# This task is concerned with extracting the correct pixel coordinates from the image.
# 
# ---
# 
# 🚩 Write a function `get_clock_hands(clock_RGB)`, which takes one input argument `clock_RGB`, a NumPy array of size 101x101x3 representing an RGB image of a clock, and returns 2 NumPy arrays with 2 columns each, such that:
# 
# - In the first array, each row corresponds to the `[row, column]` index of a pixel belonging to the **hour hand**.
# - In the second array, each row corresponds to the `[row, column]` index of a pixel belonging the **minute hand**.
# 
# The goal is to obtain, for each hand, a collection of `[row, column]` coordinates which indicate where on the picture is the clock hand. You will need to figure out a way to decide whether a given pixel belongs to the hour hand, the minute hand, or neither.
# 
# 
# ---
# 
# ***Important note:*** the pictures all contain some amount of noise and blur. Depending on how you decide to count a certain pixel or not as part of a clock hand, your function will pick up different pixels. There isn't just one possible set of pixel coordinates to pick up for a given image -- the most important thing is that the pixels you extract **only** belong to one of the two hands, and not to the background for example. This will ensure that you can use linear regression efficiently.
# 
# ---
# 
# ✅ *Testing:* For example, for the tiny 7x7 clock below (a 7x7 pixel image is available in the `testing` folder for you to try your function):
# 
# | Clock | Hour hand | Minute hand |
# |:--:|:--:|:--:|
# | <img src="graphics/task2.png" alt="Task 2 example" style="width: 100px;"/> | [[1, 1]<br/> [2, 2]] | [[3, 3]<br/> [4, 3]<br/> [4, 4]<br/> [5, 4]<br/> [6, 5]] |

# %%
def get_clock_hands(clock_RGB):
    minute_hand=np.array(np.where((clock_RGB[:,:,0]<0.6) & (clock_RGB[:,:,2]<0.6) )) # Get the position based on the color range of task 1
    hour_hand=np.array(np.where((clock_RGB[:,:,1]<0.6) & (clock_RGB[:,:,2]<0.6))) # Extracts the coordinate array of the clock
    return minute_hand.T,hour_hand.T
img=plt.imread(r'testing/task2_7x7.png') 
m,h=get_clock_hands(img) 
print(m)
print(h)

# %% [markdown]
# ---
# 
# ## Task 3: Calculate the angle of the two hands [9 marks]
# 
# Now that we have pixel locations for each hand, we can estimate the **angle** between each hand and the 12 o'clock position. We will use this angle later to determine the time indicated by each hand. For instance, the figure below shows the angle made by the hour hand with the 12 o'clock position.
# 
# ![Angle between hour hand and 12 o'clock](graphics/angle.png)
# 
# ---
# 
# 🚩 Write a function `get_angle(coords)` which takes one input argument, a NumPy array with 2 columns representing `[row, column]` pixel coordinates of one clock hand, exactly like one of the arrays returned by `get_clock_hands()` from Task 2.
# 
# - Your function should use these pixel coordinates to find a **line of best fit** using linear regression.
# - Then, using this line of best fit, you should determine and **return** the angle between the clock hand and the 12 o'clock position, measured in **radians**.
# 
# The angle should take a value between $0$ (inclusive) and $2\pi$ (exclusive) radians, where $0\, \text{rad}$ corresponds to the 12 o'clock position.
# 
# ---
# 
# ***Notes:***
# 
# - When performing linear regression, you will need to pay particular attention to the case where the clock hand is vertical or almost vertical.
# - Beware of the correspondance between `[row, column]` index and `(x, y)` coordinate for a given pixel.
# - Note that the meeting point of the 2 clock hands may not be exactly at `[50, 50]`. Some of the pictures have a small offset.
# - Partial attempts will receive partial marks. For instance, if you are struggling with using linear regression, or if you don't know how to account for possible offset of the centre, you may receive partial marks if you use a simpler (but perhaps less accurate) method.
# 
# ---
# 
# ✅ *Testing:* the files `task3_hourhand.txt` and `task3_minutehand.txt` are provided for you to test your function in the `testing` folder. Use `np.loadtxt()` to read them.
# 
# With these coordinates, you should find an angle of approximately 4.2 radians for the hour hand, and 5.7 radians for the minute hand.

# %%

import numpy as np

def get_angle(coords):
    mid=50 # midpoint
    x=coords[:,1]
    y=-coords[:,0]
    mean_x=np.mean(x)
    mean_y=np.mean(y)
    k=np.sum((x-mean_x)* (y-mean_y))/(np.sum((x-mean_x)*(x-mean_x))+0.000000000000000000000000000000001)
    angle=np.arctan(k) # arctan function
    if mean_x<mid: # judge
        angle=np.pi*3/2-angle
    else:
        angle=-angle+np.pi/2
    return angle

h=np.loadtxt(r'testing/task3_hourhand.txt')
m=np.loadtxt(r'testing/task3_minutehand.txt')

print(get_angle(h))
print(get_angle(m))

# %% [markdown]
# ---
# 
# ## Task 4: Visualising the clock [6 marks]
# 
# 🚩  Use `matplotlib` and your artistic skills to visualise the clock. Write a function `draw_clock(angle_hour, angle_minute)` that takes 2 input arguments, corresponding to the two angles of the clock hands, and draw a clock with the precise location of both hands.
# 
# Your plot may include the number associated to hours, a background like a circle, an arrow head for each hand etc.
# 
# ---
# 
# ✅ *Testing:* with `angle_hour` set to $\frac{\pi}{3}$ and `angle_minute` set to $\frac{11\pi}{6}$, the hour hand should point exactly at 2, and the minute hand should point exactly at 11.
# 
# There is also an example image in the `testing` folder, which was produced entirely with `matplotlib`. This is just to give you an idea of what is possible to do -- you shouldn't attempt to reproduce this particular example, don't hesitate to get creative!

# %%
import numpy as np
import matplotlib.pyplot as plt
def draw_clock(angle_hour, angle_minute):
    
    Mid=np.array([5, 5])
    hour_rad=0.9 # hour hand radius
    min_rad=1.7 # minute radius
    txt_rad=1.8 # txt radius
    step=100
    r=2 # round frame radius
    r2=1.1 # round frame radius
    
    fig = plt.figure() 
    ax = fig.add_subplot(111) # set plot
    ax.set_aspect('equal') 
    plt.plot(np.linspace(Mid[0] - r, Mid[0] + r, step), np.sqrt(r**2 - (np.linspace(Mid[0] - r, Mid[0] + r, step)-Mid[0])**2) + Mid[1], c='k') 
    plt.plot(np.linspace(Mid[0] - r, Mid[0] + r, step), -np.sqrt(r**2 - (np.linspace(Mid[0] - r, Mid[0] + r, step)-Mid[0])**2) + Mid[1], c='k')
    plt.plot(np.linspace(Mid[0] - r2, Mid[0] + r2, step), np.sqrt(r2**2 - (np.linspace(Mid[0] - r2, Mid[0] + r2, step) -Mid[0])**2)+ Mid[1], ls='--',c='k') 
    plt.plot(np.linspace(Mid[0] - r2, Mid[0] + r2, step), -np.sqrt(r2**2 - (np.linspace(Mid[0] - r2, Mid[0] + r2, step) -Mid[0])**2) + Mid[1], ls='--',c='k')
    plt.plot(Mid[0], Mid[1], marker='s',c='green')
    
    
    # hand
    position_hour=Mid+np.array([hour_rad*np.cos(np.pi/2-angle_hour),hour_rad*np.sin(np.pi/2-angle_hour)])# 根据公式缺点指针尾部位置
    position_min=Mid+np.array([min_rad*np.cos(np.pi/2-angle_minute),min_rad*np.sin(np.pi/2-angle_minute)]) # 同理，得到分钟的位置
    ax.annotate("",xy=(position_min[0],position_min[1]),xytext=(Mid[0],Mid[1]),arrowprops=dict(arrowstyle="-|>", color="blue"),size=20)
    ax.annotate("",xy=(position_hour[0],position_hour[1]),xytext=(Mid[0],Mid[1]),arrowprops=dict(arrowstyle="-|>", color="r"),size=20)
    
    
    # text
    for i in range(12):
        textangle=i*(np.pi/6)
        text=str(i)
        pos=Mid+np.array([txt_rad*np.cos(np.pi/2-textangle),txt_rad*np.sin(np.pi/2-textangle)])
        plt.text(pos[0]-0.1,pos[1]-0.1,text,size=14)
    plt.show()

draw_clock(np.pi/3,11*np.pi/6)

# %% [markdown]
# ---
# ## Task 5: Analog to digital conversion [5 marks]
# 
# 🚩 Write a function `analog_to_digital(angle_hour, angle_minute)` that takes two input arguments, corresponding to the angles formed by each hand with 12 o'clock, and returns the time in digital format. More specifically, the output is a string showing the time in hour and minute in the format `hh:mm`, where `hh` is the hour and `mm` is the minute.
# 
# - When the hour is smaller than 10, add a leading zero (e.g. `04:30`).
# - When the hour is zero, display `12`.
# 
# At this point, your function is not concerned about the imprecision. It should calculate the hour from the hour hand, and the minute from the minute hand, separately.
# 
# ---
# ✅ *Testing:* the same angles as in Task 4 should give you `02:55`.

# %%
def analog_to_digital(angle_hour, angle_minute):
    h=str(int(np.floor(12*angle_hour/(np.pi*2))))
    m=str(int(np.round(60*angle_minute/(np.pi*2))))
    if len(h)== 1: 
        h='0'+(h)
        if h == '0': #The 0 is replaced by 13
            h='12'
    return h+':'+m
print(analog_to_digital(np.pi/3,11*np.pi/6))

# %% [markdown]
# ---
# ## Task 6: Find the misalignment [5 marks]
# 
# Now that you have extracted useful information from the pictures, you need to check if the two hands are aligned properly. To do so, you will need to find the exact time that the **small hand** is showing, in hours and minutes. Then, compare with the minutes that the big hand is showing, and report the difference.
# 
# Note that the misalignment will never be more than 30 minutes. For example, if you read a 45-minute difference between the minutes indicated by the hour hand and by the minute hand, you can realign the minute hand by 15 minutes in the other direction instead.
# 
# ---
# 
# 🚩 Write a function `check_alignment(angle_hour, angle_minute)` which returns the misalignment in minutes.
# 
# Make sure you structure you code sensibly. You may wish to use some intermediate functions to do the sub-tasks.
# 
# ---
# ✅ *Testing:* the same angles as in Task 4 should give you a 5-minute misalignment.

# %%
def check_alignment(angle_hour, angle_minute):
    h=12*angle_hour/(np.pi*2) #  Convert to hours
    alignment=np.abs((h-np.floor(h))*60-(60*angle_minute/(np.pi*2))) #Calculation error
    if alignment<30: 
        return alignment
    else:
        return 60-alignment #  If the error is greater than 30, take the smaller side
print(check_alignment(np.pi/3,11*np.pi/6))

# %% [markdown]
# ---
# ## Task 7: Putting it all together [6 marks]
# 
# Now that you have successfully broken down the problem into a sequence of sub-tasks, you need to combine all the above steps in one function.
# 
# 🚩 Write a function `validate_clock(filename)` that takes the name of an image file (a picture of a clock face) as an input argument, and returns the misalignment in minutes as an integer.
# 
# Then, write a function `validate_batch(path, tolerance)` which takes 2 input arguments: `path`, a string to indicate the path of a folder containing a batch of clock pictures, and `tolerance`, a positive integer representing the maximum tolerable number of minutes of misalignment for a clock to pass the quality control check.
# 
# Your `validate_batch()` function should write a .txt file called `batch_X_QC.txt` (where `X` should be replaced by the batch number), containing the following information:
# 
# ```
# Batch number: [X]
# Checked on [date and time]
# 
# Total number of clocks: [X]
# Number of clocks passing quality control ([X]-minute tolerance): [X]
# Batch quality: [X]%
# 
# Clocks to send back for readjustment:
# clock_[X]   [X]min
# clock_[X]   [X]min
# clock_[X]   [X]min
# [etc.]
# ```
# 
# The square brackets indicate information which you need to fill in.
# 
# - You will need to check all pictures in the given folder. You may wish to use Python's `os` module.
# - The date and time should be the exact date and time at which you performed the validation, in the format `YYYY-MM-DD, hh:mm:ss`. You may wish to use Python's `datetime` module.
# - The batch quality is the percentage of clocks which passed the quality control in the batch, rounded to 1 decimal place. For example, in a batch of 20 clocks, if 15 passed the control and 5 failed, the batch quality is `75.0%`.
# - List all clock numbers which should be sent back for realignment, in **decreasing order of misalignment**. That is, the most misaligned clock should appear first.
# - The list of clocks to send back and the misalignment in minutes should be vertically aligned, in a way which makes the report easy to read. Check the example in the `testing` folder.
# - Your function should not return anything, simply write the .txt report.
# 
# For instance, to use your function to check batch 1 with a 2-minute maximum acceptable misalignment, the command will be `validate_batch('clock_images/batch_1', 2)`.
# 
# ---
# 
# ✅ *Testing:* There is an example report in the `testing` folder (for a batch which you do not have), to check that your report is formatted correctly.
# 
# ---
# 
# 🚩 Use your function `validate_batch()` to generate quality control reports for the 5 batches of clocks provided in the `clock_images` folder, with a tolerance of 3 minutes.
# 
# Your reports should all be saved in a folder called `QC_reports`, which you should create using Python. You should generate all 5 reports and include them in your submission.
# 

# %%
import os
import time
import numpy as np
def validate_clock(filename):
    m,h=get_clock_hands(plt.imread(filename))
    h_a=get_angle(h)
    m_a=get_angle(m)
    return check_alignment(h_a,m_a)

def validate_batch(path, tolerance):
    bad_err=[] # Record errors that need to be repaired
    bad_id=[] # Record the ID of the repair
    good_nums=0 # Good clock 
    nums=0 # The total number 
    for fpath, dirname, NAME in os.walk(path):     
        for name in NAME:
            nums=nums+1
            NAME = os.path.join(fpath, name) # Iterate to get the names of all the files
            misalignment =validate_clock(NAME)# Get the error
            if misalignment <=tolerance: # If the error is less than the limit, record it
                good_nums=good_nums+1 # Calculate the value of error less than tolerance
            else: # Error greater than tolerance Record ID and error
                bad_err.append(misalignment )
                bad_id.append(int(name[6:-4]))
    INDEX=np.argsort(-np.array(bad_err)) # Sort by error size
    # Redirect output to TXT file as required
    txt = open("batch_"+str(int(path[-1]))+"_QC.txt", "w") 
    print("Batch number: {}".format(int(path[-1])),file = txt)
    print("Checked on {}".format(time.strftime("%Y-%M-%D, %H:%M:%S", time.localtime())),file = txt)
    print("",file = txt)
    print("Total number of clocks: {}".format(nums),file = txt)
    print("Number of clocks passing quality control ({}-minute tolerance): {}".format(tolerance,good_nums),file = txt)
    print("Batch quality: {:.1f}% ".format(100*good_nums/nums),file = txt)
    print("",file = txt)
    print("Clocks to send back for readjustment:",file = txt)
    for i in INDEX:
        print("clock_{:d}   {:d}min".format(bad_id[i],int(bad_err[i])),file = txt)
validate_batch('clock_images/batch_4', 5)

# %%



