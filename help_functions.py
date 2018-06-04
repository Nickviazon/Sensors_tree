def key_init(dictionary, key, data):
    if key not in dictionary:
        dictionary[key] = data


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


def draw_plot(title, x_title, y_title, file_name="plot.html", save_image=False, **plot_data):
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

    if "x_type" not in plot_data or not plot_data["x_type"]:
        plot_data["x_type"] = "scatter"
    if "y_type" not in plot_data or not plot_data["y_type"]:
        plot_data["y_type"] = "scatter"

    for key, value in plot_data.items():
        if key not in ["x_type", "y_type"]:
            if "x_axis" not in value or not value["x_axis"]:
                raise KeyError("Dictionary haven't '{0}' key or '{0}' have unexpected value".format("x_axis"))
    data = []
    markers = ["circle-open", "square", "triangle", "x"]
    i = 0
    for name in sorted(list(plot_data), reverse=True):
        if name not in ["x_type", "y_type", "Неадаптивный", "Неадаптивный(теор.)"]:
            data.append(go.Scatter(x=plot_data[name]["x_axis"],
                                   y=plot_data[name]["value"],
                                   name=name,
                                   line={"width": 7},
                                   marker={"size": 17,
                                           "symbol": markers[i]}))
            i += 1

        elif name == "Неадаптивный":
            data.append(go.Scatter(
                x=plot_data["Неадаптивный"]["x_axis"],
                y=plot_data["Неадаптивный"]["value"],
                name="Неадаптивный",
                line={
                    "width": 7,
                    "dash": "longdash",
                },
                marker={
                    "size": 18,
                    "symbol": "cross"
                },
            ))
        elif name == "Неадаптивный(теор.)":
            data.append(go.Scatter(
                x=plot_data["Неадаптивный(теор.)"]["x_axis"],
                y=plot_data["Неадаптивный(теор.)"]["value"],
                name="Неадаптивный(теор.)",
                line={"width": 7},
            ))

    layout = go.Layout(title=u"{}".format(title),
                       titlefont=dict(
                           family='Calibri, monospace',
                           size=44
                       ),

                       font=dict(
                           family='Calibri, monospace',
                           size=38
                       ),

                       xaxis=dict(
                           title=u"{}".format(x_title),
                           titlefont=dict(
                               family='Calibri, monospace',
                               size=38
                               ),
                           type="{}".format(plot_data["x_type"]),
                           domain=[0.08, 1]
                           ),

                       yaxis=dict(
                           title=u"{}".format(y_title),
                           titlefont=dict(
                                family='Calibri, monospace',
                                size=38
                                ),
                           type="{}".format(plot_data["y_type"]),
                           domain=[0.01, 1],
                           gridcolor='#bdbdbd',
                           gridwidth=2,
                           ),

                       legend=dict(
                           borderwidth=1,
                           x=0.1495,
                           y=1,
                           xanchor='left',

                           font=dict(
                               family='Calibri, monospace',
                               size=24
                               ),
                           ),

                       )

    plot = dict(data=data, layout=layout)
    if save_image:
        plotly.offline.plot(plot, filename=file_name, image="png", image_height=1020, image_width=1980)
    else:
        plotly.offline.plot(plot, filename=file_name)
