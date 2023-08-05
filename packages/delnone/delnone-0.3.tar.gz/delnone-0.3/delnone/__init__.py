import collections
import json
import sys

def delnone(i):
  if isinstance(i, dict):
    o = {key:delnone(value) for (key,value) in i.items() if value is not None}
  elif isinstance(i, list):
    o = [delnone(value) for value in i if value is not None]
  else:
    o = i
  return o
