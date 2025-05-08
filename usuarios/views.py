from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ver y editar usuarios.

    Este ViewSet proporciona automáticamente las acciones `list`, `create`, `retrieve`,
    `update` y `destroy`.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'correo']

    @action(detail=False, methods=['get'])
    def buscar_por_nombre(self, request):
        """
        Endpoint personalizado para buscar usuarios por nombre.
        """
        nombre = request.query_params.get('nombre', '')
        if nombre:
            usuarios = Usuario.objects.filter(nombre__icontains=nombre)
            page = self.paginate_queryset(usuarios)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(usuarios, many=True)
            return Response(serializer.data)
        return Response({"error": "Debe proporcionar un parámetro 'nombre'"}, status=400)