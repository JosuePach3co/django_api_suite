from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response({'data': active_items}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación mínima
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    """
    Vista para manejar operaciones sobre un recurso específico (PUT, PATCH, DELETE).
    """

    def put(self, request, item_id):
        # 1. Buscar el elemento por su id (y que esté activo)
        item = next((item for item in data_list if item['id'] == item_id and item.get('is_active', False)), None)
        
        if not item:
            return Response({'error': 'Elemento no encontrado o inactivo.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        if 'id' not in data or 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos (id, name, email) para el reemplazo total.'}, status=status.HTTP_400_BAD_REQUEST)

        if data['id'] != item_id:
            return Response({'error': 'El identificador del cuerpo no coincide con la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        item['name'] = data['name']
        item['email'] = data['email']

        return Response({'message': 'Elemento reemplazado exitosamente.', 'data': item}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        # 1. Buscar el elemento
        item = next((item for item in data_list if item['id'] == item_id and item.get('is_active', False)), None)
        
        if not item:
            return Response({'error': 'Elemento no encontrado o inactivo.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        
        # 2. Actualización parcial (solo si el campo viene en el request)
        if 'name' in data:
            item['name'] = data['name']
        if 'email' in data:
            item['email'] = data['email']

        return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        # 1. Buscar el elemento
        item = next((item for item in data_list if item['id'] == item_id and item.get('is_active', False)), None)
        
        if not item:
            return Response({'error': 'Elemento no encontrado o ya estaba inactivo.'}, status=status.HTTP_404_NOT_FOUND)

        # 2. Eliminación lógica
        item['is_active'] = False
        
        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)