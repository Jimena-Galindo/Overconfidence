#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sp
import seaborn as sns
import random
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf


# In[2]:


# the dgp
# matrices: matrix[0] is the low type, matrix[2] is the high type. column 0 is low omega, row 0 is low effort
ml = np.array([[.20, .25, .40], [.07, .30, .45], [.02, .20, .50]])
mm = np.array([[.40, .45, .65], [.30, .65, .69], [.05, .50, .80]])
mh = np.array([[.45, .55, .75], [.35, .69, .80], [.25, .65, .98]])

msc = [ml, mm, mh]

# number of periods
T = 11

# number of trials
be_trials = 10

seed = 3452


# In[3]:


# for each of the priors, simulate the choices under each of the parameterizations of the bias from attributions
# where the attribution is [c_positive, c_negative, c_negative, c_positive] for each of the possible 
# combinations of c_positive and c_negative

# create a matrix of the possible combinations of c_positive and c_negative
c_H = np.array([x for x in range(10, 100, 10)])/100
c_M = np.array([x for x in range(10, 150, 10)])/100
c_L = np.array([x for x in range(100, 200, 10)])/100

grid_good_HML = np.array(np.meshgrid(c_H, c_M, c_L)).T.reshape(-1, 3)

# turn into a dataframe
grid_good_HML = pd.DataFrame(grid_good_HML, columns = ['c_H', 'c_M', 'c_L'])

# keep only values for which c_H < c_M < c_L
grid_good_HML = grid_good_HML[grid_good_HML['c_H'] < grid_good_HML['c_M']]
grid_good_HML = grid_good_HML[grid_good_HML['c_M'] < grid_good_HML['c_L']]

#turn back into an array
grid_good_HML = np.array(grid_good_HML)


# In[4]:


# the list of possible prior beliefs on theta
priors_theta = [[1/3, 1/3, 1/3], 
                [1/2, 1/4, 1/4],
                [3/4, 1/8, 1/8],
                [9/10, 1/20, 1/20],
                [1/4, 1/2, 1/4],
                [1/8, 3/4, 1/8],
                [1/20, 9/10, 1/20],
                [1/4, 1/4, 1/2],
                [1/8, 1/8, 3/4],
                [1/20, 1/20, 9/10]]


# In[5]:


# the prior on omega is induced and uniform
prior_omega = [1/3, 1/3, 1/3]


# In[6]:


###### THIS IS THE BAYES UPDATE WITH THE BIAS PARAMETERS C######
# joint bayesian update

def joint_bayes_biased(p0, signal, M, e_index, c):
    # c should be [c_H, c_M, c_L]

    # number of sucesses
    k = sum(signal)
    n = len(signal)
    # determine if it is good news or bad news and set the parameter c accordingly
    if k>=n/2:
        c_H = c[0]
        c_M = c[1]
        c_L = c[2]
    else:
        c_L = c[2]
        c_M = c[1]
        c_H = c[0]
    
    # the probabilities of having observed each of the signals
    matrix = np.array([sp.stats.binom.pmf(k, n, M[0][e_index, :], loc=0), 
                       sp.stats.binom.pmf(k, n, M[1][e_index, :], loc=0), 
                       sp.stats.binom.pmf(k, n, M[2][e_index, :], loc=0)])
    
    
    if k>=n/2:
        matrix_bias = [[matrix[0, 0]**c_L, matrix[0, 1]**c_L, matrix[0, 2]**c_L],
                       [matrix[1, 0]**c_M, matrix[1, 1]**c_M, matrix[1, 2]**c_M],
                       [matrix[2, 0]**c_H, matrix[2, 1]**c_H, matrix[2, 2]**c_H]]
    else:
        matrix_bias = [[matrix[0, 0]**c_L, matrix[0, 1]**c_M, matrix[0, 2]**c_H],
                       [matrix[1, 0]**c_L, matrix[1, 1]**c_M, matrix[1, 2]**c_H],
                       [matrix[2, 0]**c_L, matrix[2, 1]**c_M, matrix[2, 2]**c_H]]
    
    # set the numerators
    num = np.diagflat(p0) @ np.diagflat(matrix_bias)
    #take only the diagonal
    num = np.diag(num)

    # sum all the numerators to get the denominator
    denom = np.sum(num)

    # the posterior beliefs are each of the numerators divided by the denominator
    p1 = num/denom

    # p1 has the order (00, 01, 02, 10, 11, 12, 20, 21, 22)
    
    return p1


