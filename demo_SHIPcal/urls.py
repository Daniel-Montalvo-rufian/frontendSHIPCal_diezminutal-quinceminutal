"""demo_SHIPcal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from simforms.views import new_simulation, load_city, new_fuel, update_fuel, ver_ciudades_disponibles
from simforms.views import async_locations, async_fueltab, async_co2factorunit, async_sim_fu, async_integrations
from results.views import all_results, result, result_instalation, result_production, result_finance

urlpatterns = [
    path('ver/ciudades_disponibles/', ver_ciudades_disponibles),


    path('admin/', admin.site.urls),
    path('', new_simulation, name="simulate"),
    path('new_location/', load_city, name='new_location'),
    path('new_fuel/', new_fuel, name='new_fuel'),
    path('fuel/<int:pk>', update_fuel.as_view(), name='update_units'), #Not implemented
    path('new_collector/', load_city, name='new_collector'), #Not implemented
    
    #results
    path('results/', all_results, name="all_results"),
    path('result/<int:sim_id>', result, name="results"),
    path('result/instalation/<int:sim_id>', result_instalation, name="results_instalation"),
    path('result/production/<int:sim_id>', result_production, name="results_production"),
    path('result/finance/<int:sim_id>', result_finance, name="results_financial"),
    
    #Async urls
    path('ajax/locations', async_locations, name='async_locations'),
    path('ajax/fuel_tab', async_fueltab, name='async_tab'),
    path('ajax/co2units', async_co2factorunit, name='async_co2units'),
    path('ajax/sim_fu', async_sim_fu, name='async_fu'),
    path('ajax/integration_schemas', async_integrations, name='async_integrations'),
]
