import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 1. Create a Pareto chart of the top 10 states with the highest average number
# of vehicles per household in 2016
def exe_1(df):
    # Get average vehicles for each state
    colName = "2016 Vehicles per Household"

    stateData = df.groupby(by='States')[colName].mean()
    df = stateData.to_frame()

    plt.figure()
    p = df.nlargest(10, colName)

    # plot bar chart
    p.plot(y=colName,kind='bar')
    plt.ylabel('Vehicles', fontsize = 8)

    # plot cumulative distribution line
    population_col = df.nlargest(10, colName)[colName].copy()
    p=1.0*population_col.cumsum()/population_col.sum()
    p.plot(color='r',secondary_y= True,style='-o')
    plt.ylabel('Cumulative Frequency',fontsize = 8)

    plt.title('Top 10 states with the highest Vehicles per Household in 2016\n')

    plt.show()


# 2. Create a relative frequency distribution histogram from the “2016 percentage of
# households without vehicles” for the entire country. Comment on the shape of the
# distribution.
def exe_2(df, col = '2016 Households Without Vehicles'):
    df.hist(col, bins = 'auto', density = 1)
    plt.xlabel('rate')
    plt.ylabel('relative frequency')
    plt.title("Relative frequency distribution histogram of "+col+'\n')
    plt.show()


# 3. Create a cumulative frequency line plot of the “2016 percentage of households
# without vehicles” for the entire country.
def exe_3(df, col = '2016 Households Without Vehicles'):
    dom_rate_col = df[col].copy()

    min_value = dom_rate_col.min()
    max_value = dom_rate_col.max()
    interval = (max_value-min_value)/10
    label = [round(min_value+i*interval,2) for i in range(0,11)]
    dom_rate_col.sort_values(inplace=True)
    class_boundaries = pd.cut(dom_rate_col,11, labels = label)
    class_boundaries = class_boundaries.value_counts()
    frequency_df=pd.DataFrame(class_boundaries,columns=[col])

    frequency_df.sort_index(inplace=True)
    frequency_df['relative frequency'] = frequency_df[col].cumsum()
    frequency_df.plot(y='relative frequency', kind='line',
        figsize=(10, 8), legend=True, style='yo-')
    print(label)
    plt.xlabel('rate')
    plt.ylabel('cumulative frequency')
    plt.title("a cumulative frequency line plot " + col + '\n')
    plt.show()



# 4. Perform numerical descriptive statistics for the “2016 Vehicles per Household” for
# the entire country.
def exe_4(df, col = '2016 Vehicles per Household'):
    dom_rate_col = df[col].copy()
    print(pd.Series(
    [
        dom_rate_col.count(),
        dom_rate_col.min(),
        dom_rate_col.idxmin(),
        dom_rate_col.quantile(.25),
        dom_rate_col.median(),
        dom_rate_col.quantile(.75),
        dom_rate_col.mean(),
        dom_rate_col.max(),
        dom_rate_col.idxmax(),
        dom_rate_col.mad(),
        dom_rate_col.var(),
        dom_rate_col.std(),
        dom_rate_col.skew(),
        dom_rate_col.kurt()
    ],
    index = [
        'sum',
        'minimum',
        'minimum index',
        'Q1',
        'median',
        'Q3',
        'mean',
        'maximum',
        'maximum index',
        'mad(Median absolute deviation)',
        'variance',
        'standard deviation',
        'skew',
        'kurtosis'
    ]))

# 5. For the “2016 percentage of households without vehicle” for the entire country,
# determine whether there are any outliers. Comment on the states to which the
# outliers belong.
def exe_5(df, col = '2016 Households Without Vehicles'):
    outliers=[]

    df_list = df[col].copy()
    q1 = df_list.quantile(.25)
    q3 = df_list.quantile(.75)
    min_threshold, max_threshold = round(q1 - 1.5 * (q3 - q1), 2), round(q3 + 1.5 * (q3 - q1), 2)

    for index, row in df.iterrows():
        if row[col] < min_threshold or row[col]>max_threshold:
            outliers.append(row[col])
    count = 0
    for o in outliers:
        count+=1
        print("%4.1f\t"%o,end='')
        if count%8 == 0: print('\n')

#Repeat tasks 2-5 above for the “2015 percentage of households without vehicle”.
# Describe whether there are any similarities or dissimilarities in the distributions of
# the two variables that you have analyzed (the two variables are: “2016 percentage
# of households without vehicles” and “2015 percentage of households without
# vehicles”)
def exe_6(df):
    # col = '2015 Households Without Vehicles'
    col = '2016 Households Without Vehicles'
    # exe_2(df, col)
    # exe_3(df, col)
    exe_4(df, col)
    exe_5(df, col)

# 7. Create a scatter plot of the "2015 Vehicles per Household" versus "2016 Vehicles per Household".
#    Use the scatter plot to describe whether there exists a correlation between the two quantities above.
#    Interpret their correlation in words.
def exe_7(df):
    f = plt.figure()
    plt.scatter(df['2015 Vehicles per Household'], np.log(df['2016 Vehicles per Household']), marker='o', s= 5)
    plt.xlabel('2015 Vehicles per Household')
    plt.ylabel('2016 Vehicles per Household')
    plt.title('a scatter plot of the "2015 Vehicles per Household" versus "2016 Vehicles per Household"')
    f.set_size_inches(10, 5)
    plt.show()


if __name__ == '__main__':

    # panda read csv file
    df = pd.read_csv('uscars.csv', index_col='Jusidiction')

    # uncomment to run

    exe_1(df)
    exe_2(df)
    exe_3(df)
    exe_4(df)
    exe_5(df)
    exe_6(df)
    exe_7(df)
