from palantiri.BasePlotHandlers import PlotHandler

import numpy as np

from sklearn.metrics import confusion_matrix, roc_curve, auc


import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.offline import iplot


class ClassifierPlotHandler(PlotHandler):
    """ Handles all the plots related of the chosen classifier. """

    def __init__(self, data_set_df, trained_classifier, **params):
        self._data_set_df = data_set_df
        self._trained_classifier = trained_classifier

        # Score of the predicted target store.
        self._predicted_target_score = self._trained_classifier.predict_proba(self._data_set_df.drop('y', axis=1))

        # The target value.
        self._target = self._data_set_df['y']

        self._n_classes = data_set_df['y'].nunique()

        self._confusion_matrix = None

        self.prediction_figure = None
        self.roc_figure = None
        self.confusion_matrix_figure = None

        super(ClassifierPlotHandler, self).__init__(**params)

    @property
    def trained_classifier(self):
        return self._trained_classifier

    @property
    def data_set_df(self):
        return self._data_set_df

    @data_set_df.setter
    def data_set_df(self, df):
        self._data_set_df = df

    @property
    def predicted_target_score(self):
        return self._predicted_target_score

    @property
    def target(self):
        return self._target

    @property
    def confusion_matrix(self):
        return self._confusion_matrix

    @property
    def n_classes(self):
        return self._n_classes

    def plot_confusion_matrix(self,
                              class_names=None,
                              normalize=False,
                              colorscale='Viridis'):

        prediction = self.trained_classifier.predict(self.data_set_df.drop('y', axis=1))

        self._confusion_matrix = confusion_matrix(self._target, prediction)

        if not class_names:
            class_names = ['Class {0}'.format(i) for i in range(self.n_classes)]

        if normalize:
            cm = self._confusion_matrix.astype('float') / self._confusion_matrix.sum(axis=1)[:, np.newaxis]
        else:
            cm = self._confusion_matrix

        cm = np.flipud(cm)
        x = class_names
        y = list(reversed(class_names))

        self.confusion_matrix_figure = ff.create_annotated_heatmap(z=cm, x=x, y=y, colorscale=colorscale)
        self.confusion_matrix_figure['layout']['yaxis'].update({'title': 'True Value'})
        self.confusion_matrix_figure['layout']['xaxis'].update({'title': 'Predicted Value'})

        iplot(self.confusion_matrix_figure)

    def plot_roc(self, title='ROC Curve'):
        data = list()

        if self.n_classes < 3:
            # False positive rate and true positive rate - computed from roc_curve()
            fpr, tpr, _ = roc_curve(self.target, self.predicted_target_score[:, 1])

            # Area under curve.
            roc_auc = auc(fpr, tpr)

            # Updating the data list.
            data.append(go.Scatter(x=fpr,
                                   y=tpr,
                                   mode='lines',
                                   line=dict(color='darkorange'),
                                   name='ROC curve (area = %0.2f)' % roc_auc))
        else:

            # False Positive, True Positive rates and Area Under Curve values for each class.
            fpr = dict()
            tpr = dict()
            roc_auc = dict()

            for i in range(self.n_classes):
                fpr[i], tpr[i], _ = roc_curve((self.target == i).astype(float), self.predicted_target_score[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])

                data.append(go.Scatter(x=fpr[i],
                                       y=tpr[i],
                                       mode='lines',
                                       name='ROC curve of class {0} (area = {1:0.2f})'''.format(i, roc_auc[i])))

        # Diagonal
        data.append(go.Scatter(x=[0, 1], y=[0, 1],
                               mode='lines',
                               line=dict(color='navy', dash='dash'),
                               showlegend=False))

        layout = go.Layout(title=title,
                           xaxis=dict(title='False Positive Rate'),
                           yaxis=dict(title='True Positive Rate'))

        self.roc_figure = go.Figure(data=data, layout=layout)

        iplot(self.roc_figure)


class TwoDimensionalClassifierPlotHandler(ClassifierPlotHandler):
    """ Handles all the plots related of the chosen classifier on 2D. """

    def __init__(self, data_set_df, trained_classifier, step_size=0.01, **params):
        self.step_size = step_size

        assert {'x1', 'x2', 'y'}.issubset(data_set_df.columns), \
            'Missing columns in dataset, columns must include x1, x2, y'

        super(TwoDimensionalClassifierPlotHandler, self).__init__(data_set_df, trained_classifier, **params)

    def plot_prediction(self, title='Classifier Prediction'):
        data = list()

        x_min, x_max = self.data_set_df['x1'].min() - 1, self.data_set_df['x1'].max() + 1
        y_min, y_max = self.data_set_df['x2'].min() - 1, self.data_set_df['x2'].max() + 1

        x = np.arange(x_min, x_max, self.step_size)
        y = np.arange(y_min, y_max, self.step_size)
        x_mesh, y_mesh = np.meshgrid(x, y)

        z = self.trained_classifier.predict(np.column_stack((x_mesh.ravel(), y_mesh.ravel())))

        z = z.reshape(x_mesh.shape)

        data.append(go.Contour(x=x, y=y, z=z,
                               showscale=False,
                               colorscale='Viridis'))

        data.append(go.Scatter(x=self.data_set_df['x1'],
                               y=self.data_set_df['x2'],
                               mode='markers',
                               marker=dict(color=self.data_set_df['y'],
                                           showscale=False,
                                           colorscale='Reds',
                                           line=dict(color='black', width=1))))

        layout = go.Layout(title=title)

        self.prediction_figure = go.Figure(data=data, layout=layout)

        iplot(self.prediction_figure)


class ThreeDimensionalClassifierPlotHandler(ClassifierPlotHandler):
    """ Handles all the plots related of the chosen classifier on 3D. """

    def __init__(self, data_set_df, trained_classifier, **params):
        assert {'x1', 'x2', 'x3', 'y'}.issubset(data_set_df.columns),\
            'Missing columns in dataset, columns must include x1, x2, x3, y'

        super(ThreeDimensionalClassifierPlotHandler, self).__init__(data_set_df, trained_classifier, **params)

    def plot_prediction(self, title='Classifier Prediction'):

        labels = self.trained_classifier.predict(self.data_set_df[['x1', 'x2', 'x3']])

        data = list()

        data.append(go.Scatter3d(x=self.data_set_df['x1'],
                                 y=self.data_set_df['x2'],
                                 z=self.data_set_df['x3'],
                                 showlegend=False,
                                 mode='markers',
                                 marker=dict(
                                     color=labels.astype(np.float),
                                     line=dict(color='black', width=1))))

        layout = go.Layout(title=title)

        self.prediction_figure = go.Figure(data=data, layout=layout)
        iplot(self.prediction_figure)
