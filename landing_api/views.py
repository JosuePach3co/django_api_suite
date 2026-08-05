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
