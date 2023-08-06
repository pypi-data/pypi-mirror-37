#!/usr/bin/env python
from setuptools import setup
setup(
  name = 'cs.queues',
  description = 'some Queue subclasses and ducktypes',
  author = 'Cameron Simpson',
  author_email = 'cs@cskk.id.au',
  version = '20181022',
  url = 'https://bitbucket.org/cameron_simpson/css/commits/all',
  classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 3', 'Development Status :: 4 - Beta', 'Intended Audience :: Developers', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'],
  install_requires = ['cs.logutils', 'cs.obj', 'cs.pfx', 'cs.py3', 'cs.resources', 'cs.seq'],
  keywords = ['python2', 'python3'],
  long_description = 'Queue-like items: iterable queues and channels.\n\n## Class `Channel`\n\nA zero-storage data passage.\nUnlike a Queue(1), put() blocks waiting for the matching get().\n\n## Function `IterablePriorityQueue(capacity=0, name=None, *args, **kw)`\n\nFactory to create an iterable PriorityQueue.\n\n## Function `IterableQueue(capacity=0, name=None, *args, **kw)`\n\nFactory to create an iterable Queue.\n\n## Class `NullQueue`\n\nMRO: `cs.resources.MultiOpenMixin`, `cs.obj.O`  \nA queue-like object that discards its inputs.\nCalls to .get() raise Queue_Empty.\n\n## Class `PushQueue`\n\nMRO: `cs.resources.MultiOpenMixin`, `cs.obj.O`  \nA puttable object which looks like an iterable Queue.\n\nCalling .put(item) calls `func_push` supplied at initialisation\nto trigger a function on data arrival, whose processing is mediated\nqueued via a Later for delivery to the output queue.\n\n## Class `TimerQueue`\n\nClass to run a lot of "in the future" jobs without using a bazillion\nTimer threads.',
  long_description_content_type = 'text/markdown',
  package_dir = {'': 'lib/python'},
  py_modules = ['cs.queues'],
)
