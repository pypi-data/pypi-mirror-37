# The `datacamprojects` python package

Skip the boilerplate of scikit-learn machine learning examples.

## Installation
```bash
pip install datacamprojects
```

## Usage

In a shell environment, you can run `datacamprojects`
with no arguments to perform a Logistic Regression
on the `digits` dataset.

This will produce a 10 x 10 confusion matrix
with the Accuracy Score at the top.

You can also pass arguments to datacamprojects at the command line.

For example, 
```bash
datacamprojects -dataset diabetes -model linear_model.Lasso
# Or
datacamprojects -d diabetes -m linear_model.Lasso
```
will run a linear regression with lasso regularization (L1)
on the `diabetes` dataset.

The `dataset` argument can be any of
the following built-in scikit-learn datasets:
- Regression
    - `boston`
    - `diabetes`
- Classification
    - `digits`
    - `iris`
    - `wine`
    - `breast_cancer`

The `model` argument refers to the model type and name from scikit-learn.
The first part is the submodule, e.g. 
- `linear_model`
- `naive_bayes`
- `ensemble`
- `svm`

while the second is what is actually imported, e.g.
- `LinearRegression`
- `GaussianNB`
- `RandomForestRegressor`
- `SVC`

Simplify code to a single function call per step:
```python
from sklearn.metrics import confusion_matrix, accuracy_score
import datacamprojects as dcp

dataset = dcp.get_data('digits')
x_train, x_test, y_train, y_test = dcp.split_data(dataset)

model = dcp.get_model(model_type='ensemble',
                      model_name='RandomForestClassifier')

fit = model.fit(x_train, y_train)
dcp.pickle_model(filename='digits_rf.pickle', model=fit)
predictions = fit.predict(x_test)

confmat = confusion_matrix(y_true=y_test, y_pred=predictions)
accuracy = accuracy_score(y_true=y_test, y_pred=predictions)

dcp.confusion_matrix_plot(cm=confmat,
                          acc=accuracy,
                          filename='digits_rf.png')
```

Or run a whole pipeline with one function:

```python
import datacamprojects as dcp

dcp.classification(dataset='digits',
                   model_type='ensemble',
                   model_name='RandomForestClassifier',
                   pickle_name='digits_rf.pickle',
                   plot_name='digits_rf.png')
```

For inspiration, look at the example pipeline in the
[pipeline folder](https://github.com/marskar/datacamprojects/tree/master/pipeline)
of the
[datacamprojects repo](https://github.com/marskar/datacamprojects).
