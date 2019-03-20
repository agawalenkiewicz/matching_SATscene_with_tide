# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 15:19:38 2018

@author: mp877190
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import re
import pandas as pd
from datetime import timedelta
from datetime import datetime
from scipy import interpolate

import scipy.optimize
import matplotlib.patches as patches



file = sys.argv[1] #'M://getting_netcdf/tide_tables/tidetable_Heysham/2016HEY.txt' 

#read in the txt file and split the lines based on tabular spaces
f = open(file)

F = []

for line in f:
    x = line.split()
    F.append(x)

# cut off the first 10 lines (not relevant) and last line (empty)
F = F[11::]
F = F[:-1]


# take 4th column for tide values
# using regular expressions extract only numerical values and leave the letters
# this is still a string and needs to be converted to float
tide = [y[3] for y in F]
#print(tide)

tide_values = []
"""
for i in tide:
    value = re.findall(r"[+-]?\d+(?:\.\d+)", i)
    #value = i.replace('M','')
    value = np.float(value[0].strip().strip("'"))
    tide_values.append(value)
"""    
#print("tide values" , tide_values)


# take 2nd (yyyy/mm/dd) and 3rd (hh:mm:ss) column for time values
# using regular expressions extract only numerical values and leave the letters
# this is still a string and needs to be converted to float
time =[y[1]+' '+y[2] for y in F]

time_values = []
"""
for i in time:
    my_calendardate = re.findall(r'[12][0-9][0-9][0-9]/[01][0-9]/[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]' , i)
    #my_clock = re.findall(r'[0-2][0-9]:[0-5][0-9]:[0-5][0-9]' , i)
    #print(my_calendardate)
    #print(my_clock)
    dated = datetime.strptime(my_calendardate[0], '%Y/%m/%d %H:%M:%S')
    day = dated.timetuple()
    doy = day.tm_yday
    #print(day)
    time_values.append(dated)
"""


measurements = [y[1]+' '+y[2] + ' , '+y[3] for y in F]
valid_data = []
valid_time = []
TEXTO = str(sys.argv[2])
#print(TEXTO)
#regex = re.escape(TEXTO) + r" [0-2][0-9]:[0-5][0-9]:[0-5][0-9] , [+-]?\d+(?:\.\d+)" #r"2016/10/1[6-8] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] , [+-]?\d+(?:\.\d+)"
regex = r"{0} [0-2][0-9]:[0-5][0-9]:[0-5][0-9] , [+-]?\d+(?:\.\d+)".format(TEXTO)
#print (regex)
test_str = str(measurements)
#print(test_str)
matches = re.finditer(regex, test_str, re.MULTILINE)
#matches = re.findall(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1
    matching = match.group()
    valid_day, valid_height = map(str,matching.split(','))
    valid_data.append(valid_height)
    valid_time.append(valid_day)
    #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    #for groupNum in range(0, len(match.groups())):
        #groupNum = groupNum + 1
        
        #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

for i in valid_data:
    value = re.findall(r"[+-]?\d+(?:\.\d+)", i)
    #value = i.replace('M','')
    value = np.float(value[0].strip().strip("'"))
    tide_values.append(value)
    
for i in valid_time:
    my_calendardate = re.findall(r'[12][0-9][0-9][0-9]/[01][0-9]/[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]' , i)
    #my_clock = re.findall(r'[0-2][0-9]:[0-5][0-9]:[0-5][0-9]' , i)
    #print(my_calendardate)
    #print(my_clock)
    dated = datetime.strptime(my_calendardate[0], '%Y/%m/%d %H:%M:%S')
    day = dated.timetuple()
    doy = day.tm_yday
    #print(day)
    time_values.append(dated)


#print(time_values)   
#print(tide_values)


time = str(sys.argv[2] + ' ' + sys.argv[3]) #'2016/10/16 10:46:34'
time = str(time[:-1])
#print("this is the time" , time)
a_dated_time = datetime.strptime(time, '%Y/%m/%d %H:%M:%S')

