import sys
sys.path.append("..")

from optparse import OptionParser
from fob import FobStream
from numpy import array, c_

def buildCols():
    """Build columns of signal data in the following format:
    [ x<sensor-id> y<sensor-id> z<sensor-id> x<sensor-id2> ... ]
    """
    
def parseData(infile, numSensors):
    """Parse out the x, y, z signals for each sensor.

    Returns a list of signal tuples, grouped by sensor.

    Example:

    [[(x1,y1,z1),(x2,y2,z2)...],  # sensor 1
    [(x1,y1,z1),(x2,y2,z2)...],   # sensor 2
    ...]                          # sensor n
    """
    fs = FobStream(infile, numSensors)

    sensorDataLines = [[] for i in range(numSensors)]
    for momentData in fs:
        for i in range(numSensors):
            sensorDataLines[i].append(momentData[i])

    def __parseData(lines):
        """Parse lines containing data for a single sensor.
        """
        return [tuple([float(val) for val in line.split()[1:4]]) for line in lines]
            
    return [__parseData(lines) for lines in sensorDataLines]        

def formatData(parsedData):
    """Put data parsed by the parseData function in a nice format.

    Format is column-oriented, and ordered by sensor and axis.

    Dimensions of returned array or as such:
    result[sensor, moment, axis]
    """
    def __formatData(sensorData):
        """Format data for a single sensor.
        """
        xs = [item[0] for item in sensorData]
        ys = [item[1] for item in sensorData]
        zs = [item[2] for item in sensorData]

        return c_[xs, ys, zs]

    return c_[[__formatData(sensorData) for sensorData in parsedData]]

def main(argv=None):
    if argv == None:
        argv = sys.argv

    usage = "usage: %prog [options] inputfile num_sensors outputfile"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    (infile, numSensors, outfile) = args
    numSensors = int(numSensors)

    # Read in sensor data
    sensorData = parseData(infile, numSensors)

    # Get it into a nice linear algebra form
    data = formatData(sensorData)


if __name__ == "__main__":
    sys.exit(main())