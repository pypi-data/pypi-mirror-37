import json

class Config(object):
  def __init__(self, dict):
      vars(self).update(dict)