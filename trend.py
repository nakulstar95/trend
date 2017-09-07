
def trend(x, y, neutpc, limitpc, name, trendSpeakthresh, errIncDecAngle) :
    
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    import seaborn as sns

# calculating values which are part of simple statements
    x = pd.Series(x)
    avg = x.mean()
    minVal = x.min()
    maxVal = x.max()
    
# values at the start and end of the series
    timeStartVal = x[0]
    timeEndVal = x[len(x)-1]
    
# will give the location of the points which have the highest and lowest values
    maxValIndices = [i for i, z in enumerate(x) if z == maxVal]
    minValIndices = [i for i, z in enumerate(x) if z == minVal]
    
# will give the percentage change when compared with the starting value and also when compared with the previous value
    chngWRTtimeStart = (timeEndVal-timeStartVal)/abs(timeStartVal) * 100
    chngWRTPrev = (timeEndVal-x[len(x)-2])/abs(x[len(x)-2]) * 100
    
# will calculate the change percentage for every value
    chngPcList = [((x[i]-x[i-1])/abs(x[i-1]) * 100) for i in np.arange(1,len(x))]
    
# will extract the location(indices) of the points which have the maximum and minimum percentage change
    minChngPcVal = pd.Series(chngPcList).min()
    maxChngPcVal = pd.Series(chngPcList).max()    
    minChngPcIndex = [(i+1) for i, z in enumerate(chngPcList) if z == minChngPcVal]
    maxChngPcIndex = [(i+1) for i, z in enumerate(chngPcList) if z == maxChngPcVal]
    
# will extract the location(indices) of the points which have the maximum and minimum Absolute change   
    chngAbsList = [(x[i]-x[i-1]) for i in np.arange(1,len(x))]
    minChngAbsVal = pd.Series(chngAbsList).min()
    maxChngAbsVal = pd.Series(chngAbsList).max()
    minChngAbsIndex = [(i+1) for i, z in enumerate(chngAbsList) if z == minChngAbsVal]
    maxChngAbsIndex = [(i+1) for i, z in enumerate(chngAbsList) if z == maxChngAbsVal]
    
#     print("minChngPcIndex :", minChngPcIndex)
#     print("maxChngPcIndex :",maxChngPcIndex)
    
# Finding the data points where the change was higher than the limit input (positive and negative peaks)
    positivePeakLoc = []
    negativePeakLoc = []

# This loop will go through the values in the value list x and check for negative and positive peaks
# and append them to the positivePeakLoc and negativePeakLoc lists
# The check is different for the first value, last value and all the the other values
# The first value isn't considered as a negative/positive peak if the next value is a peak. 
# The first 'if' statement in the first condition takes care about that
# The last value however will be considered as a positive/negative peak even if the previous value was a peak
# the reason for that is one needs to have an idea about the status of the most recent value compared to the previous value
# The last condition takes care about the peaks for the values other than the first and last values
# Note: This isn't the peak locator code used previously which was based on the signal processing logic

    for i,j in enumerate(x):
        if i == 0:
            if (abs(x[i]-x[i+1])/x[i]*100 > limitpc):
                if ((abs(x[i+1] - x[i])/x[i])*100 > limitpc) & ((abs(x[i+1] - x[i+2])/x[i+1])*100 > limitpc) & ((x[i+1] - x[i])*(x[i+1] - x[i+2]) > 0):
                    continue
                elif (x[i]-x[i+1] > 0):
                    positivePeakLoc.append(i)
                else:
                    negativePeakLoc.append(i)
        elif i == len(x)-1:
            if (abs(x[i]-x[i-1])/x[i]*100 > limitpc):
                if (x[i]-x[i-1] > 0):
                    positivePeakLoc.append(i)
                else:
                    negativePeakLoc.append(i)
        else:
            if ((abs(x[i] - x[i-1])/x[i-1])*100 > limitpc) & ((abs(x[i] - x[i+1])/x[i-1])*100 > limitpc) & ((x[i] - x[i-1])*(x[i] - x[i+1]) > 0):
                if (x[i]-x[i-1] > 0):
                    positivePeakLoc.append(i)
                else:
                    negativePeakLoc.append(i)
                    
