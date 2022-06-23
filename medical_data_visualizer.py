import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = df = pd.read_csv('medical_examination.csv' , index_col=None)

# Add 'overweight' column
df['overweight'] = (df['weight'] / ((df['height']/100)**2)).apply(lambda x: 1 if x > 25 else 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] =df['cholesterol'].apply(lambda x: 0 if x ==1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x ==1 else 1)
# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(frame=df, id_vars=["cardio"] , value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    group_data_0 = df_cat[(df_cat['cardio'] == 0)].groupby(['value', 'variable']).count() #sum function
    group_data_0 = group_data_0.reset_index()
    group_data_0['total']=group_data_0['cardio']
    group_data_0['cardio']=0

    group_data_1 = df_cat[(df_cat['cardio'] == 1)].groupby(['value', 'variable']).count() #sum function
    group_data_1 = group_data_1.reset_index()
    group_data_1['total']=group_data_1['cardio']
    group_data_1['cardio']=1
    df_cat = pd.concat([group_data_0, group_data_1])

    # Draw the catplot with 'sns.catplot()'

    sns.set_theme(style="ticks")
    fig = sns.catplot(x="variable" , data=df_cat, kind="bar", y="total", hue='value', col = "cardio", ci="sd", palette="dark", alpha=.6, height=6).fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat =  df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) &  (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975)) ]


    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask =  np.triu(np.ones_like(corr))
    print(mask)




    # Set up the matplotlib figure
    fig , ax =  plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'

    ax = sns.heatmap(corr, annot = True, mask=mask, fmt = '.1f')

    # Do not modify the next two lines
    fig.figure.savefig('heatmap.png')
    return fig
