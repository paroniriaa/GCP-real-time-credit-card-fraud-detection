
�2root"_tf_keras_model*�2{"name": "random_forest_model", "trainable": true, "expects_training_arg": true, "dtype": "float32", "batch_input_shape": null, "must_restore_from_config": false, "class_name": "RandomForestModel", "config": {"layer was saved without config": true}, "is_graph_network": false, "full_save_spec": {"class_name": "__tuple__", "items": [[{"day": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "day"]}, "age": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "age"]}, "distance": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "distance"]}, "trans_diff": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "trans_diff"]}, "avg_spend_pw": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "avg_spend_pw"]}, "avg_spend_pm": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "avg_spend_pm"]}, "trans_freq_24": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "trans_freq_24"]}, "category": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "category"]}, "amt": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "amt"]}, "state": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "state"]}, "job": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "job"]}, "unix_time": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "unix_time"]}, "city_pop": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "city_pop"]}, "merchant": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "merchant"]}}], {}]}, "save_spec": {"day": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "day"]}, "age": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "age"]}, "distance": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "distance"]}, "trans_diff": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "trans_diff"]}, "avg_spend_pw": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "avg_spend_pw"]}, "avg_spend_pm": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "avg_spend_pm"]}, "trans_freq_24": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "trans_freq_24"]}, "category": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "category"]}, "amt": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "float32", "amt"]}, "state": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "state"]}, "job": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "job"]}, "unix_time": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "unix_time"]}, "city_pop": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "int64", "city_pop"]}, "merchant": {"class_name": "TypeSpec", "type_spec": "tf.TensorSpec", "serialized": [{"class_name": "TensorShape", "items": [null]}, "string", "merchant"]}}, "keras_version": "2.8.0", "backend": "tensorflow", "model_config": {"class_name": "RandomForestModel"}, "training_config": {"loss": null, "metrics": [[{"class_name": "TruePositives", "config": {"name": "tp", "dtype": "float32", "thresholds": null}, "shared_object_id": 0}, {"class_name": "FalsePositives", "config": {"name": "fp", "dtype": "float32", "thresholds": null}, "shared_object_id": 1}, {"class_name": "TrueNegatives", "config": {"name": "tn", "dtype": "float32", "thresholds": null}, "shared_object_id": 2}, {"class_name": "FalseNegatives", "config": {"name": "fn", "dtype": "float32", "thresholds": null}, "shared_object_id": 3}, {"class_name": "BinaryAccuracy", "config": {"name": "accuracy", "dtype": "float32", "threshold": 0.5}, "shared_object_id": 4}, {"class_name": "Precision", "config": {"name": "precision", "dtype": "float32", "thresholds": null, "top_k": null, "class_id": null}, "shared_object_id": 5}, {"class_name": "Recall", "config": {"name": "recall", "dtype": "float32", "thresholds": null, "top_k": null, "class_id": null}, "shared_object_id": 6}, {"class_name": "AUC", "config": {"name": "auc", "dtype": "float32", "num_thresholds": 200, "curve": "ROC", "summation_method": "interpolation", "multi_label": false, "label_weights": null}, "shared_object_id": 7}, {"class_name": "AUC", "config": {"name": "prc", "dtype": "float32", "num_thresholds": 200, "curve": "PR", "summation_method": "interpolation", "multi_label": false, "label_weights": null}, "shared_object_id": 8}]], "weighted_metrics": null, "loss_weights": null, "optimizer_config": {"class_name": "RMSprop", "config": {"name": "RMSprop", "learning_rate": 0.001, "decay": 0.0, "rho": 0.9, "momentum": 0.0, "epsilon": 1e-07, "centered": false}}}}2
�"root.keras_api.metrics.0"_tf_keras_metric*�{"class_name": "Mean", "name": "loss", "dtype": "float32", "config": {"name": "loss", "dtype": "float32"}, "shared_object_id": 9}2
�#root.keras_api.metrics.1"_tf_keras_metric*�{"class_name": "TruePositives", "name": "tp", "dtype": "float32", "config": {"name": "tp", "dtype": "float32", "thresholds": null}, "shared_object_id": 0}2
�$root.keras_api.metrics.2"_tf_keras_metric*�{"class_name": "FalsePositives", "name": "fp", "dtype": "float32", "config": {"name": "fp", "dtype": "float32", "thresholds": null}, "shared_object_id": 1}2
�%root.keras_api.metrics.3"_tf_keras_metric*�{"class_name": "TrueNegatives", "name": "tn", "dtype": "float32", "config": {"name": "tn", "dtype": "float32", "thresholds": null}, "shared_object_id": 2}2
�&root.keras_api.metrics.4"_tf_keras_metric*�{"class_name": "FalseNegatives", "name": "fn", "dtype": "float32", "config": {"name": "fn", "dtype": "float32", "thresholds": null}, "shared_object_id": 3}2
�'root.keras_api.metrics.5"_tf_keras_metric*�{"class_name": "BinaryAccuracy", "name": "accuracy", "dtype": "float32", "config": {"name": "accuracy", "dtype": "float32", "threshold": 0.5}, "shared_object_id": 4}2
�(root.keras_api.metrics.6"_tf_keras_metric*�{"class_name": "Precision", "name": "precision", "dtype": "float32", "config": {"name": "precision", "dtype": "float32", "thresholds": null, "top_k": null, "class_id": null}, "shared_object_id": 5}2
�)root.keras_api.metrics.7"_tf_keras_metric*�{"class_name": "Recall", "name": "recall", "dtype": "float32", "config": {"name": "recall", "dtype": "float32", "thresholds": null, "top_k": null, "class_id": null}, "shared_object_id": 6}2
�*root.keras_api.metrics.8"_tf_keras_metric*�{"class_name": "AUC", "name": "auc", "dtype": "float32", "config": {"name": "auc", "dtype": "float32", "num_thresholds": 200, "curve": "ROC", "summation_method": "interpolation", "multi_label": false, "label_weights": null}, "shared_object_id": 7}2
�+root.keras_api.metrics.9"_tf_keras_metric*�{"class_name": "AUC", "name": "prc", "dtype": "float32", "config": {"name": "prc", "dtype": "float32", "num_thresholds": 200, "curve": "PR", "summation_method": "interpolation", "multi_label": false, "label_weights": null}, "shared_object_id": 8}2