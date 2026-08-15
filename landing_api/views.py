from datetime import datetime

from firebase_admin import db
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "landing_entries"

    def get(self, request):
        try:
            # Referencia a la colección
            ref = db.reference(f"{self.collection_name}")

            # get: Obtiene todos los elementos de la colección
            data = ref.get() or {}

            # Devuelve un arreglo JSON con los datos obtenidos
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = dict(request.data) if request.data is not None else {}
            if not data:
                return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Referencia a la colección
            ref = db.reference(f"{self.collection_name}")

            # Obtener la fecha y hora actual y formatearla según especificación
            current_time = datetime.now()
            custom_format = (
                current_time.strftime("%d/%m/%Y, %I:%M:%S %p")
                .lower()
                .replace("am", "a. m.")
                .replace("pm", "p. m.")
            )

            # Añadir timestamp al objeto recibido
            data.update({"timestamp": custom_format})

            # push: Guarda el objeto en la colección
            new_resource = ref.push(data)

            # Devuelve el id del objeto guardado
            return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LandingAPIDetail(APIView):
    name = "Landing API Detail"
    collection_name = "landing_entries"

    def get(self, request, pk):
        """Obtiene un registro específico por su ID"""
        try:
            # Apuntamos directamente al nodo específico usando el ID (pk)
            ref = db.reference(f"{self.collection_name}/{pk}")
            data = ref.get()
            
            if not data:
                return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
                
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        """Actualiza un registro específico"""
        try:
            data = dict(request.data) if request.data is not None else {}
            if not data:
                return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

            ref = db.reference(f"{self.collection_name}/{pk}")
            
            # Verificamos si existe antes de actualizar
            if not ref.get():
                return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # update() modifica solo los campos enviados sin borrar el resto
            ref.update(data)
            return Response({"message": "Registro actualizado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Elimina un registro específico de Firebase"""
        try:
            ref = db.reference(f"{self.collection_name}/{pk}")
            
            if not ref.get():
                return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # delete() borra el nodo de la base de datos
            ref.delete()
            return Response({"message": "Registro eliminado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)