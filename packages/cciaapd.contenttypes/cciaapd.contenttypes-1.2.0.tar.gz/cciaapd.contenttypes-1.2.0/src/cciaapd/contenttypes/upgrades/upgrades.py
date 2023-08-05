# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.referenceablebehavior.uidcatalog import modified_handler
from cciaapd.contenttypes import logger
from plone import api
from plone.app.textfield.value import RichTextValue


def to_1010(context):
    """Performs the profile update
    """
    catalog = getToolByName(context, 'portal_catalog')

    offices_list = catalog.searchResults({'portal_type': 'Ufficio'})
    for office in offices_list:
        logger.info("Updated item %s" % office)
        modified_handler(office.getObject(), None)

    logger.info("Profile updated.")


def to_1100(context):
    """
    Convert old tuple values to new RichText values
    """
    portal_transforms = api.portal.get_tool(name='portal_transforms')
    setup_tool = api.portal.get_tool(name='portal_setup')
    setup_tool.runImportStepFromProfile(
        "profile-cciaapd.contenttypes:default",
        'tinymce_settings',
        run_dependencies=False)
    offices_list = api.content.find(portal_type='Ufficio')

    for brain in offices_list:
        office = brain.getObject()
        timetable = getattr(office, 'office_timetable', None)
        if not timetable:
            continue
        if isinstance(timetable, tuple):
            text = "\n".join(timetable)
            data = portal_transforms.convertTo(
                'text/html',
                text,
                mimetype='text/-x-web-intelligent')
            office.office_timetable = RichTextValue(data.getData())
        logger.info("Updated item %s" % brain.getPath())
    logger.info("Profile updated.")


def to_1200(context):
    'Import types registry configuration'
    logger.info('Importing types registry configuration for ' +
                'cciapd.contenttypes')

    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile('profile-cciaapd.contenttypes:default',
                                        'typeinfo', run_dependencies=False)
