from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from posts.models import postModel, commentModel, tagModel
from posts.serializers import postSerializers, commentSerializer, tagsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return ["title", "postType", "parentId", "body"]


class postHandler(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = postSerializers
    filter_backends = [DjangoFilterBackend, DynamicSearchFilter]
    filterset_fields = ["id", "title", "postType", "parentId", "author", "tags", "score"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return postModel.objects.order_by("-pk")

    def post(self, request, *args, **kwargs):
        serial = postSerializers(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.validated_data, status=200)
        return Response(serial.errors, status=400)

    @staticmethod
    def put(request, id, *args, **kwargs):
        try:
            model = postModel.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response("Not Found", status=404)
        try:
            for i in request.data['tags']:
                model.tags.add(tagModel.objects.get(tag=i))
        except:
            None
        serial = postSerializers(model, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.validated_data, status=200)
        return Response(serial.errors, status=400)


class commentView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = commentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["message", "postId", "id"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return commentModel.objects.order_by("-pk")

    @staticmethod
    def put(request, id, *args, **kwargs):
        try:
            model = commentModel.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response("Not Found", status=404)
        serial = commentSerializer(model, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.validated_data, status=200)
        return Response(serial.errors, status=400)


class tagView(generics.ListCreateAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = tagsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tag", "id"]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return tagModel.objects.order_by("-pk")

    @staticmethod
    def put(request, id, *args, **kwargs):
        try:
            model = tagModel.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response("Not Found", status=404)
        serial = tagsSerializer(model, data=request.data, partial=True)
        if serial.is_valid():
            serial.save()
            return Response(serial.validated_data, status=200)
        return Response(serial.errors, status=400)
