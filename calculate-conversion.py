#!/usr/bin/env python

import sys
from pathlib import Path

flowRateHe = 30
initFlowRateCO = 2
initFlowRateO2 = 4

def print_usage():
    print('Usage: calculate-conversion.py <directory with spectra> <calibration file>')

def parse_spectrum(filepath):
    print('processing file:', filepath.resolve())
    with filepath.open() as filehandler:
        for line in filehandler:
            if 'Time	Time Relative [s]	T [°C]	Time	Time Relative [s]	Pressure [mbar]' in line:
                nextline = filehandler.readline()
                temperature = float(nextline.split('\t')[2])
                pressure = float(nextline.split('\t')[5])
                print('temperature:', temperature)
                print('pressure:', pressure)
            if 'Mass [amu]	Ion Current [A]' in line:
                nextline = filehandler.readline()
                m = list()
                ic_rel = list()
                while nextline.strip():
                    m.append(float(nextline.split('\t')[0]))
                    ic_rel.append(float(nextline.split('\t')[1]) / pressure)
                    nextline = filehandler.readline()
                print('# of ion current vs m/q pairs:', len(m))
                break
    return [temperature, m, ic_rel]

def find_const_baseline(i):
    print('function find_const_baseline is not finished!')
    return 0.00001

def find_CO2_concentration(m, icRel, mCal, icRelCal, flowRateHe, initFlowRateCO, initFlowRateO2):
    iBaseCal = find_const_baseline(icRelCal)
    iCO2Cal = icRelCal[mCal.index(44)]
    iBase = find_const_baseline(icRel)
    iCO2 = icRel[m.index(44)]
    xCO2Cal = initFlowRateCO / sum([initFlowRateCO, initFlowRateO2, flowRateHe]) # assumption: calibration was done with the same flow rates as catalytic activity measurement experiment
    xCO2 = xCO2Cal * (iCO2 - iBase) / (iCO2Cal - iBaseCal)
    print('xCO2 = ', xCO2)
    return xCO2

def find_conversion(flowRateHe, initFlowRateCO, initFlowRateO2, specdata, caldata):
    conversionData = list()
    for spectrum in specdata:
        CO2_concentration = find_CO2_concentration(m = spectrum[1], icRel = spectrum[2], mCal = caldata[1], icRelCal = caldata[2], flowRateHe = flowRateHe, initFlowRateCO = initFlowRateCO, initFlowRateO2 = initFlowRateO2)
        totalInitFlowRate= sum([flowRateHe, initFlowRateCO, initFlowRateO2])
        conversion = (CO2_concentration * totalInitFlowRate / initFlowRateCO) * (1 / (1 + CO2_concentration / 2))
        conversionData.append([spectrum[0], conversion])
    return conversionData

try:
    specdir = Path(sys.argv[1])
    calfile = Path(sys.argv[2])
except:
    print_usage()
    quit()

if specdir.is_dir() and calfile.is_file():
    print('calculating conversion vs. temperature using files in:', specdir.resolve())
    specdata = list()
    for file in specdir.iterdir():
        if file.is_file():
            specdata.append(parse_spectrum(file))
    print('parsed data length:', len(specdata))
    caldata = parse_spectrum(calfile)
    conversion = find_conversion(flowRateHe, initFlowRateCO, initFlowRateO2, specdata, caldata)
    print('conversion:\n', conversion)
else:
    print_usage()
    quit()
