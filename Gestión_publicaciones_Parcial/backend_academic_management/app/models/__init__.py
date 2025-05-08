# Importa todos los modelos generados
from .base_models import (
    Countries,
    Keywords,
    Projects,
    PublicationTypes,
    Users,
    Acquisitions,
    Authors,
    Conferences,
    Journals,
    Milestones,
    ProjectMembers,
    RefreshTokens,
    Deliverables,
    Publications,
    PublicationAuthors,
    PublicationReferences
)

# Lista todos los modelos disponibles para importación directa
__all__ = [
    'Countries',
    'Keywords',
    'Projects',
    'PublicationTypes',
    'Users',
    'Acquisitions',
    'Authors',
    'Conferences',
    'Journals',
    'Milestones',
    'ProjectMembers',
    'RefreshTokens',
    'Deliverables',
    'Publications',
    'PublicationAuthors',
    'PublicationReferences'
]

# Opcional: Función para inicializar modelos con la aplicación
def init_models(app):
    """Inicializa los modelos con la aplicación Flask"""
    # No es necesario hacer nada aquí porque db ya está inicializado en extensions.py
    # Pero puedes añadir lógica de inicialización si necesitas
    pass