import pandas as pd

# Input should be a file with all rows containing regio metadata manually extracted from all metadata as downloaded from CBS
regions = pd.read_csv("metadata_regios.csv", sep=';')
regions['Key'] = regions['Key'].str.strip()

# Input should be the municipality-level data as downloaded from CBS
municipalities = pd.read_csv("vermogen_gemeenten.csv", sep=';')
municipalities['TotaalVermogen_3'] = municipalities['TotaalVermogen_3'].str.strip()
municipalities['GemiddeldVermogen_4'] = municipalities['GemiddeldVermogen_4'].str.strip()
municipalities['MediaanVermogen_5'] = municipalities['MediaanVermogen_5'].str.strip()
municipalities = pd.merge(municipalities, regions.rename(columns={'Title':'Regionaam'}), left_on='RegioS', right_on='Key', how='left').drop(['Key', 'Description'], axis=1)
municipalities['RegioType'] = 'Municipality'
print(municipalities)
municipalities.to_csv('vermogen_gemeenten_modified.csv', index=False)

# Input should be the province-level data as downloaded from CBS
provinces = pd.read_csv("vermogen_provincies.csv", sep=';')
provinces['RegioS'] = provinces['RegioS'].str.strip()
provinces['TotaalVermogen_3'] = provinces['TotaalVermogen_3'].str.strip()
provinces['GemiddeldVermogen_4'] = provinces['GemiddeldVermogen_4'].str.strip()
provinces = pd.merge(provinces, regions.rename(columns={'Title':'Regionaam'}), left_on='RegioS', right_on='Key', how='left').drop(['Key', 'Description'], axis=1)
provinces['RegioType'] = 'Province'
provinces['Regionaam'] = provinces['Regionaam'].map(lambda x: x.rstrip(' (PV)'))
print(provinces)
provinces.to_csv('vermogen_provincies_modified.csv', index=False)

# Input should be the country-level data as downloaded from CBS
netherlands = pd.read_csv("vermogen_nederland.csv", sep=';')
netherlands['RegioS'] = netherlands['RegioS'].str.strip()
netherlands['Regionaam'] = 'Netherlands'
netherlands['RegioType'] = 'Country'
print(netherlands)
netherlands.to_csv('vermogen_nederland_modified.csv', index=False)
