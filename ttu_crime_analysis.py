# This program reads the TTU Lubbock crime log from the TTPD and helps visualize the data
# The earliest entry in this data is 09/01/2020
# https://banapps.texastech.edu/ITIS/CrimeLog/CrimeLog Source of data
# https://www.depts.ttu.edu/parking/InformationFor/StudentParking/ResidenceHallParking.php Contains Aliases used for the parking lots
# https://www.depts.ttu.edu/clery/reports/2021_TTU_Clery_Lubbock.pdf Valuable information. Page 106 contains some crime statistics.

import pandas as pd
import re
import matplotlib.pyplot as plt
from pandas.core.algorithms import value_counts
from crime_dictionary import crime_dict

# READING HTML 
crime_pdf = pd.read_html('CrimeLog.html')
crime_df = crime_pdf[0]

# SUMMARIZE DATA BEFORE PROCESSING
print('----------Data before processing----------')
print(crime_df.head(5))
print(crime_df.info())

# DATA PROCESSING AND INFORMATION GATHERING
# Shorten location names
def short_loc(loc):
    return re.sub('Residence Hall', 'Res. Hall', loc)
crime_df['Location'] = crime_df['Location'].apply(short_loc)

# Use synopsis to make a column naming specific crimes
def label_crime(desc):
    for crime in crime_dict:
        if all(word in desc for word in crime_dict[crime]): # Find matching words from the dict in crime desc 
            return crime[:-1]
    print('\nWARNING : UNDEFINED SYNOPSIS\n', desc) # Iterated thru whole dict w/ no return
    return 'UNDEFINED'
crime_df['Crime'] = crime_df['Synopsis'].apply(label_crime)

disp_counts = crime_df['Disposition'].value_counts()
loc_arrest_count = crime_df[crime_df['Disposition'] == "Cleared By Arrest"]['Location'].value_counts()
inactive_crime_count = crime_df[crime_df['Disposition'] == "Open Inactive"]['Crime'].value_counts()

arrest_crime_count = crime_df[crime_df['Disposition'] == "Cleared By Arrest"]['Crime'].value_counts()
defined_crime_count = crime_df[crime_df['Crime'] != 'UNDEFINED']['Crime'].value_counts()
loc_bike_theft_count = crime_df[crime_df['Crime'] == 'Bike theft']['Location'].value_counts()
bike_theft_disp_count = crime_df[crime_df['Crime'] == 'Bike theft']['Disposition'].value_counts()
loc_general_theft_count = crime_df[crime_df['Crime'] == 'General theft']['Location'].value_counts()

# SUMMARIZE AND EXPORT DATA POST PROCESSING
print('\n----------Data post processing----------')
print(crime_df.head(5))
print(crime_df.info())
print('Crime value counts :\n', crime_df['Crime'].value_counts())
crime_df.to_csv('CrimeLog.csv', index=False)

# INFORMATION DISPLAY
title_bp = 'from TTUPD Crime Log, 09/01/2020 - ' + crime_df['Date and Time Reported'][0].split()[0]

# Graph locations and their ammount of arrests on bar graph
fig = plt.figure()
loc_arrest_count[loc_arrest_count > 1].plot(kind='bar', color='orange')
plt.title('Locations w/ More Than 1 Arrest ' + title_bp)
plt.xlabel('Location')
plt.ylabel('Arrests')
plt.xticks(rotation=45, ha='right')
plt.yticks(range(0, loc_arrest_count[0]+1, 2))
fig.set_size_inches(15, 7)
plt.tight_layout()
plt.savefig('location_arrests_counts.jpg', dpi=300)

# Graph all crimes on a bar graph
fig = plt.figure()
defined_crime_count.plot(kind='barh', color='purple')
plt.title('Type of Reports ' + title_bp)
plt.xlabel('Occurences')
plt.ylabel('Type of Report')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('crime_counts.jpg', dpi=300)

# Graph all dispositions on a pie chart 
fig = plt.figure()
disp_counts[disp_counts > 5].plot(kind='pie', autopct='%1.1f%%')
plt.title('Dispositions of Reports (> 5) ' + title_bp)
plt.xlabel('')
plt.ylabel('')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('disposition_counts.jpg', dpi=300)

# Graph locations of all bike thefts
fig = plt.figure()
loc_bike_theft_count.plot(kind='bar', color='red')
plt.title('Location of Bike Thefts ' + title_bp)
plt.xlabel('Location')
plt.ylabel('Bike thefts')
plt.xticks(rotation=45, ha='right')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('bike_theft_location_counts.jpg', dpi=300)

# Graph locations of all bike thefts
fig = plt.figure()
bike_theft_disp_count[bike_theft_disp_count > 5].plot(kind='pie', autopct='%1.1f%%')
plt.title('Disposition of Bike Thefts (> 5) ' + title_bp)
plt.xlabel('')
plt.ylabel('')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('bike_theft_disposition_counts.jpg', dpi=300)

# Graph locations of general thefts 
fig = plt.figure()
loc_general_theft_count.plot(kind='bar', color='red')
plt.title('Location of General Thefts ' + title_bp)
plt.xlabel('Location')
plt.ylabel('Thefts')
plt.xticks(rotation=45, ha='right')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('general_theft_location_counts.jpg', dpi=300)

# Graph crimes of arrested dispositions
fig = plt.figure()
arrest_crime_count.plot(kind='bar', color='red')
plt.title('Crimes of Arrests ' + title_bp)
plt.xlabel('Crime')
plt.ylabel('Arrest')
plt.xticks(rotation=45, ha='right')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('arrest_crime_counts.jpg', dpi=300)

# Graph crimes of open inactive dispositions 
fig = plt.figure()
loc_general_theft_count.plot(kind='bar', color='red')
plt.title('Crimes of Inactive Dispositiosn ' + title_bp)
plt.xlabel('Crime')
plt.ylabel('')
plt.xticks(rotation=45, ha='right')
fig.set_size_inches(15,7)
plt.tight_layout()
plt.savefig('general_theft_location_counts.jpg', dpi=300)



