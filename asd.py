#! /usr/bin/env python
# -*- coding: utf-8 -*-
import redis
red = redis.Redis(host='127.0.0.1', password='123456', port=6379, db=0)
red.sadd("key", "ssss")
value = red.spop("key")
print(value)