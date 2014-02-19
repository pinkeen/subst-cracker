#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from cipher.key import Key

key = Key()
key.randomize()

key.save_to_file("random_key.txt")
