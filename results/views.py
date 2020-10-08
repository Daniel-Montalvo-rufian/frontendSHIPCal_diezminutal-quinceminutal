from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from .models import SimResults, TemplateVars, PlotVars, ReportVars
from numpy import array

from SHIPcal.Plot_modules.plottingSHIPcal import SankeyPlot,prodWinterPlot,prodSummerPlot,financePlot,storageWinter,storageSummer,prodMonths,savingsMonths #noqa
from SHIPcal.Plot_modules.plottingSHIPcal import mollierPlotST,mollierPlotSH,rhoTempPlotOil,viscTempPlotOil,rhoTempPlotSalt,viscTempPlotSalt,demandVsRadiation, storageNonAnnual,flowRatesPlot #noqa
from SHIPcal.Plot_modules.plottingSHIPcal_2 import prodMonths2, prodSummerPlot2, prodWinterPlot2, savingsMonths2,demandVsRadiation2, storageNonAnnual2, flowRatesPlot2
# Create your views here.

def all_results(request):
    every_simulation = SimResults.objects.all()
    
    return render(request, 'results.html', {'simulations':every_simulation})


def result(request, sim_id):
   
    sim_results = SimResults.objects.get(simulation=sim_id)

    #For converting back [float(item) for item in string_series.split()]
    rv_l = {
        'Energy_savingsList':[float(item) for item in (sim_results.reportsVar.Energy_savingsList).split(",")],
        'anual_energy_cost':[float(item) for item in (sim_results.reportsVar.anual_energy_cost).split(",")],
    }

    pv_d = model_to_dict(sim_results.plotVars)

    pv_d.update({
        'Break_cost':[float(item) for item in (sim_results.plotVars.Break_cost).split(",")], 
        'Acum_FCF':[float(item) for item in (sim_results.plotVars.Acum_FCF).split(",")], 
        'FCF':[float(item) for item in (sim_results.plotVars.FCF).split(",")], 
        'T_in_C_AR':[float(item) for item in (sim_results.plotVars.T_in_C_AR).split(",")], 
        'Demand':[float(item) for item in (sim_results.plotVars.Demand).split(",")], 
        'Q_prod':[float(item) for item in (sim_results.plotVars.Q_prod).split(",")], 
        'Q_prod_lim':[float(item) for item in (sim_results.plotVars.Q_prod_lim).split(",")], 
        'Q_charg':[float(item) for item in (sim_results.plotVars.Q_charg).split(",")], 
        'Q_discharg':[float(item) for item in (sim_results.plotVars.Q_discharg).split(",")], 
        'DNI':[float(item) for item in (sim_results.plotVars.DNI).split(",")], 
        'SOC':[float(item) for item in (sim_results.plotVars.SOC).split(",")], 
        'Q_useful':[float(item) for item in (sim_results.plotVars.Q_useful).split(",")], 
        'Q_defocus':[float(item) for item in (sim_results.plotVars.Q_defocus).split(",")], 
        'T_alm_K':[float(item) for item in (sim_results.plotVars.T_alm_K).split(",")], 
        'step_sim':[float(item) for item in (sim_results.plotVars.step_sim).split(",")],
        'Q_prod_steam':[float(item) for item in (sim_results.plotVars.Q_prod_steam).split(",")],
        'Q_drum':[float(item) for item in (sim_results.plotVars.Q_drum).split(",")],
        'SD_energy':[float(item) for item in (sim_results.plotVars.SD_energy).split(",")],
        'Q_prod_rec':[float(item) for item in (sim_results.plotVars.Q_prod_rec).split(",")],
    })
    print('itercontrol es:', sim_results.plotVars.itercontrol,'pasos de simulación son:',sim_results.plot.steps_sim)
    if sim_results.plot.steps_sim==8760 or sim_results.plot.steps_sim==52560 or sim_results.plot.steps_sim==35040:
        if sim_results.plotVars.itercontrol!='paso_10min' and sim_results.plotVars.itercontrol!='paso_15min':
            plots = {
            'image_financePlot': financePlot(**pv_d),
            'image_prodMonths': prodMonths(**pv_d)
            }
        else:
            plots = {
            'image_financePlot': financePlot(**pv_d),
            'image_prodMonths': prodMonths2(**pv_d)
            }
        return render(request,'imp.html', {'s':sim_results, 'rv_l':rv_l, 'p':plots})
    else:
        if sim_results.plotVars.itercontrol!='paso_10min' and sim_results.plotVars.itercontrol!='paso_15min':
            plots = {
            'image_prodvsdemand': demandVsRadiation(**pv_d),
            'image_storage': storageNonAnnual(**pv_d)
            }
        else:
            plots = {
            'image_prodvsdemand': demandVsRadiation2(**pv_d),
            'image_storage': storageNonAnnual2(**pv_d)
            }
        return render(request,'imp.html', {'s':sim_results, 'rv_l':rv_l, 'p':plots})

