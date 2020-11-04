from django.db import models
from django.core import validators
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

# Create your models here.
class Simulation(models.Model):
    
    #Who is simulating
    name = models.CharField(_("Name"), max_length=30)
    email = models.EmailField("e-mail",)
    #What is simulating
    industry = models.CharField(_("Industry"), max_length=30)
    sectorIndustry = models.CharField(_("Industry sector"), max_length=30)
    process = models.TextField(_("Process description"), blank=True, null=True)
    #Solar time
    to_solartime= models.CharField(_("Do you want to calculate the solar time?"), choices=[('on',_("Yes")),('off',_("No"))], max_length=3)
    huso=models.FloatField(_("In case you have chosen to calculate solar time, write here the difference between the format of the TMY`s time and UTC"),)
    #Simulation date and time
    date = models.DateTimeField(_("Date"), auto_now=True)
    itercontrol= models.CharField(_("Step of simulation"), choices=[('paso_10min',_("10 minutes")),('paso_15min',_("15 minutes")),('horario',_("hourly steps"))], max_length=10)
    annual=models.CharField(_("Do you want to simulate during a full year?"), choices=[('yes',_("Yes")),('no',_("No"))], max_length=3)
    #Financial data
    co2TonPrice = models.FloatField(validators=[validators.MinValueValidator(0, message=_("The CO2 price cannot be less than 0"))])
    businessModel = models.CharField(_("Business model"), choices=[('turnkey',_("Turnkey project")),('ESCO','ESCO')], max_length=10)
    fuel_price = models.FloatField(_("Fuel price"),validators=[validators.MinValueValidator(0, message=_("The fuel price cannot be less than 0"))])

    pais = CountryField(_("Country"))
    location = models.ForeignKey('Locations',on_delete=models.CASCADE)

    surface =models.FloatField(_("Available surface"), validators=[validators.MinValueValidator(0, message=_("The available surface cannot be less than 0"))])
    distance = models.FloatField(_("Distance to process"), validators=[validators.MinValueValidator(0, message=_("The distance cannot be less than 0"))])
    
    fluid=models.CharField(_("Fluid"), max_length=15, choices=[('water',_("Water")),('steam',_("Steam")),('oil',_("Thermal oil")),('moltenSalt',_("Molten salts"))])
    tempOUT=models.FloatField(_("Outlet temperature"),)
    tempIN=models.FloatField(_("Inlet temperature"),)
    connection=models.CharField(_("Connection type"), choices=[('direct',_("Direct to process")),('w_storage',_("With intermediate deposit"))], max_length=30)

    fuel = models.ForeignKey('Fuels', on_delete=models.CASCADE)
    fuel_price_unit = models.ForeignKey('FuelUnits', on_delete=models.CASCADE)

    pressureUnit = models.FloatField(_("Pressure unit"), choices=[(1,"bar"),(10,"MPa"),(0.06894757293, "psi")]) #The factor to convert the pressure into bar
    pressure = models.FloatField(_("Pressure"))

    #Yearly total demand
    demand = models.FloatField(_("Annual energy demand"),validators=[validators.MinValueValidator(0.001, message=_("The demand cannot be less or equal to 0"))])
    demandUnit = models.FloatField(_("Demand unit"), choices=[(1,_("kWh/year")),(1000,_("MWh/year")),(0.000277778, _("KJ/year")),(0.000293071,_("BTU/year")),(0.01163,_("kcal/year"))]) #The factor to convert the demand into kWh

    #Beginning and ending of simulation
    month_ini_sim=models.IntegerField(_("Month in which the simulation starts"),validators=[validators.MinValueValidator(0, message=_("The month cannot be less or equal to 0")),validators.MaxValueValidator(13, message=_("The month cannot be greater than 12"))], default=1 )
    month_fin_sim=models.IntegerField(_("Month in which the simulation ends"),validators=[validators.MinValueValidator(0, message=_("The month cannot be less or equal to 0")),validators.MaxValueValidator(13, message=_("The month cannot be greater than 12"))], default=1 )
    day_ini_sim=models.IntegerField(_("Day in which the simulation starts"),validators=[validators.MinValueValidator(0, message=_("The day cannot be less or equal to 0")),validators.MaxValueValidator(32, message=_("The day cannot be greater than 31"))], default=1 )
    day_fin_sim=models.IntegerField(_("Day in which the simulation ends"),validators=[validators.MinValueValidator(0, message=_("The month cannot be less or equal to 0")),validators.MaxValueValidator(32, message=_("This cannot be greater than 31"))], default=1 )
    hour_fin_sim = models.TimeField(_("Ending hour of simulation. For hourly simulations day starts at 1, so if you write 0, SHIPCal will not run"), )
    hour_ini_sim = models.TimeField(_("Starting hour of simulation. For hourly simulations day starts at 1, so if you write 0, SHIPCal will not run"), )


    #Consumption profile
    #Hourly
    # ten_min_end= models.FloatField(_("), )
    # ten_min_ini= models.FloatField(_("Ending time of simulation, from 0 to 24H"), )
    # fifteen_min_end=
    #fifteen_min_ini
    #Daily
    hourEND = models.IntegerField(_("Last hour with demand in the day"), )
    hourINI= models.IntegerField(_("First hour with demand in the day"))
    #Monthly
    Jan = models.FloatField(_("Jan"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Feb = models.FloatField(_("Feb"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Mar = models.FloatField(_("Mar"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Apr = models.FloatField(_("Apr"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    May = models.FloatField(_("May"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Jun = models.FloatField(_("Jun"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Jul = models.FloatField(_("Jul"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Aug = models.FloatField(_("Aug"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Sep = models.FloatField(_("Sep"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Oct = models.FloatField(_("Oct"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Nov = models.FloatField(_("Nov"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Dec = models.FloatField(_("Dec"),validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    #Weekly 
    Mond = models.FloatField(_("Mon"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Tues = models.FloatField(_("Tue"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Wend = models.FloatField(_("Wed"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Thur = models.FloatField(_("Thu"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Fri = models.FloatField(_("Fri"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Sat = models.FloatField(_("Sat"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)
    Sun = models.FloatField(_("Sun"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0")),validators.MaxValueValidator(1, message=_("This cannot be greater than 1"))], default=0)

    #Not used fields #But they may be used in the future
    terrain=models.CharField(_("Terrain type"), choices=[('clean_ground',_("Clean ground"))], default='clean_ground' ,blank=True, null=True, max_length=30)
    orientation=models.CharField(_("Orientation"), choices=[('NS',_("North-South"))], default='NS',blank=True, null=True, max_length=30)
    inclination=models.CharField(_("Inclination"), choices=[('flat',_("Flat"))], default='flat',blank=True, null=True, max_length=30)
    shadows=models.CharField(_("Shadows"), choices=[('free',_("Shadows free"))], default='free' ,blank=True, null=True, max_length=30)

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
    num_loops=models.IntegerField(_("Number of loops"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0"))])
    n_coll_loop=models.IntegerField(_("Collectors per loop"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0"))])
    type_integration=models.CharField(_("Integration schema"), choices=integration_schemas, max_length=20)
    almVolumen=models.FloatField(_("Thermal storage capacity"), validators=[validators.MinValueValidator(0, message=_("This cannot be less than 0"))], blank=True, default=0)

    mofINV=models.FloatField(_("Investment modificator"), blank=True, default=1)
    mofDNI=models.FloatField(_("Solar radiation modificator"), blank=True, default=1)
    mofProd=models.FloatField(_("Production modificator"), blank=True, default=1)

class Fuels(models.Model):
    fuel = models.CharField(_("Fuel"), max_length=30)
    co2factor = models.FloatField(_("CO2 Ton per"))
    co2units = models.ForeignKey('FuelUnits', on_delete=models.CASCADE, null=True, blank=True)#_("CO2 factor units")

    class Meta:
        verbose_name = _("Fuel")
        verbose_name_plural = _("Fuels")

    def __str__(self):
        return self.fuel

class FuelUnits(models.Model):
    fuel=models.ForeignKey('Fuels', on_delete=models.CASCADE)
    factor_name = models.CharField(_("Conversion factor"), max_length=10) #kWh/ conversion factor e.g kWh/l, kWh/kg, etc.
    conversion_factor = models.FloatField(_("Conversion factor")) #kWh/ conversion factor e.g. kWh/l in order to just multilpy

    class Meta:
        verbose_name = _("Fuel unit")
        verbose_name_plural = _("Fuels units")

    def __str__(self):
        return self.factor_name

class Locations(models.Model):
    pais = CountryField(_("Country"))
    city = models.CharField(_("City"), max_length=200)
    location_aux = models.CharField(default='', blank=True, null=True, max_length=50)
    lat = models.FloatField(_("Latitude"))
    lon = models.FloatField(_("Longitude"))
    #meteo = models.ForeignKey()
    def __str__(self):
        return self.city
    

class MeteoData(models.Model):
    location = models.ForeignKey('Locations', on_delete=models.CASCADE)
    month_sim=models.PositiveSmallIntegerField()
    day_sim=models.PositiveSmallIntegerField()
    hour_sim=models.PositiveSmallIntegerField()
    min_sim=models.PositiveSmallIntegerField(default=0)
    hour_year_sim=models.PositiveSmallIntegerField()
    DNI=models.FloatField()
    GHI=models.FloatField()
    temp=models.FloatField()

    def __str__(self):
        return self.location.city
    