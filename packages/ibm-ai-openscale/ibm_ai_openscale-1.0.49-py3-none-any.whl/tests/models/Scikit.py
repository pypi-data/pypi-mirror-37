import os


def create_scikit_learn_model_data(model_name='digits'):
    from sklearn import datasets
    from sklearn.pipeline import Pipeline
    from sklearn import preprocessing
    from sklearn import decomposition
    from sklearn import svm

    global model_data
    global model

    if model_name == 'digits':
        model_data = datasets.load_digits()
        scaler = preprocessing.StandardScaler()
        clf = svm.SVC(kernel='rbf')
        pipeline = Pipeline([('scaler', scaler), ('svc', clf)])
        model = pipeline.fit(model_data.data, model_data.target)
        predicted = model.predict(model_data.data[1: 10])
    if model_name == 'iris':
        model_data = datasets.load_iris()
        pca = decomposition.PCA()
        clf = svm.SVC(kernel='rbf')
        pipeline = Pipeline([('pca', pca), ('svc', clf)])
        model = pipeline.fit(model_data.data, model_data.target)
        predicted = model.predict(model_data.data[1: 10])

    return {
        'model': model,
        'pipeline': pipeline,
        'training_data': model_data.data,
        'training_target': model_data.target,
        'prediction': predicted
    }


def get_digits_model_data():
    return _get_model_data('digits')


def get_iris_model_data():
    return _get_model_data('iris')


def _get_model_data(model_name='digits'):
    from sklearn import datasets
    from sklearn.pipeline import Pipeline
    from sklearn import preprocessing
    from sklearn import decomposition
    from sklearn import svm

    global model_data
    global model

    if model_name == 'digits':
        model_data = datasets.load_digits()
        scaler = preprocessing.StandardScaler()
        clf = svm.SVC(kernel='rbf')
        pipeline = Pipeline([('scaler', scaler), ('svc', clf)])
        model = pipeline.fit(model_data.data, model_data.target)
        predicted = model.predict(model_data.data[1: 10])
    if model_name == 'iris':
        model_data = datasets.load_iris()
        pca = decomposition.PCA()
        clf = svm.SVC(kernel='rbf')
        pipeline = Pipeline([('pca', pca), ('svc', clf)])
        model = pipeline.fit(model_data.data, model_data.target)
        predicted = model.predict(model_data.data[1: 10])

    return {
        'model': model,
        'pipeline': pipeline,
        'training_data': model_data.data,
        'training_target': model_data.target,
        'prediction': predicted
    }


def get_digits_scoring_payload():
    return {"values": [
        [
            0.0,
            0.0,
            5.0,
            16.0,
            16.0,
            3.0,
            0.0,
            0.0,
            0.0,
            0.0,
            9.0,
            16.0,
            7.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            12.0,
            15.0,
            2.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            15.0,
            16.0,
            15.0,
            4.0,
            0.0,
            0.0,
            0.0,
            0.0,
            9.0,
            13.0,
            16.0,
            9.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            14.0,
            12.0,
            0.0,
            0.0,
            0.0,
            0.0,
            5.0,
            12.0,
            16.0,
            8.0,
            0.0,
            0.0,
            0.0,
            0.0,
            3.0,
            15.0,
            15.0,
            1.0,
            0.0,
            0.0
        ],
        [
            0.0,
            0.0,
            6.0,
            16.0,
            12.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            5.0,
            16.0,
            13.0,
            10.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            5.0,
            5.0,
            15.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            8.0,
            15.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            13.0,
            13.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            6.0,
            16.0,
            9.0,
            4.0,
            1.0,
            0.0,
            0.0,
            3.0,
            16.0,
            16.0,
            16.0,
            16.0,
            10.0,
            0.0,
            0.0,
            5.0,
            16.0,
            11.0,
            9.0,
            6.0,
            2.0
        ]
    ]
    }
