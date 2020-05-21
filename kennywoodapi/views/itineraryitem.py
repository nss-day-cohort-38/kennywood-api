"""View module for handling requests about itineraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
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
        fields = ('id', 'url', 'starttime', 'attraction_id', 'attraction',)
        depth = 2

class ItineraryItems(ViewSet):

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

    def create(self, request):

        attraction = Attraction.objects.get(pk=request.data["ride_id"])
        customer = Customer.objects.get(user=request.auth.user)

        new_itinerary_item = Itinerary()
        new_itinerary_item.starttime = request.data["starttime"]
        new_itinerary_item.customer = customer
        new_itinerary_item.attraction = attraction

        new_itinerary_item.save()

        serializer = ItineraryItemSerializer(
            new_itinerary_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual itinerary item
        Returns:
            Response -- Empty body with 204 status code
        """
        itinerary = Itinerary.objects.get(pk=pk)
        itinerary.starttime = request.data["starttime"]
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