def result_instalation(request, sim_id):
    sim_results = SimResults.objects.get(simulation=sim_id)

    #For converting back [float(item) for item in string_series.split()]
    rv_l = {
        # 'Energy_savingsList':[float(item) for item in (sim_results.reportsVar.Energy_savingsList).split(",")],
        # 'anual_energy_cost':[float(item) for item in (sim_results.reportsVar.anual_energy_cost).split(",")],

        # 'fuelPrizeArrayList': [float(item) for item in (sim_results.reportsVar.fuelPrizeArrayList).split(",")], 
        # 'Acum_FCFList':[float(item) for item in (sim_results.reportsVar.Acum_FCFList).split(",")],
        # 'OM_cost_year':[float(item) for item in (sim_results.reportsVar.OM_cost_year).split(",")],
        # 'Q_prod':[float(item) for item in (sim_results.reportsVar.Q_prod).split(",")],
        # 'Q_prod_lim':[float(item) for item in (sim_results.reportsVar.Q_prod_lim).split(",")],
        # 'Demand':[float(item) for item in (sim_results.reportsVar.Demand).split(",")],
        # 'Q_charg':[float(item) for item in (sim_results.reportsVar.Q_charg).split(",")],
        # 'Q_discharg':[float(item) for item in (sim_results.reportsVar.Q_discharg).split(",")],
        # 'Q_defocus':[float(item) for item in (sim_results.reportsVar.Q_defocus).split(",")],
        # 'flow_rate_kgs':[float(item) for item in (sim_results.reportsVar.flow_rate_kgs).split(",")],
    }
    if sim_results.plot.steps_sim==8760 or sim_results.plot.steps_sim==52560 or sim_results.plot.steps_sim==35040:
        return render(request,'imp_instalation.html', {'s':sim_results})
    else:
        return render(request,'imp_instalation.html')
