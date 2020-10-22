# best_sensor_data

You have a distance sensor HC-SR04 and a series of distance observations, assuming the target does not move you want to establish the best or most correct measure.

## Analysis 

I tried to establish a statistical method, by executing an exploratory analysis, this is collected in the funciton **analyse_data**. 
I used two methods to find the outliers: 

* Take out the observations that are not within 3*SD from the mean 
* Take out the observations that are bigger than 1.5* Inter-Quartile-Range + Third Quartile value or lower than First Quartile value -  1.5* Inter-Quartile-Range

## Conclusion
I verified the two methods with a barplot and a boxplot, the first method did not remove enough "polluted" values as it removed only two observations and the 
the average was biased towards the lower outliers. In my opinion the median represented the "good measure" better than the mean, so I used the second method. 
The result is in the function **find_measure**. As I was lazy and did not want to use numpy, I also wrote **quartile** to find the median, Q1, Q3 and teh IQR. 