# In[7]:


# bayesian choices (the inputs are the belief (nine-dimensional array) and the DGP (msc), returns the index of the choice that maximizes the expected utility)
# this can be used for the unbiased and the biased updates since it only takes the posterior belief ans calculates the expectated utility for each of the choices

def joint_bayes_c(p1, M):
    # compute the expected payoffs for each of the 3 choices
    # the expected payoff is the probability of success times the probability of that combination of parameters
    # Take the first row of each of the matrices in M and cancatenate them (this will match the order of the probabilities in the posterior)
    choices_1 = np.concatenate((M[0][0, :], M[1][0, :], M[2][0, :]))
    # Take the second row of each of the matrices in M and stack them
    choices_2 = np.concatenate((M[0][1, :], M[1][1, :], M[2][1, :]))
    # Take the third row of each of the matrices in M and concatenate them
    choices_3 = np.concatenate((M[0][2, :], M[1][2, :], M[2][2, :]))

    # multiply the choices by the probabilities in the posterior
    Eu= [choices_1@p1, choices_2@p1, choices_3@p1]

    e_index = np.argmax(Eu)
    
    return e_index
    


# In[8]:


# function that simulates the joint biased bayes only (this can be turned into the correct bayesian y settinc c=[1, 1, 1, 1])

def simulate_joint_bayes_biased(theta, omega, p0_theta, p0_omega, M, c, T, trials, seed, epsilon):
    
    ###### Determine the outcomes beforehand
    # set a seed for each type
    rng_H = np.random.default_rng(seed=seed)
    
    

    #############
    # generate all the draws for T periods for each type and for each effort choice
    ############

    ##### for the high types
    # outcomes after choosing L
    outcome_H_L = rng_H.binomial(1, M[2][0, omega], size=(T, trials))
    # outcomes after choosing M
    outcome_H_M = rng_H.binomial(1, M[2][1, omega], size=(T, trials))
    # outcomes after choosing H
    outcome_H_H = rng_H.binomial(1, M[2][2, omega], size=(T, trials))

    ##### for the medium types
    rng_M = np.random.default_rng(seed=seed)
    # after low effort
    outcome_M_L = rng_M.binomial(1, M[1][0, omega], size=(T, trials))
    # after medium effort
    outcome_M_M = rng_M.binomial(1, M[1][1, omega], size=(T, trials))
    # after high effort
    outcome_M_H = rng_M.binomial(1, M[1][2, omega], size=(T, trials))

    #### for the low types
    rng_L = np.random.default_rng(seed=seed)
    outcomes_L_L = rng_L.binomial(1, M[0][0, omega], size=(T, trials))
    outcomes_L_M = rng_L.binomial(1, M[0][1, omega], size=(T, trials))
    outcomes_L_H = rng_L.binomial(1, M[0][2, omega], size=(T, trials))

    # stack the outcome vectors foe each type into a matrix. first element is the effort choice, secod is t
    outcomes_H = np.stack((outcome_H_L, outcome_H_M, outcome_H_H))
    outcomes_M = np.stack((outcome_M_L, outcome_M_M, outcome_M_H))
    outcomes_L = np.stack((outcomes_L_L, outcomes_L_M, outcomes_L_H))

    # stack all the matrices into a single outcomes matrix of matrices
    outcomes = np.stack((outcomes_L, outcomes_M, outcomes_H))
    
    
    #############
    # set empty vectors where all the data will be saved period by period for each of the models
    ############
    # beliefs
    # take every value of p0_theta and multiply by each value of p0_omega
    p_joint_bayes_biased = [np.kron(p0_theta, p0_omega)]
    
    # choices
    e_joint_bay_biased = [joint_bayes_c(p_joint_bayes_biased[0], M)]
    signal = [0]
    
    signals = outcomes[theta]
    
    for t in range(T):
        # get the signals 
        
        signal_bay = signals[e_joint_bay_biased[t], t]
        signal.append(sum(signal_bay))
        
        # update beliefs 
        
        p1_joint = joint_bayes_biased(p_joint_bayes_biased[t], signal_bay, M, e_joint_bay_biased[t], c)
        p_joint_bayes_biased.append(p1_joint)
    
        
        # Choices

        # draw a random number between 0 and 1 to determine if the agent will tremble or not
        tremble = np.random.uniform(0, 1)
        # if the agent trembles, then choose a random effort level
        if tremble<epsilon:
            e_joint_biased_t = np.random.randint(0, 3)
        else:
        # if the agent does not tremble, then choose the effort level that maximizes the expected utility
            e_joint_biased_t = joint_bayes_c(p_joint_bayes_biased[t], M)
        
        e_joint_bay_biased.append(e_joint_biased_t)
        
    return e_joint_bay_biased, signal