def result_production(request, sim_id):
    sim_results = SimResults.objects.get(simulation=sim_id)
    
    pv_d = model_to_dict(sim_results.plotVars)

    pv_d.update({
        'Break_cost':[float(item) for item in (sim_results.plotVars.Break_cost).split(",")], 
        'Acum_FCF':[float(item) for item in (sim_results.plotVars.Acum_FCF).split(",")], 
        'FCF':[float(item) for item in (sim_results.plotVars.FCF).split(",")], 
        'T_in_C_AR':[float(item) for item in (sim_results.plotVars.T_in_C_AR).split(",")], 
        'Demand':[float(item) for item in (sim_results.plotVars.Demand).split(",")], 
        'Q_prod':[float(item) for item in (sim_results.plotVars.Q_prod).split(",")], 
        'Q_prod_lim':[float(item) for item in (sim_results.plotVars.Q_prod_lim).split(",")], 
        'Q_charg':[float(item) for item in (sim_results.plotVars.Q_charg).split(",")], 
        'Q_discharg':[float(item) for item in (sim_results.plotVars.Q_discharg).split(",")], 
        'DNI':[float(item) for item in (sim_results.plotVars.DNI).split(",")], 
        'SOC':[float(item) for item in (sim_results.plotVars.SOC).split(",")], 
        'Q_useful':[float(item) for item in (sim_results.plotVars.Q_useful).split(",")], 
        'Q_defocus':[float(item) for item in (sim_results.plotVars.Q_defocus).split(",")], 
        'T_alm_K':[float(item) for item in (sim_results.plotVars.T_alm_K).split(",")], 
        'Q_prod_steam':[float(item) for item in (sim_results.plotVars.Q_prod_steam).split(",")],
        'Q_drum':[float(item) for item in (sim_results.plotVars.Q_drum).split(",")],
        'SD_energy':[float(item) for item in (sim_results.plotVars.SD_energy).split(",")],
        'Q_prod_rec':[float(item) for item in (sim_results.plotVars.Q_prod_rec).split(",")],
    })

    # Plots of fluid properties
    fluid = sim_results.simulation.fluid
    if fluid=="water": #WATER
        #Mollier Plot for s-t for Water
        image_prop1 = mollierPlotST(**pv_d)
        #Mollier Plot for s-h for Water 
        image_prop2 = mollierPlotSH(**pv_d)
    elif fluid=="oil": 
        image_prop1 = rhoTempPlotOil(**pv_d) #(12) Plot thermal oil properties Rho & Cp vs Temp
        image_prop2 = viscTempPlotOil(**pv_d) #(13) Plot thermal oil properties Viscosities vs Temp
    elif fluid=="moltenSalt": 
        image_prop1 = rhoTempPlotSalt(**pv_d) #(12) Plot thermal oil properties Rho & Cp vs Temp
        image_prop2 = viscTempPlotSalt(**pv_d) #(13) Plot thermal oil properties Viscosities vs Temp
    if sim_results.plot.steps_sim==8760 or sim_results.plot.steps_sim==52560 or sim_results.plot.steps_sim==35040:
        if sim_results.plotVars.itercontrol!='paso_10min' and sim_results.plotVars.itercontrol!='paso_15min':
            plots = {
            'image_prodMonths': prodMonths(**pv_d),
            'image_Sankey': SankeyPlot(**pv_d),
            'image_prodSummerPlot': prodSummerPlot(**pv_d),
            'image_prodWinterPlot': prodWinterPlot(**pv_d),
            'image_prop1':image_prop1,
            'image_prop2':image_prop2
                }
        else:
            plots = {
            'image_prodMonths': prodMonths2(**pv_d),
            'image_Sankey': SankeyPlot(**pv_d),
            'image_prodSummerPlot': prodSummerPlot2(**pv_d),
            'image_prodWinterPlot': prodWinterPlot2(**pv_d),
            'image_prop1':image_prop1,
            'image_prop2':image_prop2
                }
    else:
        if sim_results.plotVars.itercontrol!='paso_10min' and sim_results.plotVars.itercontrol!='paso_15min':
            plots = {
            'image_prodvsdemand': demandVsRadiation(**pv_d),
            'image_Storage':storageNonAnnual(**pv_d),
            'image_flowrateandtemperature': flowRatesPlot(**pv_d),
            
            'image_prop1':image_prop1,
            'image_prop2':image_prop2
                }
        else:
            plots = {
            'image_prodvsdemand': demandVsRadiation2(**pv_d),
            'image_Sankey':storageNonAnnual2(**pv_d),
            'image_flowrateandtemperature': flowRatesPlot2(**pv_d),
            
            'image_prop1':image_prop1,
            'image_prop2':image_prop2
                }

    return render(request,'imp_prod.html', {'s':sim_results, 'p':plots,})
    
