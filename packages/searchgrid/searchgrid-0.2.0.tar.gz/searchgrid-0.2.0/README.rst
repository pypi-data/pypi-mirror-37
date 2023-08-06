searchgrid documentation
============================

Helps building parameter grids for `scikit-learn grid search
<scikit-learn:grid_search>`.

|version| |licence| |py-versions|

|issues| |build| |docs| |coverage|

Specifying a parameter grid for `sklearn.model_selection.GridSearchCV <GridSearchCV>` in
Scikit-Learn can be annoying, particularly when:

-  you change your code to wrap some estimator in, say, a ``Pipeline``
   and then need to prefix all the parameters in the grid using lots of
   ``__``\ s
-  you are searching over multiple grids (i.e. your ``param_grid`` is a
   list) and you want to make a change to all of those grids

searchgrid allows you to define (and change) the grid together with the
esimator, reducing effort and sometimes code.
It stores the parameters you want to search on each particular estimator
object. This makes it much more straightforward to
specify complex parameter grids, and means you don't need to update your
grid when you change the structure of your composite estimator.

It provides two main functions:

-  `searchgrid.set_grid` is used to specify the parameter values to be
   searched for an estimator or GP kernel.
-  `searchgrid.make_grid_search` is used to construct the
   ``GridSearchCV`` object using the parameter space the estimator is annotated
   with.

Other utilities for constructing search spaces include:

- `searchgrid.build_param_grid`
- `searchgrid.make_pipeline`
- `searchgrid.make_union`

Quick Start
...........

If scikit-learn is installed, then, in a terminal::

    pip install searchgrid

and use in Python::

    from search_grid import set_grid, make_grid_search
    estimator = set_grid(MyEstimator(), param=[value1, value2, value3])
    search = make_grid_search(estimator, cv=..., scoring=...)
    search.fit(X, y)

Or search for the best among multiple distinct estimators/pipelines::

    search = make_grid_search([estimator1, estimator2], cv=..., scoring=...)
    search.fit(X, y)

Motivating examples
...................

Let's look over some of the messy change cases. We'll get some imports out of
the way.::

    >>> from sklearn.pipeline import Pipeline
    >>> from sklearn.linear_model import LogisticRegression
    >>> from sklearn.feature_selection import SelectKBest
    >>> from sklearn.decomposition import PCA
    >>> from searchgrid import set_grid, make_grid_search
    >>> from sklearn.model_selection import GridSearchCV

Wrapping an estimator in a pipeline.
    You had code which searched over parameters for a classifier.
    Now you want to search for that classifier in a Pipeline.
    With plain old scikit-learn, you have to insert ``__``\ s and change::

        >>> gs = GridSearchCV(LogisticRegression(), {'C': [.1, 1, 10]})

    to::

        >>> gs = GridSearchCV(Pipeline([('reduce', SelectKBest()),
        ...                             ('clf', LogisticRegression())]),
        ...                   {'clf__C': [.1, 1, 10]})

    With searchgrid we only have to wrap our classifier in a Pipeline, and
    do not have to change the parameter grid, adding the ``clf__`` prefix. From::

        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> gs = make_grid_search(lr)

    to::

        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> gs = make_grid_search(Pipeline([('reduce', SelectKBest()),
        ...                                 ('clf', lr)]))


You want to change the estimator being searched in a pipeline.
    With scikit-learn, to use PCA instead of SelectKBest, you change::

        >>> pipe = Pipeline([('reduce', SelectKBest()),
        ...                  ('clf', LogisticRegression())])
        >>> gs = GridSearchCV(pipe,
        ...                   {'reduce__k': [5, 10, 20],
        ...                    'clf__C': [.1, 1, 10]})

    to::

        >>> pipe = Pipeline([('reduce', PCA()),
        ...                  ('clf', LogisticRegression())])
        >>> gs = GridSearchCV(pipe,
        ...                   {'reduce__n_components': [5, 10, 20],
        ...                    'clf__C': [.1, 1, 10]})

    Note that ``reduce__k`` became ``reduce__n_components``.

    With searchgrid it's easier because you change the estimator and the
    parameters in the same place::

        >>> reduce = set_grid(SelectKBest(), k=[5, 10, 20])
        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> pipe = Pipeline([('reduce', reduce),
        ...                  ('clf', lr)])
        >>> gs = make_grid_search(pipe)

    becomes::

        >>> reduce = set_grid(PCA(), n_components=[5, 10, 20])
        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> pipe = Pipeline([('reduce', reduce),
        ...                  ('clf', lr)])
        >>> gs = make_grid_search(pipe)

Searching over multiple grids.
    You want to take the code from the previous example, but instead search
    over feature selection and PCA reduction in the same search.

    Without searchgrid::

        >>> pipe = Pipeline([('reduce', None),
        ...                  ('clf', LogisticRegression())])
        >>> gs = GridSearchCV(pipe, [{'reduce': [SelectKBest()],
        ...                           'reduce__k': [5, 10, 20],
        ...                           'clf__C': [.1, 1, 10]},
        ...                          {'reduce': [PCA()],
        ...                           'reduce__n_components': [5, 10, 20],
        ...                           'clf__C': [.1, 1, 10]}])

    With searchgrid::

        >>> kbest = set_grid(SelectKBest(), k=[5, 10, 20])
        >>> pca = set_grid(PCA(), n_components=[5, 10, 20])
        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> pipe = set_grid(Pipeline([('reduce', None),
        ...                           ('clf', lr)]),
        ...                 reduce=[kbest, pca])
        >>> gs = make_grid_search(pipe)

    And since you no longer care about step names, use
    `searchgrid.make_pipeline` to express alternative steps even more simply::

        >>> from searchgrid import make_pipeline
        >>> kbest = set_grid(SelectKBest(), k=[5, 10, 20])
        >>> pca = set_grid(PCA(), n_components=[5, 10, 20])
        >>> lr = set_grid(LogisticRegression(), C=[.1, 1, 10])
        >>> pipe = make_pipeline([kbest, pca], lr)
        >>> gs = make_grid_search(pipe)

.. |py-versions| image:: https://img.shields.io/pypi/pyversions/searchgrid.svg
    :alt: Python versions supported

.. |version| image:: https://badge.fury.io/py/searchgrid.svg
    :alt: Latest version on PyPi
    :target: https://badge.fury.io/py/searchgrid

.. |build| image:: https://travis-ci.org/jnothman/searchgrid.svg?branch=master
    :alt: Travis CI build status
    :scale: 100%
    :target: https://travis-ci.org/jnothman/searchgrid

.. |issues| image:: https://img.shields.io/github/issues/jnothman/searchgrid.svg
    :alt: Issue tracker
    :target: https://github.com/jnothman/searchgrid

.. |coverage| image:: https://coveralls.io/repos/github/jnothman/searchgrid/badge.svg
    :alt: Test coverage
    :target: https://coveralls.io/github/jnothman/searchgrid

.. |docs| image:: https://readthedocs.org/projects/searchgrid/badge/?version=latest
     :alt: Documentation Status
     :scale: 100%
     :target: https://searchgrid.readthedocs.io/en/latest/?badge=latest

.. |licence| image:: https://img.shields.io/badge/Licence-BSD-blue.svg
     :target: https://opensource.org/licenses/BSD-3-Clause
