Install python 3.6.5

Check to see below network share folder and all sub folders is available from your machine:

\\gscfile01\SharedFile\QA_MVC

1:
Edit and save 'config.json' based on your env and target date. Date format used is DDMMMYY example: 07JUN18 (must be uppercase).

2:
Open command line and run 'python req.py'. It will take 90 min to finish.

3:
Login to Movement Control see if any flight got missed. If missed fill out OUT OFF ON IN for those flights manually.
This is to ensure every delayed flight have their previous flight OUT OFF ON IN time filled.

4:
Run 'python filter.py'
Once finished your data should be available in 'filtered_data' folder with the name 'filtered.csv'
Save that file as xslx file.