def result_finance(request, sim_id):
    sim_results = SimResults.objects.get(simulation=sim_id)

    rv_l = {
        'Energy_savingsList':[float(item) for item in (sim_results.reportsVar.Energy_savingsList).split(",")],
        'anual_energy_cost':[float(item) for item in (sim_results.reportsVar.anual_energy_cost).split(",")],
        #'n_anual_energy_cost':anual_energy_cost - energy_savingsList
        'fuelPrizeArrayList': [float(item) for item in (sim_results.reportsVar.fuelPrizeArrayList).split(",")], 
        'Acum_FCF':[float(item) for item in (sim_results.plotVars.Acum_FCF).split(",")], 
        'FCF':[float(item) for item in (sim_results.plotVars.FCF).split(",")], 

        'OM_cost_year':[float(item) for item in (sim_results.reportsVar.OM_cost_year).split(",")],
    }

    n_anual_energy_cost = array(rv_l["anual_energy_cost"])-array(rv_l["Energy_savingsList"])
    t_data = zip(rv_l["fuelPrizeArrayList"][:15],rv_l["anual_energy_cost"][:15],n_anual_energy_cost.tolist()[:15],rv_l["Energy_savingsList"][:15],rv_l["FCF"][:15],rv_l["Acum_FCF"][:15])

    pv_d = model_to_dict(sim_results.plotVars)

    pv_d.update({
        'Break_cost':[float(item) for item in (sim_results.plotVars.Break_cost).split(",")], 
        'Acum_FCF':[float(item) for item in (sim_results.plotVars.Acum_FCF).split(",")], 
        'FCF':[float(item) for item in (sim_results.plotVars.FCF).split(",")], 
        'T_in_C_AR':[float(item) for item in (sim_results.plotVars.T_in_C_AR).split(",")], 
        'Demand':[float(item) for item in (sim_results.plotVars.Demand).split(",")], 
        'Q_prod':[float(item) for item in (sim_results.plotVars.Q_prod).split(",")], 
        'Q_prod_lim':[float(item) for item in (sim_results.plotVars.Q_prod_lim).split(",")], 
        'Q_charg':[float(item) for item in (sim_results.plotVars.Q_charg).split(",")], 
        'Q_discharg':[float(item) for item in (sim_results.plotVars.Q_discharg).split(",")], 
        'DNI':[float(item) for item in (sim_results.plotVars.DNI).split(",")], 
        'SOC':[float(item) for item in (sim_results.plotVars.SOC).split(",")], 
        'Q_useful':[float(item) for item in (sim_results.plotVars.Q_useful).split(",")], 
        'Q_defocus':[float(item) for item in (sim_results.plotVars.Q_defocus).split(",")], 
        'T_alm_K':[float(item) for item in (sim_results.plotVars.T_alm_K).split(",")], 
        'Q_prod_steam':[float(item) for item in (sim_results.plotVars.Q_prod_steam).split(",")],
        'Q_drum':[float(item) for item in (sim_results.plotVars.Q_drum).split(",")],
        'SD_energy':[float(item) for item in (sim_results.plotVars.SD_energy).split(",")],
        'Q_prod_rec':[float(item) for item in (sim_results.plotVars.Q_prod_rec).split(",")],
    })
    if sim_results.plot.steps_sim==8760 or sim_results.plot.steps_sim==52560 or sim_results.plot.steps_sim==35040:
        if sim_results.plotVars.itercontrol!='paso_10min' and sim_results.plotVars.itercontrol!='paso_15min':
            plots = {
            'image_financePlot': financePlot(**pv_d),
            'image_savingsMonths': savingsMonths(**pv_d),
            }
        else:
            plots = {
            'image_financePlot': financePlot(**pv_d),
            'image_savingsMonths': savingsMonths2(**pv_d),
            }
        return render(request,'imp_finance.html', {'s':sim_results, 'pv_d':pv_d, 'rv_l':rv_l, 'p':plots, 't':t_data})
    else:
        return render(request,'imp_finance.html')