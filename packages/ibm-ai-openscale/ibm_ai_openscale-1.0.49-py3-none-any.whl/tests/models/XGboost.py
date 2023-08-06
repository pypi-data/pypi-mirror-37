import os


def get_model_data():
    file_path = os.path.join(os.getcwd(), 'artifacts', 'XGboost', 'xgboost_model.tar.gz')

    return {
        'path': file_path
    }


def get_scoring_payload():
    import xgboost as xgb
    import scipy

    labels = []
    row = []
    col = []
    dat = []
    i = 0
    for l in open(os.path.join(os.getcwd(), 'datasets', 'XGboost', 'agaricus.txt.test')):
        arr = l.split()
        labels.append(int(arr[0]))
        for it in arr[1:]:
            k, v = it.split(':')
            row.append(i)
            col.append(int(k))
            dat.append(float(v))
        i += 1
    csr = scipy.sparse.csr_matrix((dat, (row, col)))

    inp_matrix = xgb.DMatrix(csr)

    return {
        'values': csr.getrow(0).toarray().tolist()
    }
