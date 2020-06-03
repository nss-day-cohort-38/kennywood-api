"""View module for handling requests about itineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from kennywoodapi.models import Attraction, ParkArea, Itinerary, Customer


class ItineraryItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for itineraries

    Arguments:
        serializers
    """

    class Meta:
        model = Itinerary
        url = serializers.HyperlinkedIdentityField(
            view_name='itinerary',
            lookup_field='id'
        )
        fields = ('id', 'url', 'starttime', 'attraction_id', 'attraction', 'image')
        depth = 1

class ItineraryItems(ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single itinerary item

        Returns:
            Response -- JSON serialized itinerary instance
        """
        try:
            itinerary_item = Itinerary.objects.get(pk=pk)
            serializer = ItineraryItemSerializer(
                itinerary_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to itinerary resource
        Returns:
            Response -- JSON serialized list of customer itineraries
        """
        customer = Customer.objects.get(user=request.auth.user)

        itineraries = Itinerary.objects.filter(customer=customer)

        serializer = ItineraryItemSerializer(
            itineraries, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, format=None):
        attraction = Attraction.objects.get(pk=request.data['attraction_id'])
        customer = Customer.objects.get(user=request.auth.user)

        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["start_time"]
        new_itinerary_item.customer = customer
        new_itinerary_item.attraction = attraction
        new_itinerary_item.image = request.data['image']

        new_itinerary_item.save()

        serializer = ItineraryItemSerializer(
            new_itinerary_item, context={'request': request})
        
        return Response(serializer.data)
        # serializer = ItineraryItemSerializer(data=request.data, context={'request': request})
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual itinerary item
        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data["start_time"]
        attraction = Attraction.objects.get(pk=request.data["attraction_id"])
        itinerary.attraction = attraction
        itinerary.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single itinerary item
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            itinerary.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
