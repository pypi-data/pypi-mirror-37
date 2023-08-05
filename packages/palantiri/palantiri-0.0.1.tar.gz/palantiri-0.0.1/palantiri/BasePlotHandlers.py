from plotly.offline import init_notebook_mode
init_notebook_mode(connected=True)


class PlotHandler(object):
    """ Handles the plots """

    def __init__(self, **params):

        for k, v in params.items():
            setattr(self, k, v)
