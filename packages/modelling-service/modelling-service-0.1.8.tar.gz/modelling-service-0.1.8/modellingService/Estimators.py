from pyspark.ml.classification import LogisticRegression, DecisionTreeClassifier, GBTClassifier, RandomForestClassifier, \
    NaiveBayes, LinearSVC
import Utils

"""
Each estimator wrapper does the following:
- take a free form dict of hyperparams as input
- filters out invalid params using reshaper
- passes clean params to Spark estimator
"""

def logisticRegressionClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['lrc'])
    else:
        params = hyperparams
    return LogisticRegression(**params)

def decisionTreeClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['dtc'])
    else:
        params = hyperparams
    return DecisionTreeClassifier(**params)

def linearSupportVectorClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['lsvc'])
    else:
        params = hyperparams
    return LinearSVC(**params)

def gradientBoostedTreeClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['gbtc'])
    else:
        params = hyperparams
    return GBTClassifier(**params)

def randomForestClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['rfc'])
    else:
        params = hyperparams
    return RandomForestClassifier(**params)

def naiveBayesClassifier(hyperparams = {}, reshape=True):
    if (reshape):
        params = Utils.reshapeParams(hyperparams, reshapers['nbc'])
    else:
        params = hyperparams
    return NaiveBayes(**params)

estimators = dict(
    lrc=logisticRegressionClassifier,
    dtc=decisionTreeClassifier,
    lsvc=linearSupportVectorClassifier,
    gbtc=gradientBoostedTreeClassifier,
    rfc=randomForestClassifier,
    nbc=naiveBayesClassifier
)

"""
A reshaper is a map of cast functions to avoid precision errors in hyperparams
"""
reshapers = dict(
    lrc = {
        'regParam': float,
        'elasticNetParam': float,
        'threshold': float
    },
    dtc = {
        'maxDepth': int,
        'minInstancesPerNode': int,
        'maxBins': int,
        'minInfoGain': float
    },
    lsvc = {
        'regParam': float
    },
    gbtc = {
        'maxDepth': int,
        'minInstancesPerNode': int,
        'maxBins': int,
        'minInfoGain': float,
        'stepSize': float,
        'subsamplingRate': float
    },
    rfc = {
        'maxDepth': int,
        'minInstancesPerNode': int,
        'maxBins': int,
        'minInfoGain': float,
        'numTrees': int,
        'subsamplingRate': float
    },
    nbc = {
        'smoothing': float
    }
)

"""
A scorer determines how to pick the best score for each algorithm
"""
scorers = dict(
    lrc = lambda score: max(score),
    dtc = lambda score: max(score),
    lsvc = lambda score: max(score),
    gbtc = lambda score: max(score),
    rfc = lambda score: max(score),
    nbc = lambda score: max(score)
)