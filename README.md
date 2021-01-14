# COVID-19 evolution in Galicia
***
This repository hosts datasets retrieved from official sources regarding COVID-19 evolution in Galicia. It also includes a Github page where data is updated automatically every day by running a set of scripts at 10:30 PM that generate several graphs plotting the relevant information.

## Datasets

At the moment two datasets are maintained in the repository:

- [data_galicia_covid](https://github.com/dgarcoe/COVID19_Galicia/blob/main/data_galicia_covid.csv) : This dataset contains general daily indicators related to COVID-19 evolution in Galicia.
- [data_galicia_vaccination.csv](https://github.com/dgarcoe/COVID19_Galicia/blob/main/data_galicia_vaccination.csv) : This datasets contains the evolution of vaccination in Galicia.

## Data sources

- Before the creation of the official coronavirus SERGAS web data was retrieved from daily press releases from [Xunta de Galicia](https://www.xunta.gal/notas-de-prensa). Data was manually saved in an Excel file.
- [Official SERGAS web for coronavirus](https://coronavirus.sergas.gal/datos/#/gl-ES/galicia)
- [Vaccination data from Spain's Ministry of Health](https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov/vacunaCovid19.htm). For the moment this data is manually saved when updated.

## Scripts

The following Python scripts are included in the code to automate data retrieval and graph generation:

- [update_data.py](https://github.com/dgarcoe/COVID19_Galicia/blob/main/update_data.py) : Retrieves data from the official source and creates a new row in the dataset for each day.
- [update-graphs.py](https://github.com/dgarcoe/COVID19_Galicia/blob/main/update_graphs.py) : Creates all the graphs to be included in the webpage in html format.
- [update-repo.py](https://github.com/dgarcoe/COVID19_Galicia/blob/main/update_repo.py) : Launches the previous scripts and updates this repository.

## Telegram bot

You can access to some of the data also through the Telegram bot [@covid19_galicia_bot](https://t.me/covid19_galicia_bot). Keep in mind that the bot is running in a Raspberry Pi at the moment so it may overload with too much queries.

The following is a list of the available commands right now:

- /help: Prints the bot help.
- /getKpis: Prints the last day evolution of main KPIs in Galicia.
- /getIA: Prints the last day incidence rate values.
- /getHosp: Prints the last day hospital occupation data.
- /getAreas: Prints main info from all the Galicia health regions.
- /getVac: Prints main info related to the vaccination campaign in Galicia.
- /getDate: Prints the date when data has been last updated.

Profile bot picture image credit: Desiree Ho for the [Innovative Genomics Institute](https://innovativegenomics.org/free-covid-19-illustrations/).
