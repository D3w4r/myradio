import json
import os
import pickle
import hashlib
import logging

def hash_item(item):
    return hashlib.sha256(str(item).encode('utf-8')).hexdigest()


class Repository:

    def persist_and_filter_list(self, input_list: list, path):
        """ Persists news, which have been already read to the user """
        to_return = []
        if not os.path.exists(path):
            f = open(path, 'w')
            f.close()
        if os.stat(path).st_size != 0:
            logging.info('Persisted store found')
            with open(path, 'rb') as file:
                news_store: list = pickle.load(file)
            for input_item in input_list:
                if hash_item(input_item) not in news_store:
                    news_store.append(hash_item(input_item))
                    to_return.append(input_item)
                    logging.info('Appended ' + str(input_item) + ' to return list')
            with open(path, 'wb') as out:
                pickle.dump(news_store, out)
        else:
            logging.info('No persisted store found')
            to_return = input_list
            input_list = list(map(lambda item: hashlib.sha256(str(item).encode('utf-8')).hexdigest(), input_list))
            with open(path, 'wb') as file:
                pickle.dump(input_list, file)
        return to_return

    def persist_dict(self, to_repository, what):
        if not os.path.exists(to_repository):
            f = open(to_repository, 'w')
            f.close()
        if os.stat(to_repository).st_size == 0:
            with open(to_repository, 'w', encoding='utf-8') as file:
                json.dump(what, file, ensure_ascii=False)
