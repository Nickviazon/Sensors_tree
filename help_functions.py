def indexes(itr, element, comparison='eq'):
    """
    Returns list of indexes all elements of an iterable object,
    which correspond to the comparison with the element of 'parameter'
    :param itr - the iterable object where you want to find the indexes of 'element'
    :param element - the element with which you want to compare
    :param comparison - comparison operation

    There is 6 provided comparison operations:
      'eq' - equal;
      'not_eq' - not equal;
      'grt' - strictly greater than;
      'lss' - strictly less than;
      'lss_eq' - less than or equal;
      'grt_eq' - greater than or equal.

    Example:

      a = [1, 2, 10, 23, 45]
      indexes(a, 10, 'lss') # Will return [0,1]
    """
    if comparison == 'eq':
        return [i for i, elem in enumerate(itr) if element == elem]
    elif comparison == 'not_eq':
        return [i for i, elem in enumerate(itr) if element != elem]
    elif comparison == 'grt':
        return [i for i, elem in enumerate(itr) if element < elem]
    elif comparison == 'lss':
        return [i for i, elem in enumerate(itr) if element > elem]
    elif comparison == 'grt_eq':
        return [i for i, elem in enumerate(itr) if element <= elem]
    elif comparison == 'lss_eq':
        return [i for i, elem in enumerate(itr) if element >= elem]


def draw_plot(title, x_title, y_title, file_name="plot.html", **plot_data):
    """
    Simple wrapper function for drawing graphs in Plotly

    -------IMPORTANT!!!!!!------
    plot_data has dict type with necessary param - x_axis
    -------IMPORTANT!!!!!!------

    :param title: graph title
    :param x_title: title of x axis
    :param y_title: title of y axis
    :param file_name: file name with its type
    :param plot_data: data for graph type: dict(x_axis=some_data). Default dict's param is x_axis and its IMPORTANT!!!!!
    :return:
    """

    import plotly
    import plotly.graph_objs as go

    if "x_axis" not in plot_data or not plot_data["x_axis"]:
        raise KeyError("Dictionary haven't '{0}' key or '{0}' have unexpected value".format("x_axis"))
    if "x_type" not in plot_data or not plot_data["x_type"]:
        plot_data["x_type"] = "scatter"
    if "y_type" not in plot_data or not plot_data["y_type"]:
        plot_data["y_type"] = "scatter"

    data = [go.Scatter(x=plot_data["x_axis"], y=plot_data[name], name=name)
            for name in plot_data if name not in ["x_axis", "x_type", "y_type"]
            ]

    layout = go.Layout(title=u"{}".format(title),
                       xaxis=dict(title=u"{}".format(x_title), type="{}".format(plot_data["x_type"])),
                       yaxis=dict(title=u"{}".format(y_title), type="{}".format(plot_data["y_type"])),
                       )

    plot = dict(data=data, layout=layout)
    plotly.offline.plot(plot, filename=file_name)


def frange(x, y, jump):
  import decimal
  while x < y:
    yield float(x)
    x += decimal.Decimal(jump)
