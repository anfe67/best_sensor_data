# best_sensor_data

You have a distance sensor HC-SR04 and a series of distance observations, assuming the target does not move you want to establish the best or most correct measure.
The particular sensor used is a HC-SR04, of which an analysis of the accuracy and performances is presented [here:] (https://app.box.com/s/sj7du1n32in2777rcoi2) in the analysis, as I do not have any specific data about the conditions in which the data is aquired, accuracy of the sensor and conditions, I simply try to skim the data removing the observations that diverge from a central cluster. Accuracy, skew of the sensors used etc should be in reality assessed, so that the data could be normalised before applying my approach.  [Here an article on the sensor and how to use with Arduino] (https://randomnerdtutorials.com/complete-guide-for-ultrasonic-sensor-hc-sr04/), and [here](http://apprenons-python.c1.biz/2018/06/09/hc-sr04-capteur-de-distance/) you can find one of my articles on how to use it with the Raspberry Pi (In French) 

## Analysis - Data Exploration and Cleaning

I tried to establish a statistical method, by executing an exploratory analysis, this is collected in the funciton **analyse_data**. 
I used two methods to find the outliers: 

* Take out the observations that are not within 3*SD from the mean 
* Take out the observations that are bigger than 1.5* Inter-Quartile-Range + Third Quartile value or lower than First Quartile value -  1.5* Inter-Quartile-Range

## Conclusion
I verified the two methods with a barplot and a boxplot, the first method did not remove enough "polluted" values as it removed only two observations and the 
the average was biased towards the lower outliers. In my opinion the median represented the "good measure" better than the mean, so I used the second method. 
The result is in the function **find_measure**. As I was lazy and did not want to use numpy, I also wrote **quartile** to find the median, Q1, Q3 and teh IQR. 
