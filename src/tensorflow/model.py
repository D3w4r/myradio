import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer
import numpy as np

categories = [
    "ARTS & CULTURE",
    "BLACK VOICES",
    "BUSINESS & MONEY",
    "COLLEGE & EDUCATION",
    "CRIME",
    "DIVORCE",
    "ENTERTAINMENT & COMEDY",
    "ENVIRONMENT & GREEN",
    "FIFTY",
    "FOOD, DRINK & TASTE",
    "GOOD NEWS",
    "HOME & LIVING",
    "IMPACT",
    "LATINO VOICES",
    "MEDIA",
    "PARENTS & PARENTING",
    "POLITICS",
    "QUEER VOICES",
    "RELIGION",
    "SCIENCE & TECH",
    "SPORTS",
    "STYLE & BEAUTY",
    "TRAVEL",
    "WEDDINGS",
    "WEIRD NEWS",
    "WELLNESS & HEALTHY LIVING",
    "WOMEN",
    "WORLD NEWS"
]


def top_k_predictions(array, k):
    top_k_indices = np.argsort(array)[-k:]
    top_k_probabilities = []
    for i in range(k):
        top_k_probabilities.append(np.around(array[top_k_indices[i]] * 100, decimals=1))
    return np.flip(top_k_indices), np.flip(top_k_probabilities)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    trained_model = TFAutoModelForSequenceClassification.from_pretrained("roberta-base", num_labels=28)
    trained_model.load_weights('saved-weights.h5')

    texts = [
        'Who scored the maximum goals?',
        'Mars might have water and dragons!',
        'CPU is over-clocked, causing it to heating too much!',
        'I need to buy new prescriptions.',
        'This is just government propaganda.'
    ]

    tokens = tokenizer(texts, padding=True, truncation=True, return_tensors='tf')
    logits = trained_model.predict(dict(tokens), verbose=1).logits
    probability = tf.nn.softmax(logits, axis=1).numpy()
    predictions = np.argmax(probability, axis=1)

    for i in range(0, len(texts)):
        print("Index of text: " + texts[i])
        top_3, top_prob = top_k_predictions(probability[i], len(texts))
        print("Prediction 1:{} ({}%); Prediction 2:{} ({}%); Prediction 3:{} ({}%); \n".format(
            categories[top_3[0]], top_prob[0], categories[top_3[1]], top_prob[1], categories[top_3[2]], top_prob[2]))
