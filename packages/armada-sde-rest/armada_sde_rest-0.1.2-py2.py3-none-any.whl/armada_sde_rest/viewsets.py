from rest_framework import viewsets


class SDEViewSet(viewsets.ReadOnlyModelViewSet):
    list_serializer = None
    details_serializer = None

    def get_serializer(self, *args, many=False, **kwargs):
        if many:
            serializer_class = self.list_serializer
        else:
            serializer_class = self.details_serializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, many=many, **kwargs)
