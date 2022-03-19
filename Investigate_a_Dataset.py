#!/usr/bin/env python
# coding: utf-8

# This dataset collects information from 100k medical appointments in Brazil and is focused on the question of whether or not patients show up for their appointment. A number of characteristics about the patient are included in each row.
# 
# 
# # Project: Investigate a Dataset - [No-show Appointments / may-2016.csv]
# 
# ## Table of Contents
# 
# 1)ScheduledDay’ tells us on what day the patient set up their appointment.
#      (2)Neighborhood’ indicates the location of the hospital.
#      (3)Scholarship’ indicates whether or not the patient is enrolled in Brasilian welfare program Bolsa Família.
#     (4)No_show’ it says ‘No’ if the patient showed up to their appointment, and ‘Yes’ if they did not show up.
# 

# In[73]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
#Data Analysis
import pandas as pd
import numpy as np
from datetime import datetime as dt

#data Visualization 
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

print("Importing Done")
#from scipy import stats  



# In[55]:


# Upgrade pandas to use dataframe.explode() function. 
get_ipython().system('pip install --upgrade pandas==0.25.0')


# <a id='wrangling'></a>
# ## General properties
# 
# 
# 

# In[74]:


# Load your data and print out a few lines. Perform operations to inspect data
# types and look for instances of missing or possibly errant data.

df = pd.read_csv("noshowappointments-kagglev2-may-2016.csv")
df.head()


# In[75]:


#explor the shape of data
df.shape


# In[76]:


#reading dataset in general information
df.info()


# In[77]:


sns.pairplot(df.sample(1000));


# In[78]:


#check if there any missing values Or data
df.isnull().sum()


# In[79]:


#check for duplication
df.duplicated().sum()


# In[80]:


#check for un unique value 
df['PatientId'].nunique()


# In[81]:


#check no of duplicated IDS of patient
df['PatientId'].duplicated().sum()


# In[82]:


#check for duplication patient and noshow
df.duplicated(['PatientId','No-show']).sum()


# In[83]:


#more information about data
df.describe()


# In[84]:


#Identfy the row index of -1 value of age 
mask=df.query('Age=="-1"')
mask


# In[85]:


#unique value for each column
df.nunique()


# In[86]:



# count appointment numbers for each age
df['Age'].value_counts()


# In[87]:



# check the age datas by order
df_age = df['Age'].unique()
df_age.sort()
print('age', df_age)
#same to == print('Age:', sorted(df['Age'].unique()))


# In[88]:


# drop the data with age < 0 and age >=98
df = df[(df.Age >= 0) & (df.Age < 98)]
df.info()


# In[89]:


# extract only 'yyyy-mm-dd' from the string including time
df['ScheduledDay'] = df['ScheduledDay'].str[0:10]
df['AppointmentDay'] = df['AppointmentDay'].str[0:10]

# verify if the extration has been done correctly
df.head(3)


# In[90]:


df.head()


# In[91]:


# check the age datas by order
df_age = df['Age'].unique()
df_age.sort()
print('age', df_age)
#same to == print('Age:', sorted(df['Age'].unique()))


# 
# ### Data Cleaning
# At this stage, we will delete the wrong data that affects the results of the analysis and also delete the unimportant data.
#  

# In[92]:


# After discussing the structure of the data and any problems that need to be
#   cleaned, perform those cleaning steps in the second part of this section.
# create a boxplot of the age using seaborn


#rename 3 column
df.rename(columns={'Handcap':'Handicap','Hipertension':'hypertension','No-show':'No_show'}, inplace=True )
#Verving if renaming true 
df.info()


# In[94]:


df['No_show'].value_counts()


# In[95]:


# define the percentage function, total here is the number of rows
def percentage(number, total):
    return number / total


# In[96]:



# calculate the percentage of patients did not presented
df_nshow = df[df.No_show == 'Yes']
number_noshow = df_nshow['No_show'].count()
per_noshow = percentage(number_noshow, total = 110508)
print(per_noshow)


# In[97]:



# calculate the percentage of patients who presented
df_show = df[df['No_show'] == 'No']
number_show = df_show['No_show'].count()
per_show = percentage(number_show, total = 110508)
print(per_show)


# In[98]:



# calculate mean
df['Age'].mean()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# Exploratory Data Analysis
# 
# After we've cleaned up the data,now we are ready to move on to exploration, such as calculating statistics and graphics to address the research questions you asked in the Introduction section.
# 
# ### Research Question 1 (Replace this header name!)

# In[99]:



