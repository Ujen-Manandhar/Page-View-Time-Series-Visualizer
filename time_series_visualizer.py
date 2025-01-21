import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col=0, parse_dates=True)

# Clean data
df = df.loc[df.value.between(df.value.quantile(0.025), df.value.quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    
    fig = plt.figure(figsize=(20, 9))
    plt.plot(df.copy().index, df.copy().value, c='r')

    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month

    # grouping 
    df_group = df_bar.groupby(['Years', 'Month'])[['value']].mean()
    df_group = df_group.unstack()
    df_group.columns = [ 
        'January', 'February', 'March', 'April', 
        'May', 'June', 'July', 'August', 'September', 
        'October', 'November', 'December']

    # Draw bar plot
    fig, axis = plt.subplots(figsize=(10,10))
    df_group.plot.bar(ax=axis)
    axis.set_ylabel('Average Page Views')
    axis.legend(title= 'Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]

    # sorting the month value
    df_box['month'] = [d.month for d in df_box.date]
    df_box.sort_values(by='month', inplace=True)
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0], hue='year', palette={2016:'blue', 2017:'orange', 2018:'green', 2019:'red'}, legend=False, fliersize=1)
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')


    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1], hue='month', palette='husl', fliersize=1)
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