# In[9]:


# load the observed data
updates = pd.read_csv('../Clean/updates.csv')


# In[10]:


# tremble in choices
round1 = updates[updates['round_number']==1]
epsilon = .1


# In[11]:


# prior distribution
prior = updates.groupby(['belief', 'certainty']).size().reset_index(name='counts')
prior['prob'] = prior['counts']/prior['counts'].sum()


# In[12]:


# calculate the probability of each type
parametrizations = updates.groupby(['type', 'rate'])['code'].count().reset_index(name='counts')
parametrizations['prob'] = parametrizations['counts']/parametrizations['counts'].sum()


# In[13]:


# function that maps each pair of belief and certainty to the prior on theta
def prior_map(belief, certainty):
    if belief == 0:
        if certainty==100:
            p0 = [9/10, 1/20, 1/20]
        elif certainty==75:
            p0 = [3/4, 1/8, 1/8]
        elif certainty==50:
            p0 = [1/2, 1/4, 1/4]
        else:
            p0 = [1/3, 1/3, 1/3]
    elif belief == 1:
        if certainty==100:
            p0 = [1/20, 9/10, 1/20]
        elif certainty==75:
            p0 = [1/8, 3/4, 1/8]
        elif certainty==50:
            p0 = [1/4, 1/2, 1/4]
        else:
            p0 = [1/3, 1/3, 1/3]
    elif belief == 2:
        if certainty==100:
            p0 = [1/20, 1/20, 9/10]
        elif certainty==75:
            p0 = [1/8, 1/8, 3/4]
        elif certainty==50:
            p0 = [1/4, 1/4, 1/2]
        else:
            p0 = [1/3, 1/3, 1/3]
    else:
        p0 = [1/3, 1/3, 1/3]
    
    return p0
        


# In[14]:


# for each possible set of parameters in the grid, simulate the data for multiple agents
#
# start a list where all the dataframes will be saved
sim_all = []
#pd.DataFrame(columns=['round', 'effort', 'theta', 'omega', 'c_H', 'c_M', 'c_L', 'ind', 'signal'])

