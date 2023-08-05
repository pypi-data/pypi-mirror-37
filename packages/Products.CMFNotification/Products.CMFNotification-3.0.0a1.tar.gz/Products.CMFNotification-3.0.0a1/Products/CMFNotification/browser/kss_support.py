"""A browser-view for subscriptions features.

$Id$
"""

from Products.CMFCore.utils import getToolByName

from kss.core import KSSView
from kss.core import kssaction

from Products.CMFNotification.NotificationTool import ID as TOOL_ID


class KSSActions(KSSView):
    """A class that holds all KSS actions related to the subscription
    portlet.
    """
    @kssaction
    def subscribe(self, portlet_hash, subscribe_to_parent=False, notifiers=['mail']):
        ## We provide a default value for 'subscribe_to_parent'
        ## because KSS will not pass it to the method is the checkbox
        ## is not checked.
        item = self.context.aq_inner
        if subscribe_to_parent:
            item = item.aq_parent
        ntool = getToolByName(item, TOOL_ID)
        ntool.subscribeTo(item, how=notifiers)
        self._refreshPortlet(portlet_hash)


    @kssaction
    def unsubscribe(self, portlet_hash):
        item = self.context.aq_inner
        ntool = getToolByName(item, TOOL_ID)
        ntool.unSubscribeFrom(item)
        self._refreshPortlet(portlet_hash)


    @kssaction
    def unsubscribeFromAbove(self, portlet_hash):
        item = self.context.aq_inner
        ntool = getToolByName(item, TOOL_ID)
        ntool.unSubscribeFromObjectAbove(item)
        self._refreshPortlet(portlet_hash)


    def _refreshPortlet(self, portlet_hash):
        commands = self.getCommandSet('plone')
        commands.refreshPortlet(portlet_hash)
