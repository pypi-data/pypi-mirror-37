"""Gaussian Mixture Model. """

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


class GaussianMixture(BayesianModel):
    """
    Custom Gaussian Mixture Model built using PyMC3.
    """

    def __init__(self):
        super(GaussianMixture, self).__init__()
        self.num_components = None

    def create_model(self):
        """
        Creates and returns the PyMC3 model.

        Note: The size of the shared variables must match the size of the
        training data. Otherwise, setting the shared variables later will raise
        an error. See http://docs.pymc.io/advanced_theano.html

        Returns
        ----------
        the PyMC3 model
        """
        model_input = theano.shared(np.zeros([self.num_training_samples,
                                              self.num_pred]))

        # model_output = theano.shared(np.zeros(self.num_training_samples))

        model_components = theano.shared(np.zeros(self.num_training_samples,
                                                  dtype='int'))

        self.shared_vars = {
            'model_input': model_input
            # ,
            # 'model_output': model_output,
            # 'model_components': model_components
        }

        model = pm.Model()

        with model:

            K = self.num_components
            D = self.num_pred

            pi = pm.Dirichlet("pi", a=np.ones(K) / K, shape=K)
            means = T.stack([pm.Uniform('cluster_center_{}'.format(k), lower=0.,
                                        upper=10., shape=D) for k in range(K)])
            Lower = T.stack([pm.LKJCholeskyCov('cluster_variance_{}'.format(k),
                                               n=D,
                                               eta=2.,
                                               sd_dist=pm.HalfNormal.dist(sd=1.)) for k in range(K)])
            Chol = T.stack([pm.expand_packed_triangular(D, Lower[k]) for k in range(K)])

            component_dists = [pm.MvNormal.dist(mu=means[k],
                                                chol=Chol[k],
                                                shape=D) for k in range(K)]

            X = pm.Mixture("X", w=pi, comp_dists=component_dists,
                           observed=model_input)

        return model

    def fit(self, X, num_components, inference_type='advi', minibatch_size=None,
            inference_args=None):
        """
        Train the Gaussian Mixture Model model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        n_truncate : numpy array, shape [n_samples, ]

        inference_type : string, specifies which inference method to call.
        Defaults to 'advi'. Currently, only 'advi' and 'nuts' are supported

        minibatch_size : number of samples to include in each minibatch for
        ADVI,
        defaults to None, so minibatch is not run by default

        inference_args : dict, arguments to be passed to the inference methods.
        Check the PyMC3 docs for permissable values. If no arguments are
        specified,
        default values will be set.
        """
        self.num_components = num_components
        self.num_training_samples, self.num_pred = X.shape

        self.inference_type = inference_type

        # if y.ndim != 1:
        #     y = np.squeeze(y)

        if not inference_args:
            inference_args = self._set_default_inference_args()

        if self.cached_model is None:
            self.cached_model = self.create_model()

        if minibatch_size:
            with self.cached_model:
                minibatches = {
                    self.shared_vars['model_input']: pm.Minibatch(X, batch_size=minibatch_size)
                    # ,
                    # self.shared_vars['model_output']: pm.Minibatch(y, batch_size=minibatch_size),
                    # self.shared_vars['model_components']: pm.Minibatch(components, batch_size=minibatch_size)
                }

                inference_args['more_replacements'] = minibatches
        else:
            self._set_shared_vars({'model_input': X})

        self._inference(inference_type, inference_args)

        return self

    def predict_proba(self, X, return_std=False):
        """
        Predicts probabilities of new data with a trained Gaussian Mixture Model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        cats : numpy array, shape [n_samples, ]

        return_std : Boolean flag of whether to return standard deviations with
        mean probabilities. Defaults to False.
        """

        if self.trace is None:
            raise PymcLearnError('Run fit on the model before predict.')

        # num_samples = X.shape[0]

        if self.cached_model is None:
            self.cached_model = self.create_model()

        self._set_shared_vars({'model_input': X})
        K = self.num_components

        with self.cached_model:
            pi = pm.Dirichlet("probability", a=np.array([1.0, 1.0, 1.0]), shape=K)
            _vars = [pi]

            ppc = pm.sample_ppc(self.trace,
                                # model=self.cached_model,
                                vars=_vars,
                                samples=2000,
                                size=len(X))

        if return_std:
            return ppc['probability'].mean(axis=0), ppc['probability'].std(axis=0)
        else:
            return ppc['probability'].mean(axis=0)

    def predict(self, X):
        """
        Predicts labels of new data with a trained model

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        cats : numpy array, shape [n_samples, ]
        """
        ppc_mean = self.predict_proba(X)

        # pred = ppc_mean > 0.5
        #
        # return pred
        return ppc_mean

    def score(self, X, y, cats):
        """
        Scores new data with a trained model.

        Parameters
        ----------
        X : numpy array, shape [n_samples, n_features]

        y : numpy array, shape [n_samples, ]

        cats : numpy array, shape [n_samples, ]
        """

        return accuracy_score(y, self.predict(X, cats))

    def save(self, file_prefix):
        params = {
            'inference_type': self.inference_type,
            # 'num_cats': self.num_cats,
            'num_pred': self.num_pred,
            'num_training_samples': self.num_training_samples
        }

        super(GaussianMixture, self).save(file_prefix, params)

    def load(self, file_prefix):
        params = super(GaussianMixture, self).load(file_prefix,
                                                        load_custom_params=True)

        self.inference_type = params['inference_type']
        # self.num_cats = params['num_cats']
        self.num_pred = params['num_pred']
        self.num_training_samples = params['num_training_samples']
