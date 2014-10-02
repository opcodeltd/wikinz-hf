# coding=utf-8

from __future__ import absolute_import
from os import path
from glob import glob
from app import app
from flask import g
import app.model as m

@app.before_request
def init_stash():
    g.stash = {}

__all__ = [ path.basename(f)[:-3] for f in glob(path.dirname(__file__) + '/*.py') ]
from . import *
