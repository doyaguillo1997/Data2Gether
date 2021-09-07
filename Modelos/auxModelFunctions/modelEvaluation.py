import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

def modelEvaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    mape = mean_absolute_percentage_error(test_labels, predictions)
    accuracy = (1 - mape)*100

    print('Model Performance')
    print('Accuracy = {:0.2f}%.'.format(accuracy))

    return accuracy
