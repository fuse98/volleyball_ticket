from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from matches.serializers import StadiumSerializer, SeatingArrangementSerializer, MatchCreateSerializer
from users.permissions import IsStadiumAdmin


class StadiumCreateView(APIView):
    permission_classes = [IsStadiumAdmin]

    def post(self, request):
        serializer = StadiumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeatingArrangementCreateView(APIView):
    permission_classes = [IsStadiumAdmin]

    def post(self, request):
        serializer = SeatingArrangementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchCreateView(APIView):
    permission_classes = [IsStadiumAdmin]

    def post(self, request):
        serializer = MatchCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
