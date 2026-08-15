from django.utils import timezone

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
            
            # Validación de campos obligatorios
            required_fields = ['nombre', 'email', 'programa']
            missing_fields = []
            
            for field in required_fields:
                # Comprueba si el campo no existe o si es una cadena de texto vacía
                if field not in data or not str(data.get(field, '')).strip():
                    missing_fields.append(field)
            
            # Si falta algún campo, detenemos el proceso y devolvemos un error 400
            if missing_fields:
                return Response(
                    {"error": f"Faltan campos obligatorios o están vacíos: {', '.join(missing_fields)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Referencia a la colección
            ref = db.reference(f"{self.collection_name}")

            # Obtener la fecha y hora actual usando la zona horaria de settings.py
            current_time = timezone.localtime()
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
        """Reemplazo total de un registro específico (PUT)"""
        try:
            data = dict(request.data) if request.data is not None else {}
            if not data:
                return Response({"error": "No data provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Validación de campos obligatorios para el reemplazo total
            required_fields = ['nombre', 'email', 'programa']
            missing_fields = [field for field in required_fields if field not in data or not str(data.get(field, '')).strip()]
            
            if missing_fields:
                return Response(
                    {"error": f"Faltan campos requeridos para el reemplazo total: {', '.join(missing_fields)}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            ref = db.reference(f"{self.collection_name}/{pk}")
            existing_data = ref.get()
            
            # Verificamos si existe antes de actualizar
            if not existing_data:
                return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # Preservar el timestamp original para no perderlo al hacer un reemplazo total
            if 'timestamp' not in data and 'timestamp' in existing_data:
                data['timestamp'] = existing_data['timestamp']

            # set() reemplaza todo el nodo de la base de datos con la nueva data
            ref.set(data)
            return Response({"message": "Registro reemplazado exitosamente."}, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """Actualización parcial de un registro específico (PATCH)"""
        try:
            data = dict(request.data) if request.data is not None else {}
            if not data:
                return Response({"error": "No data provided para actualizar."}, status=status.HTTP_400_BAD_REQUEST)

            ref = db.reference(f"{self.collection_name}/{pk}")
            
            # Verificamos si existe antes de actualizar
            if not ref.get():
                return Response({"error": "Registro no encontrado."}, status=status.HTTP_404_NOT_FOUND)

            # update() modifica solo los campos enviados sin borrar el resto del nodo
            ref.update(data)
            return Response({"message": "Registro actualizado parcialmente exitosamente."}, status=status.HTTP_200_OK)
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