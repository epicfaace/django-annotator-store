'''
An implementation of the
`Annotation store API <http://docs.annotatorjs.org/en/v1.2.x/storage.html.>`_
for `Annotator.js <http://annotatorjs.org/>`_.
'''

default_app_config = 'annotator_store.apps.AnnotatorStoreConfig'

__version_info__ = (0, 6, 0, None)

# Dot-connect all but the last. Last is dash-connected if not None.
__version__ = '.'.join([str(i) for i in __version_info__[:-1]])
if __version_info__[-1] is not None:
    __version__ += ('-%s' % (__version_info__[-1],))
