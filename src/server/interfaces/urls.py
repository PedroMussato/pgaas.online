from django.urls import path
from .views import home, databases, database_create, database_management, database_delete, agent_communication

urlpatterns = [
    path('', home, name='home'),
    path('databases/', databases, name='databases'),
    path('database/create/', database_create, name='database_create'),
    path('database/<str:id>/', database_management, name='database_management'),
    path('database/delete/<str:id>/', database_delete, name='database_delete'),
    path('agent_communication/<str:id>/', agent_communication, name='agent_communication'),
]