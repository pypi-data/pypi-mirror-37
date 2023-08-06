"""
Constants and smart defaults for use with modelling-service
"""

"""
(min, max) range of hyperparams for building param grid in bayesian optimization
"""
bounds = dict(
    # Logistic Regression Classifier
    lrc = {
        'regParam': (0.1, 1),
        'elasticNetParam': (0.1, 1),
        'threshold': (0.4, 0.6)
    },

    # Decision Tree Classifier
    dtc = {
        'maxDepth': (1,10),
        'minInstancesPerNode': (1,10),
        'minInfoGain':(0.0,0.5),
        'maxBins':(32,64)
    },

    # Linear Support Vector Classifier
    lsvc = {
        'regParam': (0.1,1.0)
    },

    # Gradient Boosted Tree Classifier
    gbtc = {
        'maxDepth': (1,10),
        'minInstancesPerNode': (1,10),
        'minInfoGain': (0.0,0.5),
        'maxBins': (32,64),
        'stepSize': (0.1,1.0),
        'subsamplingRate': (0.5,1.0)
    },

    # Random Forest Classifier
    rfc = {
        'maxDepth': (1,10),
        'minInstancesPerNode': (1,10),
        'minInfoGain': (0.0,0.5),
        'maxBins': (32,64),
        'numTrees': (10,50),
        'subsamplingRate':(0.5,1.0)
    },

    #Naive Bayes Classifier
    nbc = {
        'smoothing': (0.1,1)
    }
)

"""
Smart default hyperparams. Generates param grid by cross product
"""
inits = dict(
    # Logistic Regression Classifier
    lrc = {
        'regParam': [0.1, 0.3],
        'elasticNetParam': [0.1, 0.3],
        'threshold': [0.4, 0.5]
    },

    #Decision Tree Classifier
    dtc = {
        'maxDepth': [1,3],
        'minInstancesPerNode': [1,3],
        'minInfoGain': [0.0,0.1],
        'maxBins': [32,40]
    },

    #Linear Support Vector Classifier
    lsvc = {
        'regParam': [0.1,0.3]
    },

    #Gradient Boosted Tree Classifier
    gbtc = {
        'maxDepth': [1,3],
        'minInstancesPerNode': [1,3],
        'minInfoGain': [0.0,0.1],
        'maxBins': [32,40],
        'stepSize': [0.1,0.5],
        'subsamplingRate': [0.5,1.0]
    },

    #Random Forest Classifier
    rfc = {
        'maxDepth': [1,3],
        'minInstancesPerNode': [1,3],
        'minInfoGain': [0.0,0.1],
        'maxBins': [32,40],
        'numTrees': [20,40],
        'subsamplingRate': [0.5,1.0]
    },

    #Naive Bayes Classifier
    nbc = {
        'smoothing': [0.5,1.0]
    }
)

"""
Dictionary containing the default hyperparams set by Spark
"""
defaults = dict(
    # Logistic Regression Classifier
    lrc = {
        'regParam': [0.0],
        'elasticNetParam': [0.0],
        'threshold': [0.5]
    },
    
    #Decision Tree Classifier
    dtc = {
        'maxDepth': [5],
        'minInstancesPerNode': [1],
        'minInfoGain': [0.0],
        'maxBins': [32]
    },

    #Linear Support Vector Classifier
    lsvc = {
        'regParam': [0.0]
    },

    #Gradient Boosted Tree Classifier
    gbtc = {
        'maxDepth': [5],
        'minInstancesPerNode': [1],
        'minInfoGain': [0.0],
        'maxBins': [32],
        'stepSize': [0.1],
        'subsamplingRate': [1.0]
    },

    #Random Forest Classifier
    rfc = {
        'maxDepth': [5],
        'minInstancesPerNode': [1],
        'minInfoGain': [0.0],
        'maxBins': [32],
        'numTrees': [20],
        'subsamplingRate': [1.0]
    },

    #Naive Bayes Classifier
    nbc = {
        'smoothing': [1.0]
    }
)