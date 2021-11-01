from keras_radam import RAdam
from keras_bert import Tokenizer
from keras_bert import get_custom_objects
from keras_bert import load_trained_model_from_checkpoint
from keras_bert.layers import TokenEmbedding
from keras_pos_embd import PositionEmbedding
from tensorflow import keras

if __name__ == "__main__":
    print(keras.__version__)
    # with keras.utils.custom_object_scope({'TokenEmbedding': TokenEmbedding,
    #                                       'PositionEmbedding': PositionEmbedding}):
    #     model = keras.models.load_model('20_newsgroups_tf_v1.h5')


