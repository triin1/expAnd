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


# TODO - formatting for particular charts, get rid of the ones you end up not using:
def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('category expenses')
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('category')
    plt.ylabel('expense')
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_scatter(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,5))
    plt.scatter(x,y)
    plt.tight_layout()
    graph = get_graph()
    return graph


def get_bar(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(5,3))
    plt.title('Monthy spend')
    plt.bar(x,y)
    plt.ylabel('Expense amount (A$)')
    plt.tight_layout()
    graph = get_graph()
    return graph