for i in range(len(grid_good_HML)):
    c = grid_good_HML[i]
    # parameter level data
    simulation_c= pd.DataFrame(columns=['round', 'effort', 'theta', 'omega', 'c_H', 'c_M', 'c_L', 'ind', 'signal'])
    N=500
    # simulate a sample of N agents. 
    for i in range(N):
        # For each agent draw a type from the distribution of parametrizations
        # draw an integer from 0 to 8 where the probability of each integer is given by the column prob in parametrizations
        # this will be the index of the row in parametrizations that will be chosen
        # the row will have the type and the rate of the agent
        theta_index = np.random.choice(9, p=parametrizations['prob'])
        # get the type and the rate
        theta = parametrizations['type'][theta_index]
        omega = parametrizations['rate'][theta_index]

        # For each agent draw a prior from the distribution of priors
        # draw an integer from 0 to 12 where the probability of each integer is given by the column prob in prior
        # this will be the index of the row in prior that will be chosen
        # the row will have the prior on theta and the certainty of the agent
        prior_index = np.random.choice(13, p=prior['prob'])
        # get the belief and the certainty
        belief = prior['belief'][prior_index]
        certainty = prior['certainty'][prior_index]

        # map the belief and the certainty to the prior on theta
        p0_theta = prior_map(belief, certainty)

        # set the round_numbers
        rounds = [t+1 for t in range(T+1)]

        #individual level data
        simulation_i = pd.DataFrame(columns=['round', 'effort', 'theta', 'omega', 'c_H', 'c_M', 'c_L'])
        
        e, s= simulate_joint_bayes_biased(theta, omega, p0_theta, prior_omega, msc, c, T, be_trials, seed, epsilon)

        simulation_i['round'] = rounds
        simulation_i['theta'] = theta
        simulation_i['omega'] = omega
        simulation_i['effort'] = e
        simulation_i['signal'] = s
        simulation_i['ind'] = str(i)+ str(c)
        simulation_i['belief'] = belief
        simulation_i['certainty'] = certainty

        # append to the dataframe for the parameters
        simulation_c=simulation_c.append(simulation_i)
        
    # add columns with the parameters of the simulation
    simulation_c['c_H'] = c[0]
    simulation_c['c_M'] = c[1]
    simulation_c['c_L'] = c[2]

    # return a list of dataframes. One for each set of parameters in the grid
    sim_all.append(simulation_c)
  


# In[15]:


# add a column with the index of the parameterization to each dataframe
for i in range(len(sim_all)):
    sim_all[i]['parametrization'] = i  

# stack all the elements of the list into a single dataframe
sim_all = pd.concat(sim_all)


# In[16]:


# drop rows in which signal is nan
sim_all = sim_all.dropna(subset=['signal'])
# change signal_previous to integer
sim_all['signal'] = sim_all['signal'].astype(int)
# change parametrization to integer
sim_all['parametrization'] = sim_all['parametrization'].astype(int)
# change round to integer
sim_all['round'] = sim_all['round'].astype(int)
# change effort to integer
sim_all['effort'] = sim_all['effort'].astype(int)
# change theta to integer
sim_all['theta'] = sim_all['theta'].astype(int)
# change omega to integer
sim_all['omega'] = sim_all['omega'].astype(int)
# change belief to integer
sim_all['belief'] = sim_all['belief'].astype(int)
# change certainty to integer
sim_all['certainty'] = sim_all['certainty'].astype(int)


# In[17]:


# for each possible parametrization, estimate the moments: regression parameters for the reaction to good news and bad news

# add a column called news_previous that is the value of the signal in the previous period
sim_all['signal_previous'] = sim_all.groupby(['ind'])['signal'].shift(1)

# add a column called 'good_news' that is 1 if the previous signal is 5 or more and 0 otherwise
sim_all.loc[sim_all['signal_previous']>=5, 'good_news'] = 1
sim_all.loc[sim_all['signal_previous']<5, 'good_news'] = 0

# add a column called 'effort_change' that is the difference between effort in the round and effort in the previous round
sim_all['effort_change'] = sim_all.groupby(['ind'])['effort'].diff()
    


# In[18]:


