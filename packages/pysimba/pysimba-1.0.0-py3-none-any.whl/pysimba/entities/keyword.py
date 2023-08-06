import json

from enum import IntEnum
from collections import namedtuple
from . import Entity


class MatchingOptions(IntEnum):
    EXACT_MATCH = 1
    PHRASE_MATCH = 2
    BROAD_MATCH = 4


class Keyword(Entity):
    def delete(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10554&docType=2
        """
        ad = self.owner
        try:
            return ad.delete_keywords(entity_ids=[self.entity_id])[0]
        except IndexError:
            raise  # TODO: custom error here
