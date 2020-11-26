import pandas as pd

df = pd.read_csv('Open_Data_RDW__Gekentekende_voertuigen.csv')

passenger_cars = df.loc[df['Voertuigsoort'] == 'Personenauto']

passenger_cars.to_csv('passenger_cars.csv', index=False)
