"""Event handlers for CMFNotification.

See ``events.txt`` for further details.

$Id$
"""

from Products.CMFCore.utils import getToolByName

from Products.CMFNotification.NotificationTool import ID

import transaction


def onObjectInitializedEvent(obj, event):
    """Subscriber for ``ObjectInitializeEvent``."""
    ntool = getToolByName(obj, ID, None)
    if ntool is not None:
        ntool.onItemCreation(obj)


def onObjectClonedEvent(obj, event):
    """Subscriber for ``ObjectClonedEvent``."""
    ntool = getToolByName(obj, ID, None)
    if ntool is not None:
        ntool.onItemCreation(obj)


def onObjectEditedEvent(obj, event):
    """Subscriber for ``ObjectModifiedEvent``."""
    ntool = getToolByName(obj, ID, None)
    if ntool is not None:
        ntool.onItemModification(obj)


def onItemRemoval_hook(status, *args, **kwargs):
    """ transaction hook to call item removal handler"""
    if status:
        obj = args[0]
        ntool = getToolByName(obj, ID, None)
        if ntool is not None:
            ntool.onItemRemoval(*args, **kwargs)


def onObjectRemovedEvent(obj, event):
    """Subscriber for ``ObjectRemovedEvent``."""
    # if we're on delete_confirmation, only trigger if submitted and not cancelled
    if obj.REQUEST.getURL().endswith('delete_confirmation') and \
       (obj.REQUEST.form.get('form.button.Cancel', None) == 'Cancel' or
                    not obj.REQUEST.form.get('form.submitted')):
        return
    currentTransaction = transaction.get()
    # check if we already set the hook
    if len([x for x in currentTransaction.getAfterCommitHooks() 
              if x[0] == onItemRemoval_hook and obj in x[1]]) == 0:
        # we wait for transaction completion as removal can be aborted
        currentTransaction.addAfterCommitHook(onItemRemoval_hook, args=(obj, ))


def onActionSucceededEvent(obj, event):
    """Subscriber for ``ActionSucceededEvent``."""
    ntool = getToolByName(obj, ID, None)
    if ntool is not None:
        ntool.onWorkflowTransition(obj, event.action)


def onDiscussionItemAddedEvent(obj, event):
    """Subscriber for ``ObjectAddedEvent`` on discussion items."""
    ntool = getToolByName(obj, ID, None)
    if ntool is not None:
        ntool.onDiscussionItemCreation(obj)
