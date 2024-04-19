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


# Set up and formatting for particular charts:
def get_plot_comparison(x1, y1, x2, y2, x3, y3):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Spending versus income and budget by month')
    plt.plot(x1, y1, c='#F0FF42', label='Expenses')
    plt.plot(x2, y2, c='#82CD47', label='Income')
    plt.plot(x3, y3, c='#54B435', label='Budget')
    plt.xlabel('Month')
    plt.ylabel('A$')
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize = 6)
    plt.tight_layout()
    graph = get_graph()
    return graph


# def get_plot_daily(x1, y1):
#     plt.switch_backend('AGG')
#     plt.figure(figsize=(5,3))
#     plt.title('Average daily spend')
#     plt.plot(x1, y1, c='#03C03C')
#     plt.xlabel('Day')
#     plt.xticks(rotation=90)
#     plt.ylabel('A$')
#     plt.tight_layout()
#     graph = get_graph()
#     return graph


def get_bar_total(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Total monthy spend')
    plt.bar(x, y, color="#03C03C")
    plt.ylabel('Expense amount (A$)')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar_average(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Average monthly spend')
    plt.bar(x, y, color="#03C03C")
    plt.ylabel('Expense amount (A$)')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_pie_current_expenses(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(3,3))
    plt.title('Current month spend by category')
    plt.pie(x, labels=y, textprops={'fontsize': 7}, colors=['#F0FF42', '#82CD47', '#54B435', '#379237', '#ffdfba', '#ffb3ba', '#bae1ff'], autopct="%.0f%%", pctdistance=0.8)
    plt.tight_layout()
    graph = get_graph()
    return graph
