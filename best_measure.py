""" Explore the data from HC-SR04 sensor observations to select best measure
    NOTE: HC-SR04 is a distance sensor based on ultrasound. The correctness of
    the measure may depend on a number of external factors.
"""

import statistics as stat
import matplotlib.pyplot as plt
from scipy import stats

sensor_data = [66.6, 66.6, 66.7, 67.1, 66.7, 66.7, 66.7, 66.7, 66.6, 66.7, 66.3, 66.7, 66.7, 66.3, 67.1, 66.7, 66.6, 66.2, 66.3, 66.6, 66.3, 66.7, 66.7, 62.5, 66.7, 66.2, 66.6, 66.7, 66.7, 66.7, 67.1, 67.1, 67.1, 66.7, 66.2, 66.7, 64.8, 66.7, 66.7, 67.1, 67.1, 66.7, 66.7, 66.6, 66.7, 66.6, 66.2, 66.6, 67.1, 66.6, 67.1, 66.7, 66.2, 67.5, 66.7, 66.7, 67.1, 66.7, 66.7, 66.3]

def quartile(data):

    """ finds out the Q1, median, Q3 and inter - quartile range an returns them as a tuple """

    data.sort()
    half_list = int(len(data) // 2)
    lower_quartile = stat.median(data[:half_list])
    upper_quartile = stat.median(data[half_list:])
    return (lower_quartile, stat.median(data), upper_quartile, upper_quartile - lower_quartile)

def analyse_data(data):

    """ Brief exploration of the data, to see which value is the most reliable,
        two different strategies for removing outliers, one using zscores and
        the other using the 1*5*IQR strategy. Results and ('dirty data') are compared """

    (lower_quartile, data_median, upper_quartile, iqr) = quartile(data)
    print(lower_quartile, data_median, upper_quartile, iqr)

    print(f"Size {len(data)}")
    print(f"Mean {stat.mean(data)}")
    print(f"Median {stat.median(data)}")
    print(f"Lower Quartile: {lower_quartile}")
    print(f"Upper Quartile: {upper_quartile}")
    print(f"Interquartile Range: {iqr}")

    # Finding frequencies
    freq_dict = {x:data.count(x) for x in data}
    # Now you have categories.
    print(freq_dict)

    # Max distance:
    min_val = min(data)
    max_val = max(data)
    print (f"Max and Min: { max_val}, { min_val }")

    print (f"Max Distance: { max_val-min_val }")
    print(f"Max Distance max from median : {max_val - stat.median(data)}")
    print(f"Max Distance min from median : {min_val - stat.median(data)}")
    print(f"Standard Deviation of data {stat.stdev(data)}")

    # Statistics suggests us that anything beyond a certain number of standard deviations from mean should be
    # considered an outlier
    zscores = abs(stats.zscore(data)) > 2.5
    scored_data = list(zip(data, zscores))
    print(f"Z scores of data {  scored_data }")
    outliers = [k for (k,v) in scored_data if v ]
    print(f"Outliers using zscores * 2.5 * sd (usually is *3 sd *sd) {  outliers }")
    outliers2 = [k for k in data if (k > upper_quartile + 1.5*iqr ) or (k < lower_quartile - 1.5*iqr )]
    print(f"Outliers using IQR {outliers2}")

    # remove outliers IQR
    data_clean = [item for item in data if item not in outliers2]

    # Remove outliers zscores
    data_clean_z = [item for item in data if item not in outliers]

    # And again
    print(f"Size {len(data_clean)}")
    print(f"Mean {stat.mean(data_clean)}")
    print(f"Median {stat.median(data_clean)}")

    min_val = min(data_clean)
    max_val = max(data_clean)
    print (f"Max and Min: { max_val}, { min_val }")

    print (f"Max Distance: { max_val-min_val }")
    print(f"Max Distance max from median : {max_val - stat.median(data_clean)}")
    print(f"Max Distance min from median : {min_val - stat.median(data_clean)}")
    print(f"Standard Deviation of data {stat.stdev(data_clean)}")
    zscores_clean = abs(stats.zscore(data_clean)) > 2.5
    scored_data_clean = list(zip(data, zscores_clean))
    print(f"Z scores of CLEAN data {  scored_data_clean }")

    freq_dict_clean = {x:data_clean.count(x) for x in data_clean}
    freq_dict_clean_z = {x:data_clean_z.count(x) for x in data_clean_z}


    # Three figures, one with the raw data, and one for each strategy

    f, ax = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.25, .75)})
    ax[0].boxplot(data, notch= True, patch_artist=True, vert=False)
    ax[1].bar(freq_dict.keys(), freq_dict.values(), edgecolor='black')
    ax[1].set(xlabel="Raw sensor data")

    f1, ax1 = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.25, .75)})

    ax1[0].boxplot(data_clean, notch= True, patch_artist=True, vert=False)
    ax1[1].bar(freq_dict_clean.keys(), freq_dict_clean.values(), edgecolor='black')
    ax1[1].set(xlabel="Sensor data with outliers removed (IQR Method")

    f2, ax2 = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.25, .75)})

    ax2[0].boxplot(data_clean_z, notch= True, patch_artist=True, vert=False)
    ax2[1].bar(freq_dict_clean_z.keys(), freq_dict_clean_z.values(), edgecolor='black')
    ax2[1].set(xlabel="Sensor data with outliers removed (zscores)")

    plt.show()


    # other factors may be taken into account :
    # if the measurement with the maximum frequency represents less than 50% of the observations,
    # then take it, if not group the max freqs until more than 50% and take average


def find_measure(data):

    """ Based on the exploratory data analysis the data above
        a simple algorithm that removes the outliers in accordance with the
        1.5 * inter-quartile range rule """

    (lower_quartile, data_median, upper_quartile, iqr) = quartile(data)
    outliers = [k for k in data if (k > upper_quartile + 1.5 * iqr) or (k < lower_quartile - 1.5 * iqr)]
    data_clean = [item for item in data if item not in outliers]

    # Either return the mean or the median
    return stat.mean(data_clean)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Uncomment here below to show the data analysis
    analyse_data(sensor_data)
    print(f"Measure IQR: {find_measure(sensor_data)}")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
