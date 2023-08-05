from Products.Five import BrowserView


class ArchivioView(BrowserView):

    def get_class_by_type(self, item):
        """
        return a css class based on filetype
        """
        if item.portal_type == "Link":
            return "fa fa-link"
        if item.is_folderish:
            return "fa fa-folder"
        item_obj = item.getObject()
        contenttype = ""
        try:
            contenttype = item_obj.file.contentType
        except AttributeError:
            # Archetype
            contenttype = item_obj.getFile().content_type
        if not contenttype:
            return ""
        if contenttype == "application/pdf":
            return "fa fa-file-pdf-o"
        else:
            return "fa fa-file-text-o"