# Peak logic ends here
    
# Getting the indices of the list where the values are increasing, decreasing and neutral
# Every value is compared with the previous value to mark it as increased(1), decreased(-1) or neutral(0) accordingly
# thus the trendmarker is the list which is shorter than the original value list by one

    trendMarker = []
    for i in np.arange(1,len(x)):
        if (x[i] - x[i-1])/abs(x[i])*100 > neutpc:
            trendMarker.append(1)
        elif(x[i] - x[i-1])/abs(x[i])*100 < -neutpc:
            trendMarker.append(-1)
        else:
            trendMarker.append(0)  

# incIndices, decIndices and neutralIndices are lists of lists
# a typical output can be as follows
# suppose the value list of 12 values has the trendmarker list as trendmarker = [1,1,1,1,1,0,0,1,-1,1,0]
# incIndices = [[1,2,3,4,5],[8],[10]]
# decIndices = [[9]]
# neutralIndices = [[6,7],[11]]
# The code below does the above mentioned stuff
# I admit that the the code below can be improved in terms of readability

    incIndices = []
    decIndices = []
    neutralIndices = []
    a = []

    for i,j in enumerate(trendMarker):
        if i == 0:
            a.append(i+1)
            continue

        elif (i == (len(trendMarker)-1))&(trendMarker[i] == trendMarker[i-1]):
            a.append(i+1)
            if trendMarker[i-1] == 1:
                incIndices.append(a)
                a = [i+1]
            elif trendMarker[i-1] == -1:
                decIndices.append(a)
                a = [i+1]
            else:
                neutralIndices.append(a)
                a=[i+1]    

        elif (i == (len(trendMarker)-1)):
            if trendMarker[i-1] == 1:
                incIndices.append(a)
                a = [i+1]
            elif trendMarker[i-1] == -1:
                decIndices.append(a)
                a = [i+1]
            else:
                neutralIndices.append(a)
                a=[i+1]
            
            a = []
            a.append(i+1)
            if trendMarker[i] == 1:
                incIndices.append(a)
            elif trendMarker[i] == -1:
                decIndices.append(a)
            else:
                neutralIndices.append(a)

        elif trendMarker[i] == trendMarker[i-1]:
            a.append(i+1)

        else:
            if trendMarker[i-1] == 1:
                incIndices.append(a)
                a = [i+1]
            elif trendMarker[i-1] == -1:
                decIndices.append(a)
                a = [i+1]
            else:
                neutralIndices.append(a)
                a = [i+1]
# the code for getting increasing, decreasing and neutral indices ends here
   
# A few functions below just handle printing the narratives so you guys can give it a miss
# A short brief of the functions is as follows
# 'periodPrinter' will print the periods like "August to December" etc.
# 'many' will handle 'commas' and 'and' [['August'],['October'],['December']] will be "August,October and December"
# The other functions use these two functions and have comments below accordingly

    # function for printing the periods 
    def periodPrinter(x):
        a = []
        for i,j in enumerate(x):
            first = y[j[0]]
            last = y[j[-1]]
            appendThis = first + " to " + last
            a.append(appendThis)
        return a  

    # function for handling 'and'
    def many(y):
        z=""
        if len(y) > 1:            
            for i in range(0,len(y)):
                if i<len(y)-1:
                    z = z +y[i]+", "
                else:
                    z = z[:-2] +" and "+ y[i] 
        else:
            z = y[0]
        return z    
    
    # perfPrint is the function which will make use of both the above functions
    def perfPrint(y):
        return many(periodPrinter(y))
    
    # spike printer function
    def spikePrinter(z):
        a = []
        for i,j in enumerate(z):
            a.append(y[j])
        return a
        
    # perfPrintspike is the function which will make use of the above function and many function
    def perfPrintspike(z):
        return many(spikePrinter(z))
    
    # perfSingPrint will print the singular points in the perfect manner
    def perSingPrint(z):
        a = []
        for i,j in enumerate(z):
            a.append(y[j])
        return many(a)

    # printing statements for testing  
