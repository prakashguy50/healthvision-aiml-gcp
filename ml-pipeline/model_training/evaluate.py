import tensorflow as tf
from sklearn.metrics import classification_report
import numpy as np

def evaluate_model(model, test_data, test_labels):
    """
    Evaluate model performance and generate metrics
    """
    predictions = model.predict(test_data)
    predicted_classes = np.argmax(predictions, axis=1)
    
    print(classification_report(test_labels, predicted_classes))
    
    metrics = {
        'accuracy': tf.keras.metrics.Accuracy()(test_labels, predicted_classes).numpy(),
        'precision': tf.keras.metrics.Precision()(test_labels, predicted_classes).numpy(),
        'recall': tf.keras.metrics.Recall()(test_labels, predicted_classes).numpy()
    }
    
    return metrics