#To plot energy spectra from CAEN binary data
import wavedumpReader
dataFile = wavedumpReader.DataFile('withRAsource.dat') #Replace
#what's in the parenthesis with the file you're analyzing 

def getArrays(dataFile):   #Use the same dataFile defined above
    """A function that returns arrays corresponding the prompt signal, delayed 
    signal, and the full array. It takes as an input 'dataFile', which is the 
    processed data file from the CAEN crate."""
    from numpy import fromfile, dtype #subtract, array
    intList = []
    dataFile.file.seek(0)
    timeList = []
    while True:
        header = fromfile(dataFile.file, dtype='I', count=6)
        if len(header) != 6:
            break
        trace = fromfile(dataFile.file, dtype=dtype('<H'), count=250)
        triggerTime = dataFile.getNextTrigger() #getNextTrigger func defined in
        #wavedumpReader 
        #timetag = fromfile(dataFile.file, dtype=dtype('<H'), count = 6)
        baseline = sum(trace[0:20])/20.
        trace = [x-baseline for x in trace] #subtract(trace, baseline)
        intList.append(-sum(trace))
        timeList.append(triggerTime)
    
    #Replace first and last element in times-stamp array (usually in wrong format)
    timeList[0] = 0.
    timeList[len(timeList)-1] = 0.
    
    ##Check that all values in timeList are floats, otherwise code will fail 
    ##To replace empty values with zeroes calList[calList == ''] = '0.'
    ##To replace last t-stamp with zero timeList[len(timeList)-1] = 0., same for 1st
    
    cal = (14563.1+14666.6)/2      #Calibration coefficient from simulation 
    calList = [x/cal for x in intList] #divide(intList, cal) #Divide by cal to get right energy scale (in MeV)
        
    #Cut events separated by delta(t) > 100 micro sec and save them in 
    #Spectrum arrays
    subSpectrum = []     #All neutron-like events
    promptSpectrum = []  #Prompt events
    delayedSpectrum = [] #Delayed events
    for i in range(len(timeList)-1):
        if abs(timeList[i+1]-timeList[i]) < 100:
            subSpectrum.append(calList[i+1])
            subSpectrum.append(calList[i])
            promptSpectrum.append(calList[i])
            delayedSpectrum.append(calList[i+1])

    #For cutting off events with E < 0.3 MeV        
    #subSpectrum1 = []
    #for i in range(len(timeList)-1):
        #if abs(timeList[i+1]-timeList[i]) < 100 and calList[i] >0.3 and calList[i+1] > 0.3:
            #subSpectrum1.append(calList[i+1])
            #subSpectrum1.append(calList[i])
    return promptSpectrum, delayedSpectrum, subSpectrum, delayedSpectrum

#To plot a histogram: hist(subSpectrum, bins=5 ,histtype='step'); #Plot histogram 