#     print("minimum :",minVal," at ",maxValIndices)
#     print("maximum :",maxVal," at ",minValIndices)
#     print("period start val :",timeStartVal)
#     print("period end val :",timeEndVal)
#     print("Change with respect to the starting value :",chngWRTtimeStart,"%")
#     print("Change with respect to the previous value :",chngWRTPrev,"%")
#     print("The values of Positive peaks are :",list(x[positivePeakLoc]),"at",positivePeakLoc)
#     print("The values of Negative peaks are :",list(x[negativePeakLoc]),"at",negativePeakLoc)
#     print("incIndices: ",incIndices)
#     print("decIndices: ",decIndices)
#     print("neutralIndices :",neutralIndices)
    
    # printing trend sentence
    print("\n")
# trendSpeakerThreshold will be the length of the lists which should be talked about
# if this value comes out to be 4 then all the lists who have lengths greater than or equal to 4 will be talked about
# NOTE: That this won't affect the narration of the peaks because it is done separately 

    trendSpeakerThreshold = np.ceil(trendSpeakthresh*len(x))
    incSpeakingList = []
    decSpeakingList = []
    neutSpeakingList = []
    
    for i in incIndices:
        if len(i) >= trendSpeakerThreshold:
            incSpeakingList.append(i)
    for i in decIndices:
        if len(i) >= trendSpeakerThreshold:
            decSpeakingList.append(i)
    for i in neutralIndices:
        if len(i) >= trendSpeakerThreshold:
            neutSpeakingList.append(i)
            
# We have now got the list of points (incSpeakingList etc.) which need to be talked about
# Now we will divide this list into points which are single and which are part of a trend
# The function below will do it for us
    
    def singlesANDmultiples(x):
        a = []
        b = []
        for i,j in enumerate(x):
            if (len(j) == 1):
                a.append(j)
            else:
                b.append(j)
        return a,b 
    
    # Now let's save those lists using the above function
    incSpeakSing, incSpeakMult = singlesANDmultiples(incSpeakingList)
    decSpeakSing, decSpeakMult = singlesANDmultiples(decSpeakingList)
    neuSpeakSing, neuSpeakMult = singlesANDmultiples(neutSpeakingList)
    
    # Now let's make a list of erratic points, the trendmarker list prepared before will be used here again
    
