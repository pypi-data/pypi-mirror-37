from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IThemeBaseView(Interface):
    """ """

    def getColumnsClasses():
        """Returns all CSS classes based on columns presence.
        """
