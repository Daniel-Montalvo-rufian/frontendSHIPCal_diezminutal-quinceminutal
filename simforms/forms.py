from .models import Simulation, Locations, Fuels, FuelUnits
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.core.exceptions import ValidationError


class SimulationForm(forms.ModelForm):
    pais = CountryField().formfield(widget=CountrySelectWidget(attrs={'class':'custom-select'}))
    def clean(self):
        cleaned_data = super().clean()
        location = cleaned_data.get("location")
        itercontrol= cleaned_data.get("itercontrol")
        hour_fin_sim= cleaned_data.get("hour_fin_sim").hour
        hour_ini_sim=cleaned_data.get("hour_ini_sim").hour
        if itercontrol=='paso_10min':
            if location.city[-5:]!='10min':
                 raise ValidationError(
                    'TMY must finish with 10min for teen-minutes steps'
                )
        elif itercontrol=='paso_15min':
             if location.city[-5:]!='15min':
                 raise ValidationError(
                    'TMY must finish with 15min for fifteen-minutes steps'
                )

        elif itercontrol!='paso_10min' and    itercontrol!='paso_15min'  :
            if location.city[-5:]=='10min' or location.city[-5:]=='15min':
                raise ValidationError(
                    'TMY must be hourly-step resolution'
                )
            if hour_ini_sim==0 or hour_fin_sim==0:
                raise ValidationError(
                    'For hourly steps, the first hour of the day in the TMY is 1, not 0'
                )
    class Meta:
        model = Simulation
        fields = [
            'name','email','industry','sectorIndustry', 'process',
            'location', 'surface', 'distance',
            'to_solartime', 'huso',
            'co2TonPrice', 'businessModel', 'fuel_price', 'fuel', 'fuel_price_unit',
            'fluid','tempOUT','tempIN','pressureUnit', 'pressure',
            'demand', 'demandUnit', 'hourEND', 'hourINI', 'itercontrol',
            'month_ini_sim', 'month_fin_sim', 'day_ini_sim', 'day_fin_sim', 'hour_fin_sim', 'hour_ini_sim',
            'Mond', 'Tues', 'Wend', 'Thur', 'Fri', 'Sat', 'Sun',
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
            'num_loops', 'n_coll_loop','connection', 'type_integration', 'almVolumen',
            'mofINV', 'mofDNI', 'mofProd',
            'orientation', 'inclination', 'shadows', 'terrain', 
        ]
        widgets = {
            'orientation':forms.Select(attrs={'class':'custom-select'}),
            'inclination':forms.Select(attrs={'class':'custom-select'}),
            'shadows':forms.Select(attrs={'class':'custom-select'}),
            'terrain':forms.Select(attrs={'class':'custom-select'}),

            'itercontrol':forms.Select(attrs={'class':'custom-select'}),
            'to_solartime':forms.Select(attrs={'class':'custom-select'}),
            'huso':forms.NumberInput(attrs={'class':'form-control'}),
            
            'num_loops':forms.NumberInput(attrs={'class':'form-control'}),
            'n_coll_loop':forms.NumberInput(attrs={'class':'form-control'}),
            'connection':forms.Select(attrs={'class':'custom-select'}),
            'type_integration':forms.Select(attrs={'class':'custom-select'}), 
            'almVolumen':forms.NumberInput(attrs={'class':'form-control'}),
            'mofINV':forms.NumberInput(attrs={'class':'form-control'}),
            'mofDNI':forms.NumberInput(attrs={'class':'form-control'}),
            'mofProd':forms.NumberInput(attrs={'class':'form-control'}),

            'name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'industry':forms.TextInput(attrs={'class':'form-control'}),
            'sectorIndustry':forms.TextInput(attrs={'class':'form-control'}), 
            'process':forms.Textarea(attrs={'class':'form-control', 'rows':2}),

            'location':forms.Select(attrs={'class':'custom-select'}),
            'surface':forms.NumberInput(attrs={'class':'form-control'}),
            'distance':forms.NumberInput(attrs={'class':'form-control'}),

            'co2TonPrice':forms.NumberInput(attrs={'class':'form-control'}),
            'businessModel':forms.Select(attrs={'class':'custom-select'}),
            'fuel_price':forms.NumberInput(attrs={'class':'form-control'}), 
            'fuel':forms.Select(attrs={'class':'custom-select'}),
            'fuel_price_unit':forms.Select(attrs={'class':'custom-select'}),

            'fluid':forms.Select(attrs={'class':'custom-select'}),
            'tempOUT':forms.NumberInput(attrs={'class':'form-control'}),
            'tempIN':forms.NumberInput(attrs={'class':'form-control'}),
            'connection':forms.Select(attrs={'class':'custom-select'}),
            'pressureUnit':forms.Select(attrs={'class':'custom-select'}),
            'pressure':forms.NumberInput(attrs={'class':'form-control'}),
            'demand':forms.NumberInput(attrs={'class':'form-control'}),
            'demandUnit':forms.Select(attrs={'class':'custom-select'}),

            'hourEND':forms.NumberInput(attrs={'class':'form-control'}),
            'hourINI':forms.NumberInput(attrs={'class':'form-control'}),
            
            'month_ini_sim':forms.NumberInput(attrs={'class':'form-control'}),
            'month_fin_sim':forms.NumberInput(attrs={'class':'form-control'}),
            'day_ini_sim ':forms.NumberInput(attrs={'class':'form-control'}),
            'day_fin_sim':forms.NumberInput(attrs={'class':'form-control'}),
            'hour_fin_sim' : forms.TimeInput(attrs={'class':'form-control'}),
            'hour_ini_sim': forms.TimeInput(attrs={'class':'form-control'}), 
            
            'Mond':forms.NumberInput(attrs={'class':'form-control'}),
            'Tues':forms.NumberInput(attrs={'class':'form-control'}),
            'Wend':forms.NumberInput(attrs={'class':'form-control'}),
            'Thur':forms.NumberInput(attrs={'class':'form-control'}),
            'Fri':forms.NumberInput(attrs={'class':'form-control'}),
            'Sat':forms.NumberInput(attrs={'class':'form-control'}),
            'Sun':forms.NumberInput(attrs={'class':'form-control'}),
            'Jan':forms.NumberInput(attrs={'class':'form-control'}),
            'Feb':forms.NumberInput(attrs={'class':'form-control'}),
            'Mar':forms.NumberInput(attrs={'class':'form-control'}),
            'Apr':forms.NumberInput(attrs={'class':'form-control'}),
            'May':forms.NumberInput(attrs={'class':'form-control'}),
            'Jun':forms.NumberInput(attrs={'class':'form-control'}),
            'Jul':forms.NumberInput(attrs={'class':'form-control'}),
            'Aug':forms.NumberInput(attrs={'class':'form-control'}),
            'Sep':forms.NumberInput(attrs={'class':'form-control'}),
            'Oct':forms.NumberInput(attrs={'class':'form-control'}),
            'Nov':forms.NumberInput(attrs={'class':'form-control'}),
            'Dec':forms.NumberInput(attrs={'class':'form-control'}),

        }
    
