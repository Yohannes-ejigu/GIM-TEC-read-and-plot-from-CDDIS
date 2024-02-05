import numpy as np
import pandas as pd

def readTEC(filename, exponent = 0.1):
    """
    Reads TEC data from an IONEX file and returns DataFrames for TEC and RMS values.

    Parameters:
    - filename (str): Path to the IONEX file.

    Returns:
    - tuple[pd.DataFrame, pd.DataFrame]: DataFrames for TEC and RMS values.
    """
    linestring = open(filename, 'r').read()
    LongList = linestring.split('\n')

    start_fill = False
    date = 0
    for i, line in enumerate(LongList):
        splitted = line.split()

        if splitted[-1] in ['DESCRIPTION', 'COMMENT']:
            continue
        elif splitted[-1] == 'FILE' and splitted[-2] == 'IN':
            NumberOfMaps = int(splitted[0])
            continue
        elif splitted[-1] == 'DHGT':
            IonH = float(splitted[0])
            continue
        elif splitted[-1] == 'EXPONENT':
            exponent = 10 ** float(splitted[0])
            continue
        elif splitted[-1] == 'DLAT':
            startLat, endLat, stepLat = map(float, splitted[:3])
            continue
        elif splitted[-1] == 'DLON':
            startLon, endLon, stepLon = map(float, splitted[:3])
            continue
        elif splitted[-1] == 'MAP' and (splitted[-4] + splitted[-2] == 'EPOCHFIRST'):
            startYear, startMonth, startDay = map(int, splitted[:3])
            date = startYear * 366. + startMonth * 31. + startDay
            continue
        elif splitted[0] == 'END' and splitted[2] == 'HEADER':
            break

    NewLongList = LongList[i + 1:]
    lonarray = np.arange(startLon, endLon + stepLon, stepLon)
    latarray = np.arange(startLat, endLat + stepLat, stepLat)
    pointsLon, pointsLat = lonarray.shape[0], latarray.shape[0]
    
    times = np.zeros(NumberOfMaps, dtype='float32')
    TEC = np.zeros((NumberOfMaps, pointsLat, pointsLon))
    RMS = np.zeros((NumberOfMaps, pointsLat, pointsLon))

    for line in NewLongList:
        splitted = line.split()

        if not line:
            break
        elif splitted[-1] == 'MAP' and splitted[-4] == 'START':
            start_fill = True
            fillarray = TEC if splitted[-2] == 'TEC' else (RMS if splitted[-2] == 'RMS' else None)
            mapnr = int(splitted[0]) - 1
            continue
        elif start_fill:
            if splitted[-1] == 'MAP' and splitted[1] == 'END':
                start_fill = False
                continue
            if splitted[-1] == 'MAP' and splitted[-4] == 'EPOCH':
                times[mapnr] = float(splitted[3]) + float(splitted[4]) / 60. + float(splitted[5]) / 3600.
                if (float(splitted[0]) * 366 + float(splitted[1]) * 31 + float(splitted[2])) > date:
                    times[mapnr] += 24.
                continue
            if splitted[-1] == 'LAT/LON1/LON2/DLON/H':
                latidx = np.argmin(np.absolute(latarray - float(line[:8])))
                lonidx = 0
                continue

            datalength = len(splitted)
            fillarray[mapnr, latidx, lonidx:lonidx + datalength] = np.array([float(i) * exponent for i in splitted])
            lonidx += datalength

    df_TEC = pd.DataFrame(data=TEC.reshape(-1, lonarray.shape[0]),
                          index=[np.repeat(times, latarray.shape[0]), np.tile(latarray, times.shape[0])],
                          columns=lonarray)
    df_TECrms = pd.DataFrame(data=RMS.reshape(-1, lonarray.shape[0]),
                             index=[np.repeat(times, latarray.shape[0]), np.tile(latarray, times.shape[0])],
                             columns=lonarray)
    df_TEC.index.names = ["Time", "Lat"]
    df_TECrms.index.names = ["Time", "Lat"]


    return df_TEC, df_TECrms, lonarray, latarray
