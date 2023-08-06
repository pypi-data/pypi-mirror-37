from importlib import import_module
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split


def get_dataset(name: str):
    """load data from sklearn.datasets"""
    datasets = import_module('sklearn.datasets')
    load_dataset = getattr(datasets, 'load_' + name)
    dataset = load_dataset()
    return dataset


def split_data(dataset, train_size=0.8, test_size=0.2, random_state=0):
    """split data into train and test sets"""
    splits = train_test_split(
        dataset['data'], dataset['target'],
        train_size=train_size,
        test_size=test_size,
        random_state=random_state
    )
    return splits


def get_model(model):
    """get a scikit-learn model"""
    model_type, model_name = model.split('.')
    models = import_module('sklearn.' + model_type)
    model = getattr(models, model_name)
    return model()


def get_fitted(model, x_train, y_train, x_test):
    fit = model.fit(x_train, y_train)
    return fit.predict(x_test)


def residual_plot(fitted, target):
    mse = mean_squared_error(y_true=target, y_pred=fitted)
    r2 = r2_score(y_true=target, y_pred=fitted)
    sns.residplot(x=fitted, y=target, lowess=True, line_kws={'color': 'red'})
    plt.xlabel('Fitted Values')
    plt.ylabel('Residuals')
    plt.title(f'MSE = {mse:.0f} and $R^2$ = {r2:.0%}')
    plt.show()


def confusion_matrix_plot(fitted, target) -> None:
    confmat = confusion_matrix(y_true=target, y_pred=fitted)
    acc = accuracy_score(y_true=target, y_pred=fitted)
    sns.heatmap(confmat, square=True, annot=True, cbar=False)
    plt.xlabel('Predicted Value')
    plt.ylabel('True Value')
    plt.title(f'Accuracy = {acc:.0%}')
    plt.show()


def classify(dataset='digits', model='linear_model.LogisticRegression'):
    data = get_dataset(dataset)
    x_train, x_test, y_train, y_test = split_data(data)
    classification_model = get_model(model=model)
    fit = classification_model.fit(x_train, y_train)
    predictions = fit.predict(x_test)
    confusion_matrix_plot(fitted=predictions, target=y_test)


def regress(dataset='diabetes', model='linear_model.LogisticRegression'):
    data = get_dataset(dataset)
    x_train, x_test, y_train, y_test = split_data(data)
    regression_model = get_model(model=model)
    fit = regression_model.fit(x_train, y_train)
    predictions = fit.predict(x_test)
    residual_plot(fitted=predictions, target=y_test)