dated_time = a_dated_time
#is dated time only for Sizewell --> because we're using Lowersoft and moving phase by 55 minutes
#dated_time = a_dated_time - timedelta(0,3327)  # days, seconds, then other fields.
"""
fig = plt.figure()
fig.set_size_inches((10,5))
ax = plt.subplot(111)
ax.plot(time_values, tide_values, label='from tide tables')
plt.axvline(dated_time,c='r' , label='from Landsat scene')
#plt.title('Tides for Sizewell on day ' + str(dated_time))
#plt.ylim(1,6)
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#plt.savefig('M://getting_netcdf/tide_tables/Sizewell_tide_graph/Sizewell_19122017.png')
"""

closest = min(time_values, key=lambda d: abs(d - dated_time))
#print('closest time' , closest)



##################################################
closest_idx = time_values.index(closest)
#print('closest index' , closest_idx)
tide_values_avg = np.mean(tide_values) #average of the constituent
tide_amplitude = tide_values - tide_values_avg #amplitude of the constituent

#print('time values' , time_values)
#print('tide values' , tide_values)
#print('tide amplitude' , tide_amplitude)

time_delta = [(time_values[i] - time_values[0]).seconds for i in range(0,len(time_values))]
#print('number of data points' , len(time_delta)) # number of data points





def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess,popt,pcov)}



tt = np.linspace(0, 24, len(time_delta)) #np.linspace(0, 10, N)
#print(len(tt))
yynoise = tide_amplitude

res = fit_sin(tt, yynoise)
#print( "Amplitude=%(amp)s, Angular freq.=%(omega)s, Period=%(period)s, phase=%(phase)s, offset=%(offset)s, Max. Cov.=%(maxcov)s" % res )


constant = res["offset"]
amplitude = res["amp"]
alpha = res["phase"]
frequency = res["freq"]
time = tt

#print(constant, amplitude, alpha)
#print(tt[closest_idx])

phase = ( 2. * np.pi * frequency * tt[closest_idx] ) + alpha
#print(phase)
while phase > (2. * np.pi):
    phase = phase - (2. * np.pi)
if amplitude < 0 :
    phase = phase - (np.pi)

#print("phase of this tide is" , phase , "rad")
phase_deg = phase * 180. / np.pi
if phase_deg < 0.:
	phase_deg = phase_deg + 360.


if 90. < phase_deg < 270. :
	print('ebb')
	#change name of file (add underscore 'ebb')
if 0. < phase_deg < 90. :
	print('flood')
	#change name of file (add underscore 'flood')
if 270. < phase_deg < 360. :
	print('flood')
	#change name of file (add underscore 'flood')
"""
phase_in_image_name = str(phase_deg).replace('.', '_')
date_in_image_name = str(TEXTO).replace('/','')

fig2 = plt.figure()

plt.plot(tt, yynoise, "ok", label="tide data")
plt.plot(tt, res["fitfunc"](tt), "r-", label="sine fit curve", linewidth=2)
plt.axvline(tt[closest_idx], c='b')
#plt.axvline(24.1)
plt.legend(loc="best")
#plt.text(150, 2.5, r'phase (deg)=%d' %tt[closest_idx])
textstr = 'phase of this tide \n is {:.2f} degrees'.format(phase_deg) #.format(phase * 180. / np.pi)
#plt.text(0.02, 0.5, textstr, fontsize=14, transform=plt.gcf().transFigure)
#plt.gcf().text(0.02, 0.5, textstr, fontsize=12)
#plt.subplots_adjust(left=0.25)

plt.title('Torness, '+ str(a_dated_time) +'\n phase of this tide is {:.2f} degrees'.format(phase_deg)) #(phase * 180. / np.pi))
plt.xlabel('hours')
plt.ylabel('height amplitude')
#plt.show()
plt.savefig('/home/users/mp877190/getting_netcdf/tide_tables/Torness_tide_graph/Torness_'+str(phase_in_image_name)+'__'+str(date_in_image_name)+'.png')
"""