from rest_framework.metadata import SimpleMetadata

class MyCustomMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = super(MyCustomMetadata, self).determine_metadata(request, view)
        metadata['name'] = view.get_view_name()
        metadata['description'] = view.get_view_description()
        # metadata['myatt'] = 'blablabla' # add extra attribute to metadata
        return metadata 