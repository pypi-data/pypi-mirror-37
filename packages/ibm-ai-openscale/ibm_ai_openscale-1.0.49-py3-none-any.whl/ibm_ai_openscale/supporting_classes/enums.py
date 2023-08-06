class MetricTypes:
    """
    Describes possible metrics types for listing deployment_metrics.

    Contains: [QUALITY_MONITORING, PERFORMANCE_MONITORING, FAIRNESS_MONITORING]
    """
    QUALITY_MONITORING = 'quality'
    PERFORMANCE_MONITORING = 'performance'
    FAIRNESS_MONITORING = 'fairness'


class Choose:
    """
    Describes possible options of choosing result from table filtering when only one result is required.

    Contains: [FIRST, LAST, RANDOM]
    """
    FIRST = 'first'
    LAST = 'last'
    RANDOM = 'random'


class ExplainabilityModelType:
    """
    For explainability, describes possible model types.

    Contains: [CLASSIFICATION, REGRESSION]
    """
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'


class ExplainabilityModelDataType:
    """
    For explainability, describes possible model data types.

    Contains: [NUMERIC_CATEGORICAL, TEXT, IMAGE]
    """
    NUMERIC_CATEGORICAL = 'numeric_categorical'
    TEXT = 'text'
    IMAGE = 'image'