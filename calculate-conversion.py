#!/usr/bin/env python

import sys
from pathlib import Path

def print_usage():
    print('Usage: calculate-conversion.py <directory with spectra> <calibration file>')

def parse_spectrum(filepath):
    print('processing file:', file.resolve())
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
else:
    print_usage()
    quit()