class NewLocation(forms.ModelForm):
    headers = forms.BooleanField(label=_("The file contains a headers"), required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    meteo_data = forms.FileField(label=_("Metorologic file to load"), widget=forms.ClearableFileInput(attrs={'class':'custom-file-input'}))
    error_css_class = 'is_invalid'
    class Meta:
        model = Locations
        fields = [
            'pais', 'city', 'lat', 'lon'
        ]
        widgets = {
            'pais':CountrySelectWidget(attrs={'class':'custom-select'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'lat':forms.NumberInput(attrs={'class':'form-control'}),
            'lon':forms.NumberInput(attrs={'class':'form-control'}),
        }

class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuels
        fields = ['fuel', 'co2factor', ]
        widgets = {
            'fuel':forms.TextInput(attrs={'class':'form-control'}),
            'co2factor':forms.NumberInput(attrs={'class':'form-control'}),
        }

class FuelForm2(forms.Form):
    co2units = forms.ChoiceField(choices=[("kWh","kWh"),], widget=forms.Select(attrs={'class':'custom-select'}))

class FuelUnitsForm(forms.ModelForm):
    units_js = forms.CharField(widget=forms.Textarea(), max_length=250)
    class Meta:
        model = FuelUnits
        fields = ['factor_name', 'conversion_factor']
        widgets = {
            'factor_name':forms.TextInput(attrs={'class':'form-control', 'style':'width:4em; display:inline-block;'}),
            'conversion_factor':forms.NumberInput(attrs={'class':'form-control'}),
        }