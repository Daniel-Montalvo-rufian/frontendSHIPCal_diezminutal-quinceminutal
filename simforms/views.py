from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.conf import settings
from django.forms.models import model_to_dict
from .forms import SimulationForm, NewLocation, FuelForm, FuelUnitsForm, FuelForm2
from .models import Locations, MeteoData, Simulation, Fuels, FuelUnits
from results.models import SimResults, TemplateVars, PlotVars, ReportVars

import numpy as np
import json


import sys
import os
sys.path.append(os.path.join(settings.BASE_DIR, 'SHIPcal'))
from SHIPcal.SHIPcal import SHIPcal #noqa

from django.db.models import Sum

# Create your views here.
def ver_ciudades_disponibles(request):
    todas_las_ciudades  = Locations.objects.all()

    total_DNI = []
    for city in todas_las_ciudades:
        total_DNI += [MeteoData.objects.filter(location=city).aggregate(Sum('DNI'))]

    table_info = zip(todas_las_ciudades, total_DNI)

    return render(request, 'ciudades_disponibles.html', {'ciudades':table_info})


def new_simulation(request):
    if request.method =='POST':
        
        sim_form = SimulationForm(request.POST)
        if sim_form.is_valid():
            
            new_sim = sim_form.cleaned_data
            sim = Simulation(**new_sim)
            sim.save()

            lang_code=translation.get_language()
            if lang_code=='es':
                lang='spa'
            else:
                lang='eng'

            inputsDjango = model_to_dict(sim)
            inputsDjango.update({
                'pressure':inputsDjango['pressure']*inputsDjango['pressureUnit'], #Converts into kWh
                'demand':inputsDjango['demand']*inputsDjango['demandUnit'], #Converts into bar
                'fuelPrice':inputsDjango['fuel_price']*sim.fuel_price_unit.conversion_factor, #converts into EUR/kWh
                'co2factor':sim.fuel.co2factor*sim.fuel.co2units.conversion_factor, # [CO2tons/kWh]
                'date':sim.date,'fuel':sim.fuel.fuel,'location_aux':sim.location.location_aux,
                'hour_ini_sim':sim_form.cleaned_data['hour_ini_sim'].hour,
                'hour_fin_sim':sim_form.cleaned_data['hour_fin_sim'].hour,

            })
            inputsDjango.update({'pressureUnit':'bar','demandUnit':'kWh','fuelUnit':'kWh',})

            confReport={'lang':lang,'sender':'SHIPcal','cabecera':_('Resultados de la <br> simulación'),'mapama':0}
            modificators={'mofINV':sim.mofINV,'mofDNI':sim.mofDNI,'mofProd':sim.mofProd}
            desginDict={'num_loops':sim.num_loops,'n_coll_loop':sim.n_coll_loop,'type_integration':sim.type_integration,'almVolumen':sim.almVolumen}
            
            if inputsDjango['itercontrol']=='paso_10min' or inputsDjango['itercontrol']=='paso_15min':
                if inputsDjango['annual']=='yes':
                     if inputsDjango['itercontrol']=='paso_10min':
                        simControl={'finance_study':1,'mes_ini_sim':1,'dia_ini_sim':1,'hora_ini_sim':0,'mes_fin_sim':12,'dia_fin_sim':31,'hora_fin_sim':24, 'itercontrol':inputsDjango['itercontrol'],'ten_min_ini_sim':0, 'ten_min_fin_sim':0, 'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}
                     elif inputsDjango['itercontrol']=='paso_15min':
                        simControl={'finance_study':1,'mes_ini_sim':1,'dia_ini_sim':1,'hora_ini_sim':0,'mes_fin_sim':12,'dia_fin_sim':31,'hora_fin_sim':24, 'itercontrol':inputsDjango['itercontrol'],'fifteen_min_ini_sim':0, 'fifteen_min_fin_sim':0, 'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}
                else:
                    minute={'ten_min_ini_sim':sim_form.cleaned_data['hour_ini_sim'].minute, 'ten_min_fin_sim':sim_form.cleaned_data['hour_fin_sim'].minute,'fifteen_min_ini_sim':sim_form.cleaned_data['hour_ini_sim'].minute, 'fifteen_min_fin_sim':sim_form.cleaned_data['hour_fin_sim'].minute}
                    if inputsDjango['itercontrol']=='paso_10min':
                        if minute['ten_min_ini_sim'] in range(0,10):
                            ten_min_ini_sim=0
                        elif minute['ten_min_ini_sim'] in range(10,20):
                                ten_min_ini_sim=1
                        elif minute['ten_min_ini_sim'] in range(20,30):
                            ten_min_ini_sim=2
                        elif minute['ten_min_ini_sim'] in range(30,40):
                            ten_min_ini_sim=3
                        elif minute['ten_min_ini_sim'] in range(40,50):
                            ten_min_ini_sim=4
                        elif minute['ten_min_ini_sim'] in range(50,60):
                            ten_min_ini_sim=5
                        if minute['ten_min_fin_sim'] in range(0,10):
                            ten_min_fin_sim=0
                        elif minute['ten_min_fin_sim'] in range(10,20):
                            ten_min_fin_sim=1
                        elif minute['ten_min_fin_sim'] in range(20,30):
                            ten_min_fin_sim=2
                        elif minute['ten_min_fin_sim'] in range(30,40):
                            ten_min_fin_sim=3
                        elif minute['ten_min_fin_sim'] in range(40,50):
                            ten_min_fin_sim=4
                        elif minute['ten_min_fin_sim'] in range(50,60):
                            ten_min_fin_sim=5
                        
                        simControl={'finance_study':1,'mes_ini_sim':inputsDjango['month_ini_sim'],'dia_ini_sim':inputsDjango['day_ini_sim'],'hora_ini_sim':sim_form.cleaned_data['hour_ini_sim'].hour,'mes_fin_sim':inputsDjango['month_fin_sim'],'dia_fin_sim':inputsDjango['day_fin_sim'],'hora_fin_sim':sim_form.cleaned_data['hour_fin_sim'].hour, 'itercontrol':inputsDjango['itercontrol'],'ten_min_ini_sim':ten_min_ini_sim, 'ten_min_fin_sim':ten_min_fin_sim, 'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}     
                     
                    elif inputsDjango['itercontrol']=='paso_15min':
                    
                        if minute['fifteen_min_ini_sim'] in range(0,15):
                            fifteen_min_ini_sim=0
                        elif minute['fifteen_min_ini_sim'] in range(15,30):
                            fifteen_min_ini_sim=1
                        elif minute['fifteen_min_ini_sim'] in range(30,45):
                            fifteen_min_ini_sim=2
                        elif minute['fifteen_min_ini_sim'] in range(45,60):
                            fifteen_min_ini_sim=3
                        if minute['fifteen_min_fin_sim'] in range(0,15):
                            fifteen_min_fin_sim=0
                        elif minute['fifteen_min_fin_sim'] in range(15,30):
                            fifteen_min_fin_sim=1
                        elif minute['fifteen_min_fin_sim'] in range(30,45):
                            fifteen_min_fin_sim=2
                        elif minute['fifteen_min_fin_sim'] in range(45,60):
                            fifteen_min_fin_sim=3
                    
                        simControl={'finance_study':1,'mes_ini_sim':inputsDjango['month_ini_sim'],'dia_ini_sim':inputsDjango['day_ini_sim'],'hora_ini_sim':sim_form.cleaned_data['hour_ini_sim'].hour,'mes_fin_sim':inputsDjango['month_fin_sim'],'dia_fin_sim':inputsDjango['day_fin_sim'],'hora_fin_sim':sim_form.cleaned_data['hour_fin_sim'].hour, 'itercontrol':inputsDjango['itercontrol'],'fifteen_min_ini_sim':fifteen_min_ini_sim, 'fifteen_min_fin_sim':fifteen_min_fin_sim, 'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}    
            
            else:
                if inputsDjango['annual']=='yes':
                    simControl={'finance_study':1,'mes_ini_sim':1,'dia_ini_sim':1,'hora_ini_sim':1,'mes_fin_sim':12,'dia_fin_sim':31,'hora_fin_sim':24, 'itercontrol':inputsDjango['itercontrol'],'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}
                else:
                    simControl={'finance_study':1,'mes_ini_sim':inputsDjango['month_ini_sim'],'dia_ini_sim':inputsDjango['day_ini_sim'],'hora_ini_sim':sim_form.cleaned_data['hour_ini_sim'].hour,'mes_fin_sim':inputsDjango['month_fin_sim'],'dia_fin_sim':inputsDjango['day_fin_sim'],'hora_fin_sim':sim_form.cleaned_data['hour_fin_sim'].hour, 'itercontrol':inputsDjango['itercontrol'],'to_solartime':inputsDjango['to_solartime'], 'huso':inputsDjango['huso']}
            
            template_vars,plotVars,reportsVar,version = SHIPcal(1,inputsDjango,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],200,confReport,modificators,desginDict,simControl,sim.id)
            print('Los pasos de simulación son:',len(plotVars['step_sim']), 'demanda:',len(plotVars['Demand']))
            tv = TemplateVars(v=version)
            tv.save()
            #Converts the lists in plotVars into strings for storing in the database. Removed "[" and "]"
            #For converting back [float(item) for item in string_series.split()]
            if plotVars['steps_sim']==8759 or plotVars['steps_sim']==52560 or plotVars['steps_sim']==35040:
                plotVars.update({
                'Break_cost':str(plotVars['Break_cost'])[1:-1], 
                'Acum_FCF':str(plotVars['Acum_FCF'])[1:-1],
                'FCF':str(plotVars['FCF'])[1:-1], 
                'T_in_C_AR':str(plotVars['T_in_C_AR'])[1:-1], 
                'Demand':str(plotVars['Demand'])[1:-1], 
                'Q_prod':str(plotVars['Q_prod'])[1:-1], 
                'Q_prod_lim':str(plotVars['Q_prod_lim'])[1:-1], 
                'Q_charg':str(plotVars['Q_charg'])[1:-1], 
                'Q_discharg':str(plotVars['Q_discharg'])[1:-1], 
                'DNI':str(plotVars['DNI'])[1:-1], 
                'SOC':str(plotVars['SOC'])[1:-1], 
                'Q_useful':str(plotVars['Q_useful'])[1:-1], 
                'Q_defocus':str(plotVars['Q_defocus'])[1:-1], 
                'T_alm_K':str(plotVars['T_alm_K'])[1:-1], 
                })
                # del plotVars['Q_prod_steam']
                # del plotVars['Q_drum']
                # del plotVars['SD_min_energy']
                # del plotVars['SD_max_energy']
                # del plotVars['SD_energy']
            else:
                plotVars.update({
                'step_sim':str(plotVars['step_sim'].tolist())[1:-1], 
                'Q_prod_steam':str(plotVars['Q_prod_steam'])[1:-1],
                'Q_drum':str(plotVars['Q_drum'])[1:-1],
                'SD_energy':str(plotVars['SD_energy'])[1:-1],
                'T_in_C_AR':str(plotVars['T_in_C_AR'])[1:-1], 
                'Demand':str(plotVars['Demand'])[1:-1], 
                'Q_prod':str(plotVars['Q_prod'])[1:-1], 
                'Q_prod_lim':str(plotVars['Q_prod_lim'])[1:-1], 
                'Q_charg':str(plotVars['Q_charg'])[1:-1], 
                'Q_discharg':str(plotVars['Q_discharg'])[1:-1], 
                'DNI':str(plotVars['DNI'])[1:-1], 
                'SOC':str(plotVars['SOC'])[1:-1], 
                'Q_useful':str(plotVars['Q_useful'])[1:-1], 
                'Q_defocus':str(plotVars['Q_defocus'])[1:-1], 
                'T_alm_K':str(plotVars['T_alm_K'])[1:-1],
                'Q_prod_rec':str(plotVars['Q_prod_rec'].tolist())[1:-1],
                'flowrate_kgs':str(plotVars['flowrate_kgs'].tolist())[1:-1],
                'flowrate_rec':str(plotVars['flowrate_rec'])[1:-1],
                'flowDemand':str(plotVars['flowrate_rec'])[1:-1],
                'flowToHx':str(plotVars['flowToHx'])[1:-1],
                'flowToMix':str(plotVars['flowToMix'])[1:-1],
                'T_in_K':str(plotVars['T_in_K'])[1:-1],
                'T_toProcess_C':str(plotVars['T_toProcess_C'])[1:-1],
                'T_out_K':str(plotVars['T_out_K'])[1:-1],
                })
                
                del plotVars['Acum_FCF']
                del plotVars['FCF']
                del plotVars['Break_cost']
                
            
            
            pv = PlotVars(**plotVars)
            pv.save()

            #Converts the lists in reportsVar into strings for storing in the database. Removed "[" and "]"
            #For converting back [float(item) for item in string_series.split()]
            if plotVars['steps_sim']==8759 or plotVars['steps_sim']==52560 or plotVars['steps_sim']==35040:
                reportsVar.update({
                'fuelPrizeArrayList':str(reportsVar['fuelPrizeArrayList'])[1:-1], 
                'Acum_FCFList':str(reportsVar['Acum_FCFList'])[1:-1], 
                'Energy_savingsList':str(reportsVar['Energy_savingsList'])[1:-1], 
                'OM_cost_year':str(reportsVar['OM_cost_year'])[1:-1], 
                'anual_energy_cost':str(reportsVar['anual_energy_cost'])[1:-1], 
                'Q_prod':str(reportsVar['Q_prod'])[1:-1], 
                'Q_prod_lim':str(reportsVar['Q_prod_lim'])[1:-1], 
                'Demand':str(reportsVar['Demand'])[1:-1], 
                'Q_charg':str(reportsVar['Q_charg'])[1:-1], 
                'Q_discharg':str(reportsVar['Q_discharg'])[1:-1], 
                'Q_defocus':str(reportsVar['Q_defocus'])[1:-1], 
                'flow_rate_kgs':str(reportsVar['flow_rate_kgs'])[1:-1], 
                })

            rv = ReportVars(**reportsVar)
            rv.save()
            
            sr = SimResults(simulation=sim, version=version, templateVars=tv, plotVars=pv, reportsVar=rv)
            sr.save()

            return HttpResponseRedirect(reverse_lazy('results', kwargs={'sim_id':sim.id}))

    else:
        sim_form = SimulationForm()
        sim_form.fields['location'].disabled = True 
        sim_form.fields['fuel_price_unit'].disabled = True 
        
    return render(request,'simulation_form.html', {'form':sim_form})

def load_city(request):
    if request.method=='POST':
        sim_form = NewLocation(request.POST, request.FILES)
        if sim_form.is_valid():
            data = sim_form.cleaned_data
            new_location = Locations(pais=data['pais'], city=data['city'], lat = data['lat'], lon=data['lon'])
            new_location.save()
            if data['headers']:
                meteo_file = np.loadtxt(request.FILES['meteo_data'], delimiter="\t", skiprows=1)
            else:
                meteo_file = np.loadtxt(request.FILES['meteo_data'], delimiter="\t")
            
            bulk_meteo_data=[]
            if data['city'][-5:]=='10min'or data['city'][-5:]=='15min':
                for hour_data in meteo_file:
                    bulk_meteo_data += [
                        MeteoData(location=new_location, month_sim=hour_data[0], day_sim=hour_data[1], hour_sim=hour_data[2],min_sim=hour_data[3] ,hour_year_sim=hour_data[4], GHI=hour_data[5], DNI=hour_data[9], temp=hour_data[10])
                        ]
            else:
                 for hour_data in meteo_file:
                    bulk_meteo_data += [
                        MeteoData(location=new_location, month_sim=hour_data[0], day_sim=hour_data[1], hour_sim=hour_data[2] ,hour_year_sim=hour_data[3], GHI=hour_data[4], DNI=hour_data[8], temp=hour_data[9])
                        ]   
            MeteoData.objects.bulk_create(bulk_meteo_data)
            #meteo_data.order_by('hour_year_sim').values_list('DNI',flat=True)
        return HttpResponseRedirect('/')
        #return render(request,'new_location.html', {'form':sim_form})

    else:
        sim_form = NewLocation()
        
    return render(request,'new_location.html', {'form':sim_form})

def new_fuel(request):
    if request.method=="POST":
        fuel = FuelForm(request.POST)
        fuel_units = FuelUnitsForm(request.POST)
        f2 = FuelForm2(request.POST)

        if fuel.is_valid() and fuel_units.is_valid():
            u = json.loads(fuel_units.cleaned_data["units_js"])
            fuel_data = fuel.cleaned_data
            n_fuel = Fuels(fuel=fuel_data["fuel"], co2factor=fuel_data["co2factor"])
            n_fuel.save()
            bulk_fuelunits=[]
            for factor_name in u:
                bulk_fuelunits += [FuelUnits(fuel=n_fuel, factor_name=factor_name, conversion_factor=u[factor_name])]
            FuelUnits.objects.bulk_create(bulk_fuelunits)
            n_fuel.co2units = FuelUnits.objects.get(fuel=n_fuel, factor_name=request.POST['co2units'])
            n_fuel.save()
            return HttpResponseRedirect("/")
        return render(request, 'new_fuel.html', {'form_f':fuel, 'form_fu':fuel_units})
    else:
        fuel = FuelForm()
        fuel_units = FuelUnitsForm()
        f2 = FuelForm2()
        
        return render(request, 'new_fuel.html', {'form_f':fuel, 'form_fu':fuel_units, 'f2':f2})

class update_fuel(UpdateView):
    model = Fuels
    form_class = FuelForm
    success_url = reverse_lazy('simulate')
    template_name = 'new_fuel.html'

def async_locations(request):
    loc=Locations.objects.filter(pais=request.GET['pais'])
    sim_form = SimulationForm()
    sim_form.fields['location'].queryset=loc
    return render(request, 'async/locations.html', {'form':sim_form})

def async_fueltab(request):
    table_data = request.GET
    table_data = table_data.dict()

    return render(request, 'async/table_fuelunits.html', {'tinfo':table_data})

def async_co2factorunit(request):
    table_data = request.GET
    table_data = table_data.dict()
    fuel = FuelForm2()
    choices = []
    for k in table_data:
        choices += [(k,k)]
    
    fuel.fields['co2units'].choices = choices

    return render(request, 'async/co2factunits.html', {'form':fuel})

def async_sim_fu(request):
    fuel = FuelUnits.objects.filter(fuel=request.GET['fuel_id'])
    sim_form = SimulationForm()
    sim_form.fields['fuel_price_unit'].queryset=fuel
    return render(request, 'async/async_sim_fu.html', {'form':sim_form})

def async_integrations(request):
    connection = request.GET['connection']
    if connection=="direct":
        choices=[
            ('SL_L_P','SL_L_P'), 
            ('SL_L_RF','SL_L_RF'), 
            ('SL_L_DRF','SL_L_DRF'), 
            ('SL_L_S_PH','SL_L_S_PH'), 
            ('SL_S_FW','SL_S_FW'), 
            ('SL_S_PD_OT','SL_S_PD_OT'), 
            ('PL_E_PM','PL_E_PM'), 
            ('SL_S_MW','SL_S_MW'), 
            ('SL_S_PD','SL_S_PD'), 
        ]
    else: # == w_storage
        choices=[
            ('SL_L_PS','SL_L_PS'), 
            ('SL_L_S','SL_L_S'), 
            ('SL_S_FWS','SL_S_FWS'), 
            ('SL_S_MWS','SL_S_MWS'), 
            ('SL_S_PDS','SL_S_PDS'), 
        ]
    sim_form = SimulationForm()
    sim_form.fields['type_integration'].choices=choices
    return render(request, 'async/integrations.html', {'form':sim_form})