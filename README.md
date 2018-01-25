# CAEN-data-analysis-code

Code to convert CAEN raw ADC data to energy deposited in the IIT detector setup (with units of MeV)

The simplest use of this code is: 
    run /pathto/CAENconverter.py                    #To convert binary data to python arrays
    prompt, delayed, subSpec = getArray(dataFile)   #To get the energy deposited in detector in MeV. This creates 3 arrays, 
                                                    #one for the prompt signal, one for the delayed signal, and one for all
    hist(subSpec, bins=500, histtype='step')
