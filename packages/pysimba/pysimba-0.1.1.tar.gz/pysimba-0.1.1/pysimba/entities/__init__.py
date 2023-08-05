import os

from pysimba import Client
from pysimba.client.mixins import ClientCapability


class Entity(ClientCapability):
    def __init__(self, entity_id, owner=None, **kwargs):
        self.entity_id = entity_id
        self.owner = owner

        for name, value in kwargs.items():
            setattr(self, name, value)
