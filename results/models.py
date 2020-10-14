from django.db import models
from django.utils.translation import ugettext_lazy as _
from simforms.models import Simulation

# Create your models here.
integration_schemas=[
    ('SL_L_P','SL_L_P'), 
    ('SL_L_PS','SL_L_PS'), 
    ('SL_L_RF','SL_L_RF'), 
    ('SL_L_DRF','SL_L_DRF'), 
    ('SL_L_S','SL_L_S'), 
    ('SL_L_S_PH','SL_L_S_PH'), 
    ('SL_S_FW','SL_S_FW'), 
    ('SL_S_FWS','SL_S_FWS'), 
    ('SL_S_PD_OT','SL_S_PD_OT'), 
    ('PL_E_PM','PL_E_PM'), 
    ('SL_S_MW','SL_S_MW'), 
    ('SL_S_MWS','SL_S_MWS'), 
    ('SL_S_PD','SL_S_PD'), 
    ('SL_S_PDS','SL_S_PDS'), 
]
class SimResults(models.Model):
    simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE)
    version = models.CharField(_("Version"),  max_length=15)
    templateVars = models.OneToOneField('TemplateVars',on_delete=models.CASCADE)
    plotVars = models.OneToOneField('PlotVars',on_delete=models.CASCADE)
    reportsVar = models.OneToOneField('ReportVars',on_delete=models.CASCADE)

class TemplateVars(models.Model):
    v = models.CharField(_("Version"),  max_length=15)

class PlotVars(models.Model):
    lang = models.CharField(_("Language"),  max_length=5)
    Production_max = models.FloatField(_("Maximum production"), default=0)
    Production_lim = models.FloatField(_("Limited production"), default=0)
    Perd_term_anual = models.FloatField(_("Annual thermal losses"), default=0)
    DNI_anual_irradiation = models.FloatField(_("Annual irradiation"), default=0)
    Area = models.FloatField(default=0)
    num_loops = models.IntegerField(_("Number of loops"))
    imageQlty = models.SmallIntegerField(_("Images quality"))
    plotPath = models.CharField(_("Plots path"), max_length=150)
    Energy_Before_annual = models.FloatField(_("Energy before boiler"),default=0)
    m_dot_min_kgs = models.FloatField(_("Minimum massic flux"))
    steps_sim = models.IntegerField(_("Simulation steps"))
    AmortYear = models.SmallIntegerField(_("Amortization year"),default=0)
    Selling_price = models.FloatField(_("Selling price"), default=0)
    in_s = models.FloatField(_("Inlet entropy"))
    out_s = models.FloatField(_("Outlet entropy"))
    T_in_flag = models.SmallIntegerField(_("Feeded from grid (0 no, 1 yes)"))
    Fuel_price = models.FloatField(_("Fuel price"),default=0)
    Boiler_eff = models.FloatField(_("Boiler efficiency"))
    T_in_C = models.FloatField(_("Inlet temperature towards collectors [C]"))
    T_out_C = models.FloatField(_("Outlet temperature from collectors [C]"))
    outProcess_s = models.FloatField(_("Outlet entropy from process"))
    T_out_process_C = models.FloatField(_("Outlet temperature from process"))
    P_op_bar = models.FloatField(_("Work pressure"))
    x_design = models.SmallIntegerField(_("Steam quality"))
    h_in = models.FloatField(_("Inlet enthalpy"))
    h_out = models.FloatField(_("Outlet enthalpy"))
    hProcess_out = models.FloatField(_("Inlet enthalpy towards process"))
    outProcess_h = models.FloatField(_("Outlet enthalpy from process"))
    sender = models.CharField(_("Sender"),  max_length=35)
    type_integration = models.CharField(_("Integration schema"), choices=integration_schemas, max_length=20)
    origin = models.SmallIntegerField(_("Origin"))
    n_years_sim = models.SmallIntegerField(_("Years simulated"),default=0)
    
    itercontrol=models.CharField(_("Control of step resolution"),  max_length=35)
    step_sim=models.TextField(_("Simlation steps")) #list
    Q_prod_steam=models.TextField() #list
    Q_drum=models.TextField() #list
    SD_energy=models.TextField()
    SD_min_energy=models.FloatField()
    SD_max_energy=models.FloatField()
    Q_prod_rec=models.TextField()
    flowrate_kgs=models.TextField()
    flowrate_rec=models.TextField()
    flowDemand=models.TextField()
    flowToHx=models.TextField()
    flowToMix=models.TextField()
    T_in_K=models.TextField()
    T_toProcess_C=models.TextField()
    T_out_K=models.TextField()
    
    
    Break_cost = models.TextField(_("Break cost"),default='0') #list
    Acum_FCF = models.TextField(_("Acumulated FCF"),default='0') #list
    FCF = models.TextField(default='0') #list
    T_in_C_AR = models.TextField(_("Water temperature from grid")) #list
    Demand = models.TextField(_("Demand")) #list
    Q_prod = models.TextField(_("Produced heat")) #list
    Q_prod_lim = models.TextField(_("Limited produced heat")) #list
    Q_charg = models.TextField(_("Charged heat")) #list
    Q_discharg = models.TextField(_("Discharged heat")) #list
    DNI = models.TextField(_("Solar radiation")) #list
    SOC = models.TextField() #list
    Q_useful = models.TextField(_("Useful produced heat")) #list
    Q_defocus = models.TextField(_("Defocused heat")) #list
    T_alm_K = models.TextField(_("Storage temperature [k]")) #list

