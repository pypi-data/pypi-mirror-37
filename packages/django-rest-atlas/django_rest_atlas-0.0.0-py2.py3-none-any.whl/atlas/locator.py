"""
Add a view to a url object
"""

from django.urls import path, re_path

class AModule(object):
    def __init__(self):
        self.urlpatterns = list()

    def route(self, path_, **kwargs):
        pattern = self.urlpatterns
        def _descriptor(obj_class):
            pattern.append(
                re_path(
                    path_,
                    obj_class.as_view(),
                    **kwargs
                )
            )
            return obj_class
        return _descriptor

    def get_urlpatterns(self):
        return list(self.urlpatterns)
