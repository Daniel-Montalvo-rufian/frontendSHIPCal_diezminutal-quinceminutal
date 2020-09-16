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
    Production_max = models.FloatField(_("Maximum production"))
    Production_lim = models.FloatField(_("Limited production"))
    Perd_term_anual = models.FloatField(_("Annual thermal losses"))
    DNI_anual_irradiation = models.FloatField(_("Annual irradiation"))
    Area = models.FloatField()
    num_loops = models.IntegerField(_("Number of loops"))
    imageQlty = models.SmallIntegerField(_("Images quality"))
    plotPath = models.CharField(_("Plots path"), max_length=150)
    Energy_Before_annual = models.FloatField(_("Energy before boiler"))
    m_dot_min_kgs = models.FloatField(_("Minimum massic flux"))
    steps_sim = models.IntegerField(_("Simulation steps"))
    AmortYear = models.SmallIntegerField(_("Amortization year"))
    Selling_price = models.FloatField(_("Selling price"))
    in_s = models.FloatField(_("Inlet entropy"))
    out_s = models.FloatField(_("Outlet entropy"))
    T_in_flag = models.SmallIntegerField(_("Feeded from grid (0 no, 1 yes)"))
    Fuel_price = models.FloatField(_("Fuel price"))
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
    n_years_sim = models.SmallIntegerField(_("Years simulated"))

    Break_cost = models.TextField(_("Break cost")) #list
    Acum_FCF = models.TextField(_("Acumulated FCF")) #list
    FCF = models.TextField() #list
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
    version = models.CharField(_("Version"),  max_length=15)
    logo_output = models.CharField(_("Logo output"), max_length=150)
    type_integration = models.CharField(_("Integration schema"), choices=integration_schemas, max_length=20)
    energyStored = models.IntegerField(_("Stored energy"))
    location = models.CharField(_("Location"), max_length=200)
    Area_total = models.FloatField(_("Total area"))
    n_coll_loop = models.IntegerField(_("Collectors per loop"))
    energStorageMax = models.IntegerField(_("Max stored energy"))
    num_loops = models.IntegerField(_("Number of loops"))
    m_dot_min_kgs = models.FloatField(_("Minimum massic flux"))
    Production_max = models.FloatField(_("Maximum production"))
    Production_lim = models.FloatField(_("Limited production"))
    Demand_anual = models.FloatField(_("Annual demand"))
    solar_fraction_max = models.FloatField(_("Maximum solar fraction"))
    solar_fraction_lim = models.FloatField(_("Limited solar fraction"))
    DNI_anual_irradiation = models.FloatField(_("Annual irradiation"))
    AmortYear = models.SmallIntegerField(_("Amortization year"))
    finance_study = models.SmallIntegerField(_("Requested finance study (0 no, 1 yes)"))
    CO2 = models.SmallIntegerField("CO2 flag")
    co2Savings = models.FloatField(_("Savings from CO2"))
    TIRscript = models.CharField(_("IRR text"), max_length=30)
    TIRscript10 = models.CharField(_("IRR10 text"), max_length=40)
    Amortscript = models.CharField(_("Amortization text"), max_length=40)
    co2TonPrice = models.FloatField(_("Price per CO2 Ton"))
    fuelIncremento = models.FloatField(_("Fuel increase"))
    IPC = models.FloatField()
    Selling_price = models.FloatField(_("Selling price"))
    IRR = models.FloatField(_("IRR"))
    IRR10 = models.FloatField(_("IRR 10"))
    tonCo2Saved = models.FloatField(_("CO2 saved Tons"))
    LCOE = models.FloatField(_("Levelized cost of energy"))
    Energy_savings_mean = models.FloatField(_("Mean energy savings"))
    lang = models.CharField(_("Language"),  max_length=5)
    sender = models.CharField(_("Sender"),  max_length=35)
    cabecera = models.CharField(_("Report header"), max_length=40)
    mapama = models.SmallIntegerField()
    totalCharged = models.FloatField(_("Total charged energy"))
    totalDischarged = models.FloatField(_("Total discharged energy"))
    totalDefocus = models.FloatField(_("Total defocused energy"))
    improvStorage = models.FloatField()
    Utilitation_ratio = models.FloatField(_("Utilization ratio"))
    flowrate_kgs_average = models.FloatField(_("Mean massic flux"))
    Energy_module_max = models.FloatField(_("Max energy produced per module"))
    mofINV = models.IntegerField(_("Investment modificator"))
    mofDNI = models.IntegerField(_("Irradiation modificator"))
    mofProd = models.IntegerField(_("Production modificator"))
    fraction_savings = models.FloatField(_("Mean savings"))

    fuelPrizeArrayList = models.TextField(_("Yearly fuel price")) #list
    Acum_FCFList = models.TextField(_("Acumulated FCF")) #list
    Energy_savingsList = models.TextField(_("Energy savings")) #list
    OM_cost_year = models.TextField(_("Operation and maniteinance annual costs")) #list
    anual_energy_cost = models.TextField(_("Annual energy costs")) #list
    Q_prod = models.TextField(_("Produced heat")) #list
    Q_prod_lim = models.TextField(_("Limited produced heat")) #list
    Demand = models.TextField(_("Annual demand")) #list
    Q_charg = models.TextField(_("Charged heat")) #list
    Q_discharg = models.TextField(_("Discharged heat")) #list
    Q_defocus = models.TextField(_("Defocused heat")) #list
    flow_rate_kgs = models.TextField(_("Massic flows")) #list