df.hist(figsize=(16,8));


# ### Research Question 2  (Replace this header name!)

# In[100]:


# Continue to explore the data to address your additional research
#   questions. Add more headers as needed if you have more questions to
#   investigate.

# draw a pie graph to show the percentage of the patients presented or not
sizes = np.array([per_noshow, per_show])
labels = 'No_shown', 'Shown'
colors = ["lightskyblue", "Yellow"]
explode = [0.2, 0]
plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, autopct = '%.2f%%', radius = 1.5)
plt.title('Percentage of present patients', fontsize = 17, loc = 'center', color = 'k')
plt.axis('equal') 
# equal aspect ratio to ensure that pie is drawn as a circle
plt.show()


# In[101]:


# count number of shown and non-shown patients by gender
df_g = df['No_show'].groupby(df['Gender']).value_counts()
# display the result
df_g


# In[102]:


#Number of shown-up or not patients with scheduled appointment by gender
df_g.plot(x=['No_shown', 'Shown'], y=['No', 'Yes'], kind ='bar', title = 'Number of shown-up or not patients with scheduled appointment by gender')
plt.ylabel('Number of patient')


# In[103]:



# calculate total female patients
df_f = df[df['Gender'] == 'F']
total_f = df_f['Gender'].count()
# calculate percentage of female patients no-shown-up and shown-up
df_fns = df_f[df_f.No_show == 'Yes']
number_fns = df_fns.No_show.count()
per_fns = percentage(number_fns, total_f) 
#percentage of female no-shown-up
per_fs = 1-per_fns 
#percentage of female shown-up
print(per_fns, per_fs)


# In[106]:


# calculate total male patients
df_m = df[df['Gender'] == 'M']
total_m = df_m['Gender'].count()
# calculate percentage of male patients no-shown-up and shown-up
df_mns = df_m[df_m.No_show == 'Yes']
number_mns = df_mns.No_show.count()
per_mns = percentage(number_mns, total_m) 
#percentage of female no-shown-up
per_ms = 1-per_mns 
#percentage of female shown-up
print(per_mns, per_ms)


# In[107]:


#Figer out the presence and gender 
#gender does  affect the attendance rate or not ??
#percentage of presence of gender 
f = (round(per_fns*100,2), round(per_fs*100,2))
m = (round(per_mns*100,2), round(per_ms*100,2))
ind = np.arange(len(m))
width = 0.25

fig,ax = plt.subplots()
rects1 = ax.bar(ind - width/2, m, width,
                color='SkyBlue', label='Male')
rects2 = ax.bar(ind + width/2, f, width,
                color='Green', label='Female')

ax.set_ylabel('Percentage')
ax.set_title('Percentage by presence and gender', fontsize = 14)
ax.set_xticks(ind)
ax.set_xticklabels(('No_shown', 'Shown'))
ax.legend()

def autolabel(rects, xpos='center'):

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

autolabel(rects1, "left")
autolabel(rects2, "right")
plt.show()


# In[ ]:


#From the previous two figures, we conclude that gender does not affect the attendance rate, but the percentage of sick women is higher than men


# <a id='conclusions'></a>
# ## Conclusions
# 1) Overall, there wasn't a huge difference in age for those who did or didn't show up to appointments. I believe the difference would have been bigger had the group who did show up for appointments not been nearly 4 times larger than the group of people who didn't show up for appointments.
# 
# 2) While the age differences aren't very wide, the people who didn't show up to appointments tended to be younger and that is also the same for whether or not these 2 groups of people had healthcare scholarships. Again, this is also possibly caused by the fact that the No-show=Yes group is about 4 times smaller than the other group.
# 
# 3) Overall, after exploring and cleaning this dataset - I don't believe there is definitive proof that either Age nor Scholarship status has an impact on whether or not a person shows up for their appointment or not. This > is partly due to the fact that the number of people who did show up for appointments was nearly four times more than the number of people who didn't show up for appointments.
# 
# ### Limitations
# 1) Given that Scholarship only has 0 or 1 for possible answers - it was tough to find good visuals that would also be able to work with Scholarship and still provide some insight and be easy to understand.
# 
# 2) Lots of the columns used categorical data which makes it more difficult to analyze and visualize. This in turn somewhat hinders the ability to find any strong correlations between columns.
# 
# 3) Again, the unbalance split between the No-show Yes and No-show No groups did't allow for a truly balanced or > equal analysis to be done but at the same time this uneven split showed some potentially interesting areas that > could be further explored.
# 

# In[1]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




