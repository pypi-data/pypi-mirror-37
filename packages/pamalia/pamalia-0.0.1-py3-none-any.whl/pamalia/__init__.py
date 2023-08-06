import numpy as np

from sklearn.pipeline import Pipeline, _name_estimators, _fit_transform_one
from sklearn.externals import six
from sklearn.base import clone, is_classifier, is_regressor
from sklearn.model_selection import (
    BaseCrossValidator,
    KFold,
    cross_val_predict,
    cross_val_score,
)
from sklearn.utils.metaestimators import if_delegate_has_method


__all__ = ["StackingPipeline", "make_stacking_pipeline"]


def _is_transformer(t):
    return (hasattr(t, "fit") or hasattr(t, "fit_transform")) and hasattr(
        t, "transform"
    )


# TODO: test proba vs log_proba


class StackingPipeline(Pipeline):
    """Pipeline of transforms and stacked estimators.

    Sequentially apply a list of transforms and estimators.
    The estimators are fitted iteratively on out-of-sample
    predictions made by previous methods.

    The purpose of the pipeline is to assemble several steps that can be
    cross-validated together while setting different parameters.
    For this, it enables setting parameters of the various steps using their
    names and the parameter name separated by a '__', as in the example below.
    A step's estimator may be replaced entirely by setting the parameter
    with its name to another estimator, or a transformer removed by setting
    to None.

    Read more in the :ref:`User Guide <pipeline>`.

    Parameters
    ----------
    steps : list
        List of (name, transform) tuples (implementing fit/transform) that are
        chained, in the order in which they are chained, with the last object
        an estimator.

    memory : None, str or object with the joblib.Memory interface, optional
        Used to cache the fitted transformers of the pipeline. By default,
        no caching is performed. If a string is given, it is the path to
        the caching directory. Enabling caching triggers a clone of
        the transformers before fitting. Therefore, the transformer
        instance given to the pipeline cannot be inspected
        directly. Use the attribute ``named_steps`` or ``steps`` to
        inspect estimators within the pipeline. Caching the
        transformers is advantageous when fitting is time consuming.

    Attributes
    ----------
    named_steps : bunch object, a dictionary with attribute access
        Read-only attribute to access any step parameter by user given name.
        Keys are step names and values are steps parameters.

    See also
    --------
    sklearn.pipeline.make_pipeline : convenience function for simplified
        pipeline construction.

    Examples
    --------
    >>> from sklearn import svm
    >>> from sklearn.datasets import samples_generator
    >>> from sklearn.feature_selection import SelectKBest
    >>> from sklearn.feature_selection import f_regression
    >>> from sklearn.pipeline import Pipeline
    >>> # generate some data to play with
    >>> X, y = samples_generator.make_classification(
    ...     n_informative=5, n_redundant=0, random_state=42)
    >>> # ANOVA SVM-C
    >>> anova_filter = SelectKBest(f_regression, k=5)
    >>> clf = svm.SVC(kernel='linear')
    >>> anova_svm = Pipeline([('anova', anova_filter), ('svc', clf)])
    >>> # You can set the parameters using the names issued
    >>> # For instance, fit using a k of 10 in the SelectKBest
    >>> # and a parameter 'C' of the svm
    >>> anova_svm.set_params(anova__k=10, svc__C=.1).fit(X, y)
    ...                      # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Pipeline(memory=None,
             steps=[('anova', SelectKBest(...)),
                    ('svc', SVC(...))])
    >>> prediction = anova_svm.predict(X)
    >>> anova_svm.score(X, y)                        # doctest: +ELLIPSIS
    0.83
    >>> # getting the selected features chosen by anova_filter
    >>> anova_svm.named_steps['anova'].get_support()
    ... # doctest: +NORMALIZE_WHITESPACE
    array([False, False,  True,  True, False, False, True,  True, False,
           True,  False,  True,  True, False, True,  False, True, True,
           False, False])
    >>> # Another way to get selected features chosen by anova_filter
    >>> anova_svm.named_steps.anova.get_support()
    ... # doctest: +NORMALIZE_WHITESPACE
    array([False, False,  True,  True, False, False, True,  True, False,
           True,  False,  True,  True, False, True,  False, True, True,
           False, False])
    """

    # BaseEstimator interface

    def __init__(self, steps, cv=5):
        self.steps = steps
        if cv is None:
            cv = 5
        if not isinstance(cv, BaseCrossValidator):
            cv = KFold(n_splits=cv, shuffle=True)
        self.cv = cv
        self._validate_steps()

    def get_params(self, deep=True):
        """Get parameters for this estimator.

        Parameters
        ----------
        deep : boolean, optional
            If True, will return the parameters for this estimator and
            contained subobjects that are estimators.

        Returns
        -------
        params : mapping of string to any
            Parameter names mapped to their values.
        """
        return {"cv": self.cv, **self._get_params("steps", deep=deep)}

    def set_params(self, **kwargs):
        """Set the parameters of this estimator.

        Valid parameter keys can be listed with ``get_params()``.

        Returns
        -------
        self
        """
        if "cv" in kwargs:
            self.cv = kwargs.pop("cv")
        self._set_params("steps", **kwargs)
        return self

    def _validate_steps(self):
        names, estimators = zip(*self.steps)

        # validate names
        self._validate_names(names)

        # validate estimators
        estimator = estimators[-1]

        for t in estimators[:-1]:
            if t is None:
                continue
            if (
                not (hasattr(t, "fit") or hasattr(t, "fit_transform"))
                or not hasattr(t, "transform")
                and not hasattr(t, "predict")
            ):
                raise TypeError(
                    "All intermediate steps should be "
                    "transformers or estimators and implement "
                    "fit and (transform or predict)."
                    " '%s' (type %s) doesn't)" % (t, type(t))
                )

        # We allow last estimator to be None as an identity transformation
        if estimator is not None and not hasattr(estimator, "fit"):
            raise TypeError(
                "Last step of Pipeline should implement fit. "
                "'%s' (type %s) doesn't" % (estimator, type(estimator))
            )

    def _fit(self, X, y=None, **fit_params):
        self.steps = list(self.steps)
        self._validate_steps()

        fit_params_steps = dict(
            (name, {}) for name, step in self.steps if step is not None
        )
        for pname, pval in six.iteritems(fit_params):
            step, param = pname.split("__", 1)
            fit_params_steps[step][param] = pval

        Xt = X

        for step_idx, (name, model) in enumerate(self.steps[:-1]):
            if model is None:
                continue
            cloned_model = clone(model)
            if _is_transformer(model):
                Xt, fitted_model = _fit_transform_one(
                    cloned_model, Xt, y, None, **fit_params_steps[name]
                )
            else:
                if is_classifier(model):
                    nXt = cross_val_predict(
                        model,
                        Xt,
                        y,
                        fit_params=fit_params_steps[name],
                        cv=self.cv,
                        method="predict_proba",
                    )
                elif is_regressor(model):
                    nXt = cross_val_predict(
                        model,
                        Xt,
                        y,
                        fit_params=fit_params_steps[name],
                        cv=self.cv,
                        method="predict",
                    )
                else:
                    raise Exception("Unknown model: %s, %s" % (name, model))
                fitted_model = model.fit(Xt, y)
                Xt = np.hstack((Xt, nXt))
            self.steps[step_idx] = (name, fitted_model)
        if self._final_estimator is None:
            return Xt, {}
        return Xt, fit_params_steps[self.steps[-1][0]]

    def fit_cv_score(self, X, y, scoring=None, **fit_params):
        """
        Fits all but the last estimator and
        return the cross-validation score of the last estimator.
        It is much faster than doing cross-validation and can
        be used to compare the same pipeline with different
        hyperparameters.

        Returns
        -------

        A cross-validation score of the last estimator
        """
        Xt, fit_params = self._fit(X, y, **fit_params)
        if self._final_estimator is None:
            raise Exception("Final estimator must not be None")
        return cross_val_score(
            self._final_estimator, Xt, y, cv=self.cv, scoring=scoring, fit_params=fit_params
        )

    def _predict_but_last(self, X):
        # TODO: predict params
        Xt = X
        for step_idx, (name, model) in enumerate(self.steps[:-1]):
            if model is None:
                continue
            if _is_transformer(model):
                Xt = model.transform(Xt)
            else:
                if is_classifier(model):
                    nXt = model.predict_proba(Xt)
                elif is_regressor(model):
                    nXt = model.predict(Xt)
                else:
                    raise Exception("Unknown model: %s, %s" % (name, model))
                Xt = np.hstack((Xt, nXt))
        return Xt

    @if_delegate_has_method(delegate="_final_estimator")
    def predict(self, X, **predict_params):
        """Apply transforms to the data, and predict with the final estimator

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements of first step
            of the pipeline.

        **predict_params : dict of string -> object
            Parameters to the ``predict`` called at the end of all
            transformations in the pipeline. Note that while this may be
            used to return uncertainties from some models with return_std
            or return_cov, uncertainties that are generated by the
            transformations in the pipeline are not propagated to the
            final estimator.

        Returns
        -------
        y_pred : array-like
        """
        Xt = self._predict_but_last(X)
        return self._final_estimator.predict(Xt, **predict_params)

    @if_delegate_has_method(delegate="_final_estimator")
    def predict_proba(self, X):
        """Apply transforms, and predict_proba of the final estimator

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements of first step
            of the pipeline.

        Returns
        -------
        y_proba : array-like, shape = [n_samples, n_classes]
        """
        Xt = self._predict_but_last(X)
        return self._final_estimator.predict_proba(Xt)

    @if_delegate_has_method(delegate="_final_estimator")
    def decision_function(self, X):
        """Apply transforms, and decision_function of the final estimator

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements of first step
            of the pipeline.

        Returns
        -------
        y_score : array-like, shape = [n_samples, n_classes]
        """
        Xt = self._predict_but_last(X)
        return self.steps[-1][-1].decision_function(Xt)

    @if_delegate_has_method(delegate="_final_estimator")
    def predict_log_proba(self, X):
        """Apply transforms, and predict_log_proba of the final estimator

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements of first step
            of the pipeline.

        Returns
        -------
        y_score : array-like, shape = [n_samples, n_classes]
        """
        Xt = self._predict_but_last(X)
        return self.steps[-1][-1].predict_log_proba(Xt)

    @property
    def transform(self):
        """Apply transforms, and transform with the final estimator

        This also works where final estimator is ``None``: all prior
        transformations are applied.

        Parameters
        ----------
        X : iterable
            Data to transform. Must fulfill input requirements of first step
            of the pipeline.

        Returns
        -------
        Xt : array-like, shape = [n_samples, n_transformed_features]
        """
        # _final_estimator is None or has transform, otherwise attribute error
        # XXX: Handling the None case means we can't use if_delegate_has_method
        if self._final_estimator is not None:
            self._final_estimator.transform
        return self._transform

    def _transform(self, X):
        return self._final_estimator.transform(self._predict_but_last(X))

    @if_delegate_has_method(delegate="_final_estimator")
    def score(self, X, y=None, sample_weight=None):
        """Apply transforms, and score with the final estimator

        Parameters
        ----------
        X : iterable
            Data to predict on. Must fulfill input requirements of first step
            of the pipeline.

        y : iterable, default=None
            Targets used for scoring. Must fulfill label requirements for all
            steps of the pipeline.

        sample_weight : array-like, default=None
            If not None, this argument is passed as ``sample_weight`` keyword
            argument to the ``score`` method of the final estimator.

        Returns
        -------
        score : float
        """
        Xt = self._predict_but_last(X)
        score_params = {}
        if sample_weight is not None:
            score_params["sample_weight"] = sample_weight
        return self._final_estimator.score(Xt, y, **score_params)


def make_stacking_pipeline(*steps, **kwargs):
    cv = kwargs.pop("cv", None)
    if kwargs:
        raise TypeError(
            'Unknown keyword arguments: "{}"'.format(list(kwargs.keys())[0])
        )

    return StackingPipeline(_name_estimators(steps), cv=cv)
