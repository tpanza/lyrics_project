import constants
import json
import happybase
import os

PROD_PATH = os.environ.get('PROD')
CLUSTER_CONFIG_PATH = PROD_PATH + '/conf/cluster_conf.json'

class HBaseManager(object):

    def __init__(self):
        cluster_config = json.loads(open(CLUSTER_CONFIG_PATH).read())
        host = cluster_config['masterHost']
        port = cluster_config['hbaseThriftPort']
        self.connection = happybase.Connection(host, port)

    def create_lyrics_to_artists_if_not_exist(self):
        if not constants.LYRICS_TO_ARTISTS_TABLE in self.connection.tables():
            families = {'artists': dict()}
            self.connection.create_table(constants.LYRICS_TO_ARTISTS_TABLE, families)
        return self.connection.table(constants.LYRICS_TO_ARTISTS_TABLE)

    def create_artists_to_word_count_table_if_not_exist(self):
        if not constants.ARTISTS_WORDS_COUNT_TABLE in self.connection.tables():
            families = {
                'words': dict(),
                'top_10_words': dict(),
                'top_10_nontrival_words': dict()
            }
            self.connection.create_table(constants.ARTISTS_WORDS_COUNT_TABLE, families)
        return self.connection.table(constants.ARTISTS_WORDS_COUNT_TABLE)

    def create_artists_to_word_tfidf_table_if_not_exist(self):
        if not constants.ARTISTS_WORDS_TFIDF_TABLE in self.connection.tables():
            families = {
                'words_tf_idf': dict(),
                'top_10_words_tf_idf': dict()
            }
            self.connection.create_table(constants.ARTISTS_WORDS_TFIDF_TABLE, families)
        return self.connection.table(constants.ARTISTS_WORDS_TFIDF_TABLE)

    def create_word_count_table_if_not_exist(self):
        if not constants.WORDS_COUNT_TABLE in self.connection.tables():
            families = {
                'counts': dict(),
            }
            self.connection.create_table(constants.WORDS_COUNT_TABLE, families)
        return self.connection.table(constants.WORDS_COUNT_TABLE)

if __name__ == "__main__":
    hbase = HBaseManager()
    hbase.create_lyrics_to_artists_if_not_exist()
    hbase.create_artists_to_word_count_table_if_not_exist()
    hbase.create_artists_to_word_tfidf_table_if_not_exist()
    hbase.create_word_count_table_if_not_exist()
