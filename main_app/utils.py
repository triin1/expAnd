import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Configuration to get matplotlib working
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# Function to add data labels to bar chart columns (in the middle of the column, rounded to 0 digits)
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i]//2, '{:,.0f}'.format(y[i]), ha='center')

def addlabels_single(x, y):
    plt.text(x, y // 2, '{:,.0f}'.format(y), ha='center')

# Set up and formatting for particular charts:
def get_plot_comparison(x1, y1, x2, y2, x3, y3):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Expenses versus income and budget by month')
    plt.plot(x1, y1, c='#F0FF42', label='Expenses')
    plt.plot(x2, y2, c='#82CD47', label='Income')
    plt.plot(x3, y3, c='#54B435', label='Budget')
    plt.ylabel('Amounts in currency')
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize = 6)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_total(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Total monthly spend')
    plt.bar(x, y, color="#03C03C")
    plt.ylabel('Expense amount')
    addlabels(x, y)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_average(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Average monthly spend')
    plt.bar(x, y, color="#03C03C")
    plt.ylabel('Expense amount')
    addlabels(x, y)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_daily(x1, y1):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,3))
    plt.title('Daily spend')
    plt.bar(x1, y1, color='#03C03C')
    plt.xlabel('Day')
    plt.ylabel('Expense amount')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_homemonth(x1, y1, x2, y2, x3, y3):
    plt.switch_backend('AGG')
    # plt.figure(figsize=(5,3))
    plt.title("Current month's expense, budget and income")
    plt.bar(x1, y1, color='#03C03C')
    plt.bar(x2, y2, color='#03C03C')
    plt.bar(x3, y3, color='#03C03C')
    plt.ylabel('Amount')
    addlabels_single(x1, y1)
    addlabels_single(x2, y2)
    addlabels_single(x3, y3)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_homeyear(x1, y1, x2, y2, x3, y3):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title("Current year's expense, budget and income")
    plt.bar(x1, y1, color='#03C03C')
    plt.bar(x2, y2, color='#03C03C')
    plt.bar(x3, y3, color='#03C03C')
    plt.ylabel('Amount')
    addlabels_single(x1, y1)
    addlabels_single(x2, y2)
    addlabels_single(x3, y3)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_pie_current_expenses(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Current month spend by category')
    plt.pie(x, labels=y, textprops={'fontsize': 7}, colors=['#F0FF42', '#82CD47', '#54B435', '#379237','#FFF0CB',  '#b1d5e3', '#e8d062'], autopct="%.0f%%", pctdistance=0.8)
    plt.tight_layout()
    graph = get_graph()
    return graph
