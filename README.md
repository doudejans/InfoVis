# InfoVis Project: Passenger Cars in The Netherlands

## Dataset

For this data visualization project, we are using a dataset from the Dutch motor vehicle authority (RDW) of all licensed motor vehicles in The Netherlands.
We are using the state of the dataset from November 25, 2020.
This dataset can be found [here](https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2).

Since we are only analyzing the passenger cars for this project, we can create a new CSV with only the rows containing passenger cars (and the CSV header), for example using `grep`:

```sh
grep -E "Kenteken,Voertuigsoort|Personenauto" Open_Data_RDW__Gekentekende_voertuigen.csv > passenger_cars.csv
```
