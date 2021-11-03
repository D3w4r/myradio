import logging

import numpy as np
import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer

from dnn import categories


class RoBERTa:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        self.trained_model = TFAutoModelForSequenceClassification.from_pretrained("roberta-base", num_labels=28)
        self.trained_model.load_weights('saved-weights.h5')
        self.logger = logging.getLogger(__name__)

    def predict(self, texts: list):
        tokens = self.tokenizer(texts, padding=True, truncation=True, return_tensors='tf')
        logits = self.trained_model.predict(dict(tokens), verbose=1).logits
        probability = tf.nn.softmax(logits, axis=1).numpy()
        predictions = np.argmax(probability, axis=1)

        pred_dict = {}
        for i in range(0, len(texts)):
            pred_dict.update({categories[predictions[i]]: texts[i]})
            self.logger.info(f'Predicted category for idx: {i}: ' + categories[predictions[i]])
        return pred_dict


if __name__ == "__main__":
    neural_net = RoBERTa()

    text = [
        'Who scored the maximum goals?',
        'Mars might have water and dragons!',
        'CPU is over-clocked, causing it to heating too much!',
        'I need to buy new prescriptions.',
        'This is just government propaganda.'
    ]

    preds = neural_net.predict(text)

    print(preds)
