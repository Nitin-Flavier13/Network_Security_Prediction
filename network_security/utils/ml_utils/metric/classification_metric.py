import sys
from sklearn.metrics import f1_score, precision_score, recall_score
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import ClassificationMetricArtifact 

def get_classification_score(y_true,y_pred) -> ClassificationMetricArtifact:
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)

        classification_metric = ClassificationMetricArtifact(
            precision_score=model_precision_score,
            recall_score=model_recall_score,
            f1_score=model_f1_score
        )

        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys)