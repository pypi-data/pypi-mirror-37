# -*- coding: utf-8 -*-
from collective.tiles.collection.interfaces import ICollectionTileRenderer
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five.browser import BrowserView
from ZODB.POSException import POSKeyError
from zope.interface import implements

from camcomskin.padova import _


class HelpersView(BrowserView):
    """
    A set of helper functions for tile collection views.
    """

    def get_image_tag(self,
                      item,
                      scale='thumb',
                      direction='down',
                      css_class=''):
        try:
            scale_view = api.content.get_view(
                name='images',
                context=item,
                request=self.request,
            )
            return scale_view.scale(
                'image', scale=scale, direction=direction
                ).tag(css_class=css_class)
        except (InvalidParameterError, POSKeyError, AttributeError, KeyError):
            # The object doesn't have an image field
            return ""

    def get_bg_url(self, item, scale='thumb'):
        try:
            scale_view = api.content.get_view(
                name='images',
                context=item,
                request=self.request,
            )
            return 'background-image: url("' +\
                   str(scale_view.scale('image', scale=scale).url) + '");'
        except (InvalidParameterError, POSKeyError, AttributeError):
            # The object doesn't have an image field
            return ""

    def get_formatted_date(self, item):
        '''
        return a formatted date
        '''
        effective = item.effective
        if effective.year() == 1969:
            # not yet published
            return {}
        return {
            'weekday': u'weekday_{0}'.format(effective.aDay().lower()),
            'month': u'month_{0}'.format(effective.aMonth().lower()),
            'month_abbr': u'month_{0}_abbr'.format(effective.aMonth().lower()),
            'day': effective.day(),
            'year': effective.year()
        }

    def get_event_dates(self, event):
        """
        returns a string with date info (range, hours,...)
        """

        months = {
            '1': 'Gennaio',
            '2': 'Febbraio',
            '3': 'Marzo',
            '4': 'Aprile',
            '5': 'Maggio',
            '6': 'Giugno',
            '7': 'Luglio',
            '8': 'Agosto',
            '9': 'Settembre',
            '10': 'Ottobre',
            '11': 'Novembre',
            '12': 'Dicembre'
        }

        date_string = ""
        start_date_parts = [
            event.startDate.day(), months[str(event.startDate.month())],
            event.startDate.year()
        ]
        startDate = ' '.join([str(x) for x in start_date_parts])

        if event.startDate.Date() == event.endDate.Date():
            date_string = startDate + ", ore " +\
                event.startDate.TimeMinutes() + " - " +\
                event.endDate.TimeMinutes()

        else:
            end_date_parts = [
                event.endDate.day(), months[str(event.endDate.month())],
                event.endDate.year()
            ]
            endDate = ' '.join([str(x) for x in end_date_parts])
            date_string = "dal " + startDate + " al " + endDate

        return date_string


class SightsView(BrowserView):
    """
    Custom view that shows sights
    """
    implements(ICollectionTileRenderer)

    display_name = _("Sights layout")


class NewsHighlightView(BrowserView):
    """
    Custom view that shows an highlighted news
    """
    implements(ICollectionTileRenderer)

    display_name = _("News highlight")


class NewsTwoRowsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout news su due righe")


class PairedCollectionView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout tile affiancate")


class NewsBigPhotoView(BrowserView):
    """
    Custom view that shows a news with a big photo on the background
    """
    implements(ICollectionTileRenderer)

    display_name = _("News with big photo")


class NewsAreaTematicaView(BrowserView):
    """
    Custom view that shows news in area tematica
    """
    implements(ICollectionTileRenderer)

    display_name = _("News in area tematica")


class ServiziAreaTematicaView(BrowserView):
    """
    Custom view that shows servizi in area tematica
    """
    implements(ICollectionTileRenderer)

    display_name = _("Servizi in area tematica")


class NewsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("News layout with image")


class VideoView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Video layout")


class EventsView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Events layout")


class GalleryView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Gallery layout")


class AreeTematicheView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Link aree tematiche")


class LandingAreeTematicheView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Landing page aree tematiche")


class OnlineServicesView(BrowserView):
    implements(ICollectionTileRenderer)

    display_name = _("Layout servizi online")
