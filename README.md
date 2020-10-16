# SHIPcal_demo

This is a functional Django front-end demo to be used with the simulation engine [SHIPcal](https://github.com/mfrasquet/SHIPcal). This front-end will allow you to visually perform simulations of solar heat for industrial processes and see the results in a matter of seconds.

## Installation

You want to have an environment manager. Using conda will make the installation easier; get conda with python 3 from [anaconda](https://www.anaconda.com/products/individual) or [miniconda](https://docs.conda.io/en/latest/miniconda.html). You could use another environment manager as pipenv or venv. You may also find it useful to get [Git](https://git-scm.com/downloads). Nevertheless, the only true requirement is to have python 3 and pip installed.

### Get the project
First, move to the directory where you will work from and clone this repository using git. Alternatively, you can download the *.zip file from the top right corner of this repository and extract the content. To clone the repository using git type and run in your terminal
```
git clone https://github.com/jaarpa/SHIPcal_demo.git
```
The previous command will create a folder called `SHIPcal_demo` you have to clone inside the `SHIPcal` repository
```
git clone https://github.com/mfrasquet/SHIPcal SHIPcal_demo/SHIPcal
```
now you have a full copy of the project in your local machine. Alternatively, you could place the SHIPcal repository downloading the zip file from [SHIPcal](https://github.com/mfrasquet/SHIPcal) and extract the content inside the SHIPcal_Demo folder.

### Install the dependencies.

The SHIPcal_demo project ships a `requirements.txt` and an `enviroment.yml` which will assist you to configure all the required packages.
#### Conda installation

If you have conda installed it is only matter to run from the terminal

```
conda env create -f environment.yml
conda activate SHIPcal_demo
```
and you are ready to go!. Just run 
```
python manage.py runserver
```
and type `localhost:8000` in your preferred web browser.

#### Otherwise

If you are using an environment manager different to conda or no environment manager at all you can similarly run in the virtual environment (if you have any) in your terminal
```
pip3 install -r requirements.txt
```
and you would be ready to go!. Just run 
```
python manage.py runserver
```
and type `localhost:8000` in your preferred web browser.

Nevertheless, this method is more likely to fail and you would have to try to install each package manually (don't worry there are not that many).

## Usage tutorial
There are a few things that are region/user dependent in the simulations (e.g. the locations, fuels, collectors) you can feed SHIPcal with the information to simulate any of these (and you have to perform any simulation).

### Add a new location

Go to the navigation menu, under Add>New location to open the new location form.

You must fill out the form with the correct data and upload a typical meteorological year (TMY) file of the location to get an accurate simulation. `SHIPcal_demo` already has a TMY example that you can use to feed the database, this file is located in `SHIPcal_demo/Tijuana.dat`. 

The `Tijuana.dat` file is the standard output of a TMY from Meteonorm **using solar time**. Select the country of the city (i.e. Mexico) the name of the city (i.e. Tijuana), its location (i.e. Lat = 32.5422951, Longitude=-116.9706862). Mark the checkbox if the file contains a line of headers, do not check it if doesn't contain headers at all, `Tijuana.dat` does not contain headers. Upload the file `SHIPcal_demo/Tijuana.dat`. 
Finally, click the save button and the location will be loaded to the database (it might take a couple of seconds).

### Add a new fuel

Go to the navigation menu, under Add>New fuel to open the new fuel form.

Add the name of the fuel, say Gas LP. SHIPcal works internally using kWh, that's why you should provide the conversion factors from any other fuel unit into kWh, for example, 1 kWh is equivalent to 0.08 kg of GLP then you fill in 0.08 kg/kWh and click the add button. Add as many conversion factors as you know. 

You should add the equivalence of CO2 ton per unit too, the available units are the same that you have added before. This will be useful to calculate how much CO2 is saved.

Click the Create button to make this fuel available for simulation.

### Add a collector

Coming soon, currently, only a default collector is supported. Make a pull request!

### Simulate

Once you have added a location, fuels, and collectors, you are ready to simulate!
Go to Simulate in the navigation menu and fill-up the form with the data for the simulation and click the simulate button. In a few seconds, you would be redirected to the results.

## TODO
- [ ] Functionality to add new collectors
- [ ] Translations
- [ ] Update/Delete fuels view
- [ ] Update/Delete locations view
- [ ] Update/Delete simulation view
- [x] Results view to get previous simulation results.
- [ ] PDF generation report
