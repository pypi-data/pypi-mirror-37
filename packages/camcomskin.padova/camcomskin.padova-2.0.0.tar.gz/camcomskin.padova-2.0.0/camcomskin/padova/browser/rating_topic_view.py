# -*- coding: utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.discussion.interfaces import IConversation
from Products.Five import BrowserView

import json


class View(BrowserView):

    def get_average_rating(self, item):
        try:
            avg_view = api.content.get_view(
                name='get_avg_rating',
                context=item,
                request=self.request
            )
            star_size_view = api.content.get_view(
                name='get_star_size',
                context=item,
                request=self.request
            )
        except InvalidParameterError:
            return ''
        avg_data = json.loads(avg_view())
        star_size = json.loads(star_size_view())
        return json.dumps({
            'rating': avg_data.get('avg_rating'),
            'max_rating': star_size.get('max_rating'),
        })

    def get_comments(self, item):
        try:
            conversation = IConversation(item)
        except Exception:
            return 0

        return conversation.total_comments
