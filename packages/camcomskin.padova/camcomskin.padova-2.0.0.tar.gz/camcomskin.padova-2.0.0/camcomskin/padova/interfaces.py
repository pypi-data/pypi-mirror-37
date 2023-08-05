from collective.editablemenu.browser.interfaces import IEditableMenuSettings
from collective.editablemenu.browser.interfaces import IEditableMenuSettings
from zope.interface import Interface


class IEditableSecondaryMenuSettings(IEditableMenuSettings):
    """
    Settings for secondary menu
    """


class ISecondaryMenuControlpanelSchema(IEditableMenuSettings):
    """
    Controlpanel for secondary menu
    """


class IRatingEnabled(Interface):
    """marker interface for enable rating"""