# The erratic1 list takes trendmarker list and then makes lists wherever the trendmarker is 1,-1,1 etc.

    erratic1 = []
    a = []
    for i,j in enumerate(trendMarker):
        if (i == len(trendMarker)-1) & (len(a) != 0):
            a = [a[0]-1] + a +[a[-1]+1]
            erratic1.append(a)
            continue
        elif (i == len(trendMarker)-1):
            continue
        elif trendMarker[i] * trendMarker[i+1] == -1:
            a.append(i+1)
        elif ((trendMarker[i] * trendMarker[i+1]) != -1) & (len(a) != 0):
            a = [a[0]-1] + a +[a[-1]+1]
            erratic1.append(a)
            a = []       
        else:
            a = []
    
    # now let's clean the erratic1 list by removing the peaks
    peaks2 = []
    peaks2.append(negativePeakLoc)
    peaks2.append(positivePeakLoc)
    
    peaks = []
    
    for i,j in enumerate(peaks2):
        if len(j)==0:
            continue
        else:
            peaks.append(j) 
    
    peaks = [item for sublist in peaks for item in sublist]
    
    erraticNew = []
    for i,j in enumerate(erratic1):
        a = []
        for m,n in enumerate(j):
            if (set([j[m]]).issubset(peaks) == False) & (m == (len(j)-1)):
                a.append(j[m])
                erraticNew.append(a)
            elif (set([j[m]]).issubset(peaks) == False):
                a.append(j[m])
            else:
                erraticNew.append(a)
                a = []
    # cleaning ends here
    
    # getting a final erratic list which
    # The erratic list will only be talked about if its longer than 4    
    
    erratic = []
    for i,j in enumerate(erraticNew):
        if (len(j) >= 4):
            erratic.append(j)         
    
    # Once this is made we will have to check which trends are erratic but increasing, decreasing or neutral
    # It uses the angle errIncDecAngle for doing this
    erraticNoSlope = []
    erraticPositive = []
    erraticNegative = []

    for i,j in enumerate(erratic):
        if ((np.polyfit(np.arange(1,len(erratic[i])),x[erratic[i][1]:erratic[i][-1]+1],1)[0] < math.tan(math.radians(errIncDecAngle))) &
            (np.polyfit(np.arange(1,len(erratic[i])),x[erratic[i][1]:erratic[i][-1]+1],1)[0] > math.tan(math.radians(-errIncDecAngle)))):
            err = j
            erraticNoSlope.append(err)
        elif (np.polyfit(np.arange(1,len(erratic[i])),x[erratic[i][1]:erratic[i][-1]+1],1)[0] > math.tan(math.radians(errIncDecAngle))):
            err = j
            erraticPositive.append(err)
        else:
            err = j
            erraticNegative.append(err)
            
    # Now we will edit those singular lists which were made before to get only those points which aren't in the erratic trend
    def SingInErrCheck(x):
        a = []
        err = []
        for i,j in enumerate(erratic):
            err = err + j

        for i,j in enumerate(x):
            if set(j).issubset(err) == False:
                a.append(j)
        return a
    
    finalSingInc = SingInErrCheck(incSpeakSing)
    finalSingDec = SingInErrCheck(decSpeakSing)
    finalSingNeut = SingInErrCheck(neuSpeakSing)
    
    finalSingInc = [item for sublist in finalSingInc for item in sublist]
    finalSingDec = [item for sublist in finalSingDec for item in sublist]
    finalSingNeut = [item for sublist in finalSingNeut for item in sublist]

    if len(positivePeakLoc) != 0:
        for i,j in enumerate(positivePeakLoc):
            if ((j != 0) & (j != (len(x)-1))):
                if set([j+1]).issubset(finalSingDec):
                    finalSingDec = list(filter((j+1).__ne__, finalSingDec))
                if set([j]).issubset(finalSingInc):
                    finalSingInc = list(filter((j).__ne__, finalSingInc))
            
    
    if len(negativePeakLoc) != 0:
        for i,j in enumerate(negativePeakLoc):
            if ((j != 0) & (j != (len(x)-1))):
                if set([j+1]).issubset(finalSingInc):
                    finalSingInc = list(filter((j+1).__ne__, finalSingInc))
                if set([j]).issubset(finalSingDec):
                    finalSingDec = list(filter((j).__ne__, finalSingDec))

