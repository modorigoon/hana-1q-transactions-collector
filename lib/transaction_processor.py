# -*- coding: utf-8 -*-
"""
    Transaction processor
    author: modorigoon
    since: 0.1.0
"""
import itertools
from common.logger import log


class TransactionProcessor:

    def __init__(self):
        self.counter = itertools.count()

    @staticmethod
    def parse(transaction):
        """ parsing transaction string
        :param transaction: transaction string
        :return: transaction object(seq, price)
        """
        as_list = ' '.join(str(transaction).split()).split(' ')
        return {
            'date_time_seq': as_list[2],
            'price': as_list[4]
        }

    @staticmethod
    def send(transaction_object) -> bool:
        """ forward to the message pipe cache
        :param transaction_object: transaction object
        :return: send message successful
        """
        log.info('[send] transaction: {}'.format(str(transaction_object)))
        # send to MQ or storage
        return True

    def process(self, transaction_source):
        """ transaction processing
        :param transaction_source: transaction string
        :return: transaction object
        """
        transaction = self.parse(transaction_source)
        transaction['seq'] = next(self.counter)
        send_successful = self.send(transaction)
        log.info('[process] transaction: {}, sent: {}'.format(str(transaction), str(send_successful)))
        return transaction
