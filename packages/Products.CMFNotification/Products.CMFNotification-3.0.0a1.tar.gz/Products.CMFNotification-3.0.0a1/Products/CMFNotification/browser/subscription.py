"""A browser-view for subscriptions features.

$Id$
"""

from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone import MessageFactory

from Products.CMFNotification.NotificationTool import ID as TOOL_ID


MF = mf = MessageFactory('cmfnotification')

class Subscription(BrowserView):
    """A browser view for subscription features.

    It is actually only a wrapper around the main methods of the tool.
    """

    def subscribe(self, subscribe_to_parent=False, notifiers=['mail']):
        item = self.context.aq_inner
        if subscribe_to_parent:
            item = item.aq_parent
            msg = MF(u'success_subscribed_parent',
                     u'You have been subscribed to the parent folder of this item.')
        else:
            msg = MF(u'success_subscribed',
                     u'You have been subscribed to this item.')

        ntool = getToolByName(item, TOOL_ID)
        ntool.subscribeTo(item, how=notifiers)

        utool = getToolByName(item, 'plone_utils')
        utool.addPortalMessage(msg)
        self.request.RESPONSE.redirect(self.context.absolute_url() + '/view')


    def unsubscribe(self):
        item = self.context.aq_inner
        ntool = getToolByName(item, TOOL_ID)
        ntool.unSubscribeFrom(item)

        msg = MF(u'success_unsubscribed',
                 u'You have been unsubscribed from this item.')
        utool = getToolByName(item, 'plone_utils')
        utool.addPortalMessage(msg)
        self.request.RESPONSE.redirect(item.absolute_url() + '/view')


    def unsubscribeFromAbove(self):
        item = self.context.aq_inner
        ntool = getToolByName(item, TOOL_ID)
        ntool.unSubscribeFromObjectAbove(item)
        msg = mf(u'success_unsubscribed_above',
                 u'You have been unsubscribed from the first parent '\
                 u'folder above.')
        utool = getToolByName(item, 'plone_utils')
        utool.addPortalMessage(msg)
        self.request.RESPONSE.redirect(item.absolute_url() + '/view')