#     print("incSpeakingList :", incSpeakingList)
#     print("decSpeakingList :", decSpeakingList)
#     print("neutSpeakingList :", neutSpeakingList)
#     print("incSpeakSing :",incSpeakSing,"incSpeakMult :",incSpeakMult)
#     print("decSpeakSing :",decSpeakSing,"decSpeakMult :",decSpeakMult)
#     print("neuSpeakSing :",neuSpeakSing,"neuSpeakMult :",neuSpeakMult)
#     print("negativePeak :",negativePeakLoc)
#     print("positivePeak :",positivePeakLoc)
#     print("peaks2 :",peaks2)
#     print("peaks :",peaks)
#     print("erratic1 :",erratic1)
#     print("erraticNew :",erraticNew)
#     print("erratic :",erratic)
#     print("erraticNoSlope :",erraticNoSlope)
#     print("erraticPositive :",erraticPositive)
#     print("erraticNegative :",erraticNegative)
#     print("finalSingInc :",finalSingInc)
#     print("finalSingDec :",finalSingDec)
#     print("finalSingNeut :",finalSingNeut)
    
    
#     print("trendmarker :",trendMarker)
#     print("\n")
#     print("Read the section below \n")
 
    # first sentence
    flag = 0
    
    if (len(incIndices)!= 0) & (len(decIndices) == 0) & (len(neutralIndices) == 0):
        if (len(incIndices[0]) == len(trendMarker)):
            print("The value of",name,"has been increasing throughout the period.")
            flag = 1
        elif (len(decIndices[0]) == len(trendMarker)):
            print("The value of",name,"has been decreasing throughout the period.")
            flag = 1
        elif (len(neutralIndices[0]) == len(trendMarker)):
            print("The value of",name,"has been more or less constant throughout the period.")
            flag = 1
    
    if (flag == 0):
        if len(incSpeakMult) != 0:
            print("The",name,"had been increasing from",perfPrint(incSpeakMult))
            if (len(decSpeakMult) != 0) & (len(neuSpeakMult) != 0):
                print(".It was however decreasing from",perfPrint(decSpeakMult),
                      ", while it remained neutral from",perfPrint(neuSpeakMult))
            elif (len(decSpeakMult) != 0):
                print(", while it was decreasing in the period from",perfPrint(decSpeakMult))
            elif (len(neuSpeakMult) != 0):
                print(", while it was neutral in the period from",perfPrint(neuSpeakMult))
        elif len(decSpeakMult) != 0:
            print("The",name," had been decreasing in the period",perfPrint(decSpeakMult))
            if (len(incSpeakMult) != 0) & (len(neuSpeakMult) != 0):
                print(".It was however increasing in the period",perfPrint(incSpeakMult),
                      ", while it remained neutral in",perfPrint(neuSpeakMult))
            elif (len(incSpeakMult) != 0):
                print(", while it was increasing in the period from",perfPrint(decSpeakMult))
            elif (len(neuSpeakMult) != 0):
                print(", while it was neutral in the period from",perfPrint(neuSpeakMult))
        elif len(neuSpeakMult) != 0:
            print("The",name,"had been neutral in the period",perfPrint(neuSpeakMult))
            if (len(incSpeakMult) != 0) & (len(decSpeakMult) != 0):
                print(".It was however increasing in the period",perfPrint(incSpeakMult),
                      ", while it was decreasing in",perfPrint(decSpeakMult))
            elif (len(incSpeakMult) != 0):
                print(", while it was increasing in the period from",perfPrint(decSpeakMult))
            elif (len(decSpeakMult) != 0):
                print(", while it was decreasing in the period from",perfPrint(neuSpeakMult))
    
    
    # second sentence
    if (flag == 0):
        if len(erraticNoSlope) != 0:
            
            print("It displayed an erratic trend from",perfPrint(erraticNoSlope))
            
            if (len(erraticPositive) != 0) & (len(erraticNegative) != 0):               
                print(".Though the",name,"were erratic from",perfPrint(erraticPositive),
                      ", it showed an overall increasing trend during", 
                      ("this period" if len(erraticPositive) == 1 else "these periods"),                 
                      ". It was also erratic with a decreasing trend from",perfPrint(erraticNegative))
            
            elif (len(erraticPositive) != 0):
                print(".Though it was also erratic from",perfPrint(erraticPositive),
                      ", it showed an overall increasing trend during ", 
                      ("this period." if len(erraticPositive) == 1 else "these periods."))
                      
            elif (len(erraticNegative) != 0):
                print(".Though it was also erratic from",perfPrint(erraticNegative),
                      ", it showed an overall decreasing trend during ",
                      ("this period." if len(erraticNegative) == 1 else "these periods."))

        elif len(erraticPositive) != 0:
            
            print("It displayed an erratic but increasing trend from",perfPrint(erraticPositive))
            
            if (len(erraticNoSlope) != 0) & (len(erraticNegative) != 0):               
                print(".It was erratic from",perfPrint(erraticNoSlope),
                      ".Though it was also erratic from",perfPrint(erraticPositive),
                      ", it showed an overall decreasing trend during ", 
                      ("this period." if len(erraticPositive) == 1 else "these periods."))                      
            
            elif (len(erraticNoSlope) != 0):
                print(".It was erratic from",perfPrint(erraticNoSlope))
                      
            elif (len(erraticNegative) != 0):
                print(".Though it was also erratic from",perfPrint(erraticNegative),
                      ", it showed an overall decreasing trend during ",
                      ("this period." if len(erraticNegative) == 1 else "these periods."))
    
        elif len(erraticNegative) != 0:
            
            print("It displayed an erratic but decreasing trend from",perfPrint(erraticNegative))
            
            if (len(erraticNoSlope) != 0) & (len(erraticPositive) != 0):               
                print(".It was erratic from",perfPrint(erraticNoSlope),
                      ".Though it was also erratic from",perfPrint(erraticPositive),
                      ", it showed an overall increasing trend during ", 
                      ("this period." if len(erraticPositive) == 1 else "these periods."))                      
            
            elif (len(erraticNoSlope) != 0):
                print(".It was erratic from",perfPrint(erraticNoSlope))
                      
            elif (len(erraticPositive) != 0):
                print(".Though it was also erratic from",perfPrint(erraticPositive),
                      ", it showed an overall increasing trend during ",
                      ("this period." if len(erraticPositive) == 1 else "these periods."))
        
    # third sentence
    if (flag == 0):        
        if len(finalSingInc) != 0:
            print("The",name,"increased in",perSingPrint(finalSingInc))
            if (len(finalSingDec) != 0) & (len(finalSingNeut) != 0):
                print(".It however decreased in",perSingPrint(finalSingDec),
                      ", while it displayed no change in",perSingPrint(finalSingNeut))
            elif (len(finalSingDec) != 0):
                print(", while it decreased in",perSingPrint(finalSingDec))
            elif (len(finalSingNeut) != 0):
                print(", while it displayed no change in",perSingPrint(finalSingNeut))
        elif len(finalSingDec) != 0:
            print("The",name," decreased in",perSingPrint(finalSingDec))
            if (len(finalSingInc) != 0) & (len(finalSingNeut) != 0):
                print(".It however increased in",perSingPrint(finalSingInc),
                      ", while it displayed no change in",perSingPrint(finalSingNeut))
            elif (len(finalSingInc) != 0):
                print(", while it increased in ",perSingPrint(finalSingInc))
            elif (len(finalSingNeut) != 0):
                print(", while it displayed no change in",perSingPrint(finalSingNeut))
        elif len(finalSingNeut) != 0:
            print("The",name,"displayed no change in",perSingPrint(finalSingNeut))
            if (len(finalSingInc) != 0) & (len(finalSingDec) != 0):
                print(".It however increased in",perSingPrint(finalSingInc),
                      ", while decreased in",perSingPrint(finalSingDec))
            elif (len(finalSingInc) != 0):
                print(", while it increased in",perSingPrint(finalSingInc))
            elif (len(finalSingDec) != 0):
                print(", while it decreased in",perSingPrint(finalSingDec))
    
    # fourth sentence
    if len(positivePeakLoc) != 0:
        print("It showed a spike in",perfPrintspike(positivePeakLoc))
        if len(negativePeakLoc) != 0:
            print(", while there was a drop in the same in",perfPrintspike(negativePeakLoc))
    elif len(negativePeakLoc) != 0:
        print("It plummeted in",perfPrintspike(negativePeakLoc))
        if len(positivePeakLoc) != 0:
            print(", while there was a spike in the same in",perfPrintspike(positivePeakLoc))

#     statements
#     print("\n")
#     print("Section below under progress needs refinement and stuff \n")
     
#     # 1
#     print("The Avg",name,"was",avg,"across all",len(x),"entities.")
    
    
#     # Refine these statements, at this moment it's just a placeholder
#     # 2
#     if (len(minChngPcIndex) == 1):
#         print("Largest single decrease in percentage basis occured in",perfPrintspike(minChngPcIndex),
#               "(",minChngPcVal,"%). The largest single decline on an absolute basis occured in",
#               perfPrintspike(minChngAbsIndex),"(",minChngAbsVal,").")
    
#     # 3
#     if (len(maxChngPcIndex) == 1):
#         print("Largest single increase in percentage basis occured in",perfPrintspike(maxChngPcIndex),
#               "(",maxChngPcVal,"%). The largest single rise on an absolute basis occured in",
#               perfPrintspike(maxChngAbsIndex),"(",maxChngAbsVal,").") 

    
    plt.plot(x)
    plt.ylabel("Values")
    plt.xlabel("Time")
    plt.plot(positivePeakLoc,list(x[positivePeakLoc]),'go')
    plt.plot(negativePeakLoc,list(x[negativePeakLoc]),'ro')
    
