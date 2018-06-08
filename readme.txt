Install python 3.6.5
Install node 8.11
Run command 'npm install' from the main directory of this project

Find out the target date for data extract. All date format used is DDMMMYY example: 07JUN18 (must be uppercase)

Check to see below network share folder is available from your machine:

\\gscfile01\SharedFile\QA_MVC\STG2\adh_receive

1:
In the requests folder step 1 file change the date to previous day of the target date.
This is to ensure all previous flights have OUT OFF ON IN time.
Drop the step 1 file in network share and wait 30 minute.

2:
Change the date in step 2 file to the target date.
This is to ensure all flight for that day has ETD delay of 15 min.
Drop step 2 file in network share and wait 30 minute

3:
Change the date in step 3 file to the target date.
This is to ensure all flights have OUT OFF ON IN time.
Drop step 3 file in network share and wait 30 minute

4:
Check MVT Stage 2 to see if any flight got missed. If missed fill out OUT OFF ON IN for those flights manually.
This is to ensure all flights have OUT OFF ON IN time.

5:
Edit get.py file line 18 set currentDate to target date and save the file.
Run command 'python get.py'
When finished run command 'node filter.js'
Your data should be available in 'filtered_data' folder with the name filtered.csv
Save that file as xslx file 

