# -*- coding: utf-8 -*-
from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView


class AddForm(DefaultAddForm):

    def updateWidgets(self):
        """
        Set length
        """
        super(AddForm, self).updateWidgets()
        default_size = 50
        self.widgets['IDublinCore.title'].size = default_size
        self.widgets['location'].size = default_size
        self.widgets['phone'].size = default_size
        self.widgets['fax'].size = default_size
        self.widgets['email'].size = default_size
        self.widgets['pec'].size = default_size
        self.widgets['executive'].size = default_size
        self.widgets['duties'].size = default_size


class EditForm(DefaultEditForm):
    def updateWidgets(self):
        """
        Set length
        """
        super(EditForm, self).updateWidgets()
        default_size = 50
        self.widgets['IDublinCore.title'].size = default_size
        self.widgets['location'].size = default_size
        self.widgets['phone'].size = default_size
        self.widgets['fax'].size = default_size
        self.widgets['email'].size = default_size
        self.widgets['pec'].size = default_size
        self.widgets['executive'].size = default_size
        self.widgets['duties'].size = default_size


class AddView(DefaultAddView):
    form = AddForm


class EditView(DefaultEditView):
    form = EditForm