# calculate the moments for each parametrization (regression parameters for the reaction to good news and bad news)
results = []
for i in sim_all['parametrization'].unique():
    # regression of effort change on signal_previous, good_news, and the interaction of the two
    # the regression is run only for round>1 and for parametrization i
    results_i = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=sim_all[(sim_all['round']>2) & (sim_all['parametrization']==i)]).fit()
    results.append([results_i, i])


# In[19]:


# create the same columns for updates
updates['signal_previous'] = updates.groupby(['code'])['signal'].shift(1)
updates.loc[updates['signal_previous']>=5, 'good_news'] = 1
updates.loc[updates['signal_previous']<5, 'good_news'] = 0
updates['effort_change'] = updates.groupby(['code'])['effort'].diff()

# run the regression for the observed data
results_obs = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=updates[(updates['round_number']>1)]).fit()


# In[20]:


data_reg = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=updates[(updates['round_number']>2)]).fit()

data_reg.summary()


# In[40]:


results_ego = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=updates[(updates['round_number']>1)& (updates['treatment']=='ego')]).fit()


# In[41]:


results_stereo = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=updates[(updates['round_number']>1)& (updates['treatment']=='stereotype')]).fit()


# In[21]:


# get the coefficients from the regression of the observed data
coeff_obs = results_obs.params

# weighting matrix of size 4
W = np.diag(1/data_reg.bse)

# get the coefficients from the regression of the simulated data and get the value of the objective function
quad_form_value = []
for i in range(len(results)):
    # the coefficients in the simulation for parametrization i
    coeff_sim = ((results[i][0].params - results_obs.params).T)@ W @(results[i][0].params - results_obs.params)
    quad_form_value.append([coeff_sim, i])


# In[42]:


quad_form_ego = []
for i in range(len(results)):
    # the coefficients in the simulation for parametrization i
    coeff_sim = ((results[i][0].params - results_ego.params).T)@ W @(results[i][0].params - results_ego.params)
    quad_form_ego.append([coeff_sim, i])


# In[44]:


quad_form_stereo = []
for i in range(len(results)):
    # the coefficients in the simulation for parametrization i
    coeff_sim = ((results[i][0].params - results_stereo.params).T)@ W @(results[i][0].params - results_stereo.params)
    quad_form_stereo.append([coeff_sim, i])


# In[22]:


# transform the list into a dataframe
quad_form_value = pd.DataFrame(quad_form_value, columns=['quad_form_value', 'parametrization'])


# In[23]:


# find the parametrization for which the objective function is minimized
min_index = quad_form_value['quad_form_value'].idxmin()

# get the row from parametrization for which 
sim_all[sim_all['parametrization']==min_index][['c_H', 'c_M', 'c_L']].groupby(['c_H', 'c_M', 'c_L']).mean()


# In[43]:


quad_form_ego = pd.DataFrame(quad_form_ego, columns=['quad_form_ego', 'parametrization'])
# find the parametrization for which the objective function is minimized
ego_index = quad_form_ego['quad_form_ego'].idxmin()

# get the row from parametrization for which 
sim_all[sim_all['parametrization']==min_index][['c_H', 'c_M', 'c_L']].groupby(['c_H', 'c_M', 'c_L']).mean()


# In[45]:


quad_form_stereo = pd.DataFrame(quad_form_stereo, columns=['quad_form_stereo', 'parametrization'])
# find the parametrization for which the objective function is minimized
stereo_index = quad_form_stereo['quad_form_stereo'].idxmin()

# get the row from parametrization for which 
sim_all[sim_all['parametrization']==min_index][['c_H', 'c_M', 'c_L']].groupby(['c_H', 'c_M', 'c_L']).mean()


# In[24]:


results[min_index][0].summary()


# In[27]:


data_reg = smf.ols('effort_change ~ signal_previous + good_news + signal_previous:good_news', data=updates[(updates['round_number']>2)]).fit()

data_reg.summary()


# In[ ]:





# In[ ]:




