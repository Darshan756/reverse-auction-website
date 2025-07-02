# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserAccountSerializer
from .models import UserAccount
from rest_framework import status
from rest_framework.views import APIView

""" @api_view(['GET', 'POST'])
def userRegister(request):
    if request.method == 'POST':
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    users = UserAccount.objects.all()
    serializer = UserAccountSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PUT'])
def getUser(request,pk):
    user = UserAccount.objects.get(pk=pk)
    if request.method == "GET":
        serializer = UserAccountSerializer(user)
        return Response(serializer.data , status=status.HTTP_200_OK)
    serializer = UserAccountSerializer(user,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


 """

class ListCreatUsers(APIView):
       
    def get(self,request):

        users = UserAccount.objects.all()
        serializer = UserAccountSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = UserAccountSerializer(data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ListUpdateUser(APIView):
    def  get_object(self,pk=None):
        try:
            return UserAccount.objects.get(pk=pk)
        except UserAccount.objects.get(pk=pk).DoesNotExist:
            raise ValueError("User Not Found") 

    def get(self,request,pk):
        user = self.get_object(pk)
        serializer = UserAccountSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        user = self.get_object(pk)
        serializer = UserAccountSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def patch(self, request,pk):
        user = self.get_object(pk)
        serializer = UserAccountSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


    
    