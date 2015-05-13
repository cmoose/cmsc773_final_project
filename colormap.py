#!/usr/bin/python
from __future__ import division

kl = {}
kl[0] = {}
kl[0] = {'all_verbs': 0.0350931637504, 'cog_adjs': 0.170914712832,
         'cog_advs': 0.262913067713, 'cog_nouns': 0.106046780815,
         'cog_verbs': 0.00986574455684, 'neg_adjs': 0.0731548805099}

def rgb_to_hex(rgb):
  r = rgb[0]
  g = rgb[1]
  b = rgb[2]
  return hex(r)[2:].upper() + hex(g)[2:].upper().zfill(2) + hex(b)[2:].upper().zfill(2)

def get_color(decimal):
  r = 255
  g = 255 - int(round(decimal * 255, 0))
  b = 255 - int(round(decimal * 255, 0))
  return (r,g,b)
