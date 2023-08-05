# -*- coding: utf-8 -*-
from cciaapd.contenttypes.interfaces import IScheda
from plone.app.contenttypes.indexers import _unicode_save_string_concat
from plone.app.textfield.value import IRichTextValue
from plone.indexer.decorator import indexer
from Products.CMFPlone.utils import safe_unicode
from plone import api


def SearchableText(obj):
    text = u""
    richtext = obj.body_text
    if richtext:
        if IRichTextValue.providedBy(richtext):
            transforms = api.portal.get_tool('portal_transforms')
            text = transforms.convertTo(
                'text/plain',
                safe_unicode(richtext.output).encode('utf8'),
                mimetype=richtext.mimeType,
            ).getData().strip()
    subject = u' '.join(
        [safe_unicode(s) for s in obj.Subject()]
    )

    return u" ".join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u"",
        safe_unicode(obj.description) or u"",
        safe_unicode(text),
        safe_unicode(subject),
    ))


@indexer(IScheda)
def SearchableText_scheda(obj):
    """
    re-defined SearchableText for scheda.
    Add also tiles text and title
    """
    return _unicode_save_string_concat(SearchableText(obj))
