#!/usr/bin/env python
# coding: utf-8
from GamesBetweenTeamsClassCopy import *
# In[3]:


import statsapi
import pandas as pd
import bnlearn



# In[4]:

this = GamesBetweenTeamsClassCopy(143, 120, '01/01/2000', '12/31/2019')

pdf = this.convert_ops_era_to_df()


# In[15]:


#pdf


# In[16]:


#ax = pdf.plot.line()


# In[17]:


OPS = pdf.drop(columns = [ 'Pera(D)', 'Wera(D)'])


# In[ ]:





# In[34]:


#OPS.plot.line()


# ### Both of the games have a linear relationship where when one team bats better the other also does better. However Washington Nats continues to outperform on the sector.

# In[19]:


ERA = pdf.drop(columns = [ 'Pops(A)', 'Wops(A)'])


# In[33]:


#ERA.plot.line()


# ### Pitching also has a relationship where one teams blunders proportionally makes the other team Worse. ERA has a negative relationship with the lower the score being better for the team. 
# 

# In[21]:


pdf['Pera(D)'] = (pdf['Pera(D)']/10 * -1 )+ 1
pdf['Wera(D)'] =  (pdf['Wera(D)']/10 * -1 )+ 1


# In[22]:


pdf


# In[23]:


pdf['Pops(A)'] = pdf['Pops(A)'].apply(lambda x: round(10 * (x)))
pdf['Wops(A)'] = pdf['Wops(A)'].apply(lambda x: round(10 * (x)))
pdf['Pera(D)'] = pdf['Pera(D)'].apply(lambda x: round(10 * (x)))
pdf['Wera(D)'] = pdf['Wera(D)'].apply(lambda x: round(10 * (x)))


# In[24]:


pdf


# In[25]:


#pdf.plot.line()


# In[26]:


from bayespy.inference import VB


# In[35]:


edges = [ 
    ('Pops(A)', 'WinsW'),
    ('Wops(A)', 'WinsW'),
    ('Pera(D)','WinsW' ),
    ('Wera(D)', 'WinsW'),
    ('Pera(D)','Wops(A)'),                                         
    ('Wera(D)', 'Pops(A)'),
]


# In[36]:


# Structure learning
DAG = bnlearn.make_DAG(edges)
# Plot
bnlearn.plot(DAG)


# In[37]:


DAG = bnlearn.parameter_learning.fit(DAG, pdf, methodtype='bayes')


# In[38]:


#bnlearn.print_CPD(DAG)


# In[39]:


Pera = round(((9.00/10 * -1) + 1) *10)
Wera = round(((8.00/10 * -1) + 1) * 10)
#q1 = bnlearn.inference.fit(DAG, variables=['WinsW'], evidence={'Wops(A)':round(1.138 * 10), 'Pops(A)':round(0.738 * 10), 'Wera(D)': Wera,'Pera(D)': Pera})
#q1 = bnlearn.inference.fit(DAG, variables=['WinsW'], evidence={'Wops(A)':1, 'Pops(A)':0, 'Wera(D)': 1,'Pera(D)': 0})
q1 = bnlearn.inference.fit(DAG, variables=['WinsW'], evidence={'Wops(A)':round(1.138 * 10)})


# ### SABRmetrics is the empirical analysis of baseball, especially baseball statistics that measure in-game activity. Or SABR  Society for American Baseball Research,
# 
# WAR = (Batting Runs + Base Running Runs +Fielding Runs + Positional Adjustment + League Adjustment +Replacement Runs) / (Runs Per Win)
# *for pitchers it is a bit more difficult*
# https://library.fangraphs.com/misc/war/
# 
# FIP- Fielding Independent Pitching (FIP) measures what a player’s ERA would look like over a given period of time if the pitcher were to have experienced league average results on balls in play and league average timing. 
# FIP = ((13*HR)+(3*(BB+HBP))-(2*K))/IP + constant //hr is awful so 13 weight //BB - Walk //HBP - hit by pitch k strike out you want these. //innings pitchd 
# https://library.fangraphs.com/pitching/fip/
# Ra9War Runs/IP x 9

# In[40]:


#df = pd.DataFrame(lst)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