class ReportVars(models.Model):
    version = models.CharField(_("Version"),  max_length=15,default='-')
    logo_output = models.CharField(_("Logo output"), max_length=150,default='-')
    type_integration = models.CharField(_("Integration schema"), choices=integration_schemas, max_length=20,default='-')
    energyStored = models.IntegerField(_("Stored energy"), default=0)
    location = models.CharField(_("Location"), max_length=200 ,default='-')
    Area_total = models.FloatField(_("Total area"), default=0)
    n_coll_loop = models.IntegerField(_("Collectors per loop"), default=0)
    energStorageMax = models.IntegerField(_("Max stored energy"), default=0)
    num_loops = models.IntegerField(_("Number of loops"), default=0)
    m_dot_min_kgs = models.FloatField(_("Minimum massic flux"), default=0)
    Production_max = models.FloatField(_("Maximum production"), default=0)
    Production_lim = models.FloatField(_("Limited production"), default=0)
    Demand_anual = models.FloatField(_("Annual demand"), default=0)
    solar_fraction_max = models.FloatField(_("Maximum solar fraction"), default=0)
    solar_fraction_lim = models.FloatField(_("Limited solar fraction"), default=0)
    DNI_anual_irradiation = models.FloatField(_("Annual irradiation"), default=0)
    AmortYear = models.SmallIntegerField(_("Amortization year"), default=0)
    finance_study = models.SmallIntegerField(_("Requested finance study (0 no, 1 yes)"), default=0)
    CO2 = models.SmallIntegerField(_("CO2 flag"), default=0)
    co2Savings = models.FloatField(_("Savings from CO2"), default=0)
    TIRscript = models.CharField(_("IRR text"), max_length=30 ,default='-')
    TIRscript10 = models.CharField(_("IRR10 text"), max_length=40 ,default='-')
    Amortscript = models.CharField(_("Amortization text"), max_length=40 ,default='-')
    co2TonPrice = models.FloatField(_("Price per CO2 Ton"), default=0)
    fuelIncremento = models.FloatField(_("Fuel increase"), default=0)
    IPC = models.FloatField( default=0)
    Selling_price = models.FloatField(_("Selling price"), default=0)
    IRR = models.FloatField(_("IRR"), default=0)
    IRR10 = models.FloatField(_("IRR 10"), default=0)
    tonCo2Saved = models.FloatField(_("CO2 saved Tons"), default=0)
    LCOE = models.FloatField(_("Levelized cost of energy"), default=0)
    Energy_savings_mean = models.FloatField(_("Mean energy savings"), default=0)
    lang = models.CharField(_("Language"),  max_length=5 ,default='-')
    sender = models.CharField(_("Sender"),  max_length=35 ,default='-')
    cabecera = models.CharField(_("Report header"), max_length=40 ,default='-')
    mapama = models.SmallIntegerField( default=0)
    totalCharged = models.FloatField(_("Total charged energy"), default=0)
    totalDischarged = models.FloatField(_("Total discharged energy"), default=0)
    totalDefocus = models.FloatField(_("Total defocused energy"), default=0)
    improvStorage = models.FloatField( default=0)
    Utilitation_ratio = models.FloatField(_("Utilization ratio"), default=0)
    flowrate_kgs_average = models.FloatField(_("Mean massic flux"), default=0)
    Energy_module_max = models.FloatField(_("Max energy produced per module"), default=0)
    mofINV = models.IntegerField(_("Investment modificator"), default=0)
    mofDNI = models.IntegerField(_("Irradiation modificator"), default=0)
    mofProd = models.IntegerField(_("Production modificator"), default=0)
    fraction_savings = models.FloatField(_("Mean savings"), default=0)

    fuelPrizeArrayList = models.TextField(_("Yearly fuel price"), default=0) #list
    Acum_FCFList = models.TextField(_("Acumulated FCF"), default=0) #list
    Energy_savingsList = models.TextField(_("Energy savings"), default=0) #list
    OM_cost_year = models.TextField(_("Operation and maniteinance annual costs"), default=0) #list
    anual_energy_cost = models.TextField(_("Annual energy costs"), default=0) #list
    Q_prod = models.TextField(_("Produced heat"), default=0) #list
    Q_prod_lim = models.TextField(_("Limited produced heat"), default=0) #list
    Demand = models.TextField(_("Annual demand"), default=0) #list
    Q_charg = models.TextField(_("Charged heat"), default=0) #list
    Q_discharg = models.TextField(_("Discharged heat"), default=0) #list
    Q_defocus = models.TextField(_("Defocused heat"), default=0) #list
    flow_rate_kgs = models.TextField(_("Massic flows"), default=0) #list
