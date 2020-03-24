import os
from os import listdir
from os.path import isdir, isfile, join
import sys

if len(sys.argv) <3:
    print("BASEDIR and country should be set")
    exit(1)
basedir = sys.argv[1]
country  = sys.argv[2]
path = basedir + "/s/synthea/build/resources/main/modules/"
files = [f for f in listdir(path) if isfile(join(path, f))]

# open file for writing markup file
os.mkdir(basedir + '/s/synthea/output')
os.chdir(basedir + '/s/synthea/output')
file = open("README.md","w") 
file.write("# " + country.upper() + " Download Page #\n")
file.write("Healthcare synthetic dataset for the country of Finland in OMOP CDM 6.0 format.\n\n")

regions = ['Uusimaa']

for region in regions:
    # cleanup previous synthea run
    os.chdir(basedir + '/s/synthea')
    if (isdir('output')):
        if (isdir('output/csv')):
            filesToRemove = [f for f in os.listdir('output/csv')]
            for f in filesToRemove:
                os.remove(os.path.join('output/csv', f))
        if (isdir('output/fhir')):
            filesToRemove = [f for f in os.listdir('output/fhir')]
            for f in filesToRemove:
                os.remove(os.path.join('output/fhir', f))
    # run synthea
    os.system("./run_synthea -p 100 Uusimaa")
    # compress synthea output
    os.chdir(basedir + '/s/synthea/output/csv')
    os.system("gzip *")
    # use real addresses
    os.chdir(basedir + '/s/fi_addresses')
    os.system("ls -al")
    os.chdir(basedir + '/s/ETL-Synthea-Python/python_etl')
    os.system("python real_address_synthea.py")
    # run synthea->omop
    os.chdir(basedir + '/s/ETL-Synthea-Python/python_etl')
    os.system("python synthea_omop.py")
    os.chdir(basedir + '/s/ETL-Synthea-Python/output')
    os.system("zip ../" + country + "_covid19_omop_6.zip *.csv")
    #file.write(module + ": " + synthea_fhir + synthea_csv + omop_cdm531 + omop_cdm6 + "\n\n")
file.close()
