"""
Multilayer perceptron
"""

# Authors: Daniel Emaasit <daniel.emaasit@gmail.com>
#
# License: BSD 3 clause

import numpy as np
import pymc3 as pm
from sklearn.metrics import accuracy_score
import theano
import theano.tensor as T


from pmlearn.exceptions import PymcLearnError
from pmlearn.base import BayesianModel

floatX = theano.config.floatX


class MLPClassifier(BayesianModel):
    """ Multilayer perceptron classification built using PyMC3.

    Fit a Multilayer perceptron classification model and estimate
    model parameters using
    MCMC algorithms or Variational Inference algorithms

    Parameters
    ----------


    Examples
    --------


    Reference
    ----------
    http://twiecki.github.io/blog/2016/06/01/bayesian-deep-learning/
    """
    def __init__(self, n_hidden=5):
        self.n_hidden = n_hidden
        self.num_training_samples = None
        self.num_pred = None
        self.total_size = None

        super(MLPClassifier, self).__init__()

    def create_model(self):
        """

        Returns
        -------

        """
        model_input = theano.shared(np.zeros([self.num_training_samples,
                                              self.num_pred]))

        model_output = theano.shared(np.zeros(self.num_training_samples))

        self.shared_vars = {
            'model_input': model_input,
            'model_output': model_output,
        }

        self.total_size = len(model_output.get_value())

        # Initialize random weights between each layer
        init_1 = np.random.randn(self.num_pred, self.n_hidden).astype(floatX)
        init_2 = np.random.randn(self.n_hidden, self.n_hidden).astype(floatX)
        init_out = np.random.randn(self.n_hidden).astype(floatX)

        model = pm.Model()

        with model:
            # Weights from input to hidden layer
            weights_in_1 = pm.Normal('w_in_1', 0, sd=1,
                                     shape=(self.num_pred, self.n_hidden),
                                     testval=init_1)

            # Weights from 1st to 2nd layer
            weights_1_2 = pm.Normal('w_1_2', 0, sd=1,
                                    shape=(self.n_hidden, self.n_hidden),
                                    testval=init_2)

            # Weights from hidden layer to output
            weights_2_out = pm.Normal('w_2_out', 0, sd=1,
                                      shape=(self.n_hidden,),
                                      testval=init_out)

            # Build neural-network using tanh activation function
            act_1 = pm.math.tanh(pm.math.dot(model_input, weights_in_1))
            act_2 = pm.math.tanh(pm.math.dot(act_1, weights_1_2))
            act_out = pm.math.sigmoid(pm.math.dot(act_2, weights_2_out))

            # Binary classification -> Bernoulli likelihood
            y = pm.Bernoulli('y',
                             act_out,
                             observed=model_output,
                             total_size=self.total_size)
        return model

    def fit(self, X, y, inference_type='advi', minibatch_size=None,
            inference_args=None):
        """ Train the Multilayer perceptron model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        y : numpy array, shape [n_samples, ]

        inference_type : string, specifies which inference method to call.
        Defaults to 'advi'. Currently, only 'advi' and 'nuts' are supported

        minibatch_size : number of samples to include in each minibatch
        for ADVI, defaults to None, so minibatch is not run by default

        inference_args : dict, arguments to be passed to the inference methods.
        Check the PyMC3 docs for permissable values. If no arguments are
        specified, default values will be set.
        """
        self.num_training_samples, self.num_pred = X.shape

        self.inference_type = inference_type

        if y.ndim != 1:
            y = np.squeeze(y)

        if not inference_args:
            inference_args = self._set_default_inference_args()

        if self.cached_model is None:
            self.cached_model = self.create_model()

        if minibatch_size:
            with self.cached_model:
                minibatches = {
                    self.shared_vars['model_input']: pm.Minibatch(
                        X, batch_size=minibatch_size),
                    self.shared_vars['model_output']: pm.Minibatch(
                        y, batch_size=minibatch_size),
                }

                inference_args['more_replacements'] = minibatches
        else:
            self._set_shared_vars({'model_input': X, 'model_output': y})

        self._inference(inference_type, inference_args)

        return self

    def predict_proba(self, X, return_std=False):
        """ Perform Prediction

        Predicts values of new data with a trained Gaussian Process
        Regression model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        return_std : Boolean
            Whether to return standard deviations with mean values.
            Defaults to False.
        """

        if self.trace is None:
            raise PymcLearnError('Run fit on the model before predict.')

        num_samples = X.shape[0]

        if self.cached_model is None:
            self.cached_model = self.create_model()

        self._set_shared_vars({'model_input': X,
                               'model_output': np.zeros(num_samples)})

        ppc = pm.sample_ppc(self.trace, model=self.cached_model, samples=2000)

        if return_std:
            return ppc['y'].mean(axis=0), ppc['y'].std(axis=0)
        else:
            return ppc['y'].mean(axis=0)

    def predict(self, X):
        """
        Predicts labels of new data with a trained model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        """
        ppc_mean = self.predict_proba(X)

        pred = ppc_mean > 0.5

        return pred

    def score(self, X, y):
        """
        Scores new data with a trained model.

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        y : numpy array, shape [n_samples, ]
        """

        return accuracy_score(y, self.predict(X))

    def save(self, file_prefix):
        params = {
            'inference_type': self.inference_type,
            'num_pred': self.num_pred,
            'num_training_samples': self.num_training_samples
        }

        super(MLPClassifier, self).save(file_prefix, params)

    def load(self, file_prefix):
        params = super(MLPClassifier, self).load(file_prefix,
                                                 load_custom_params=True)

        self.inference_type = params['inference_type']
        self.num_pred = params['num_pred']
        self.num_training_samples = params['num_training_samples']
