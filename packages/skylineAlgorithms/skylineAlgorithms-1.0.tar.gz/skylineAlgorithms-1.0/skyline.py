# -*- coding: utf-8 -*-
import sys
import os
FP = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(FP)
import numpy as np
import pandas as pd
from scipy import stats,array,std

def detect(ts,CONSENSUS=6,FULL_DURATION = 1,INTERVAL = 5):
    '''
    返回连续型数据（时间序列）的基线
    '''
    #----------------------------
    #INTERVAL = 5 #数据粒度，单位为分钟
    #FULL_DURATION = 1 #数据跨度，单位为天
    #----------------------------
    top1, low1 =re_median_absolute_deviation(ts)
    top2 =re_grubbs(ts)
    top3,low3 = re_first_hour_average(ts,FULL_DURATION,INTERVAL)
    top4,low4 = re_stddev_from_average(ts)
    top5,low5 = re_mean_subtraction_cumulation(ts)
    top6,low6 = re_stddev_from_moving_average(ts)
    top7,low7 = re_least_squares(ts)
    top8,low8 = re_histogram_bins(ts)

    consensus = CONSENSUS
    threshold = sorted([top1,top2,top3,top4,top5,top6,top7,low8])
    threshold_low = sorted([low1,low3,low4,low5,low6,low7])
    return threshold[consensus-1]

def detect_list(ts,CONSENSUS=3):
    '''
    #离散型数据（离散数据点）的基线
    '''
    if len(ts)==1:
        return ts[0]
    top1, low1 = re_median_absolute_deviation(ts)
    top2 = re_grubbs(ts)
    top3, low3 = re_stddev_from_average(ts)
    top4, low4 = re_histogram_bins(ts)
    threshold = sorted([top1, top2, top3, low4])
    consensus = CONSENSUS
    return threshold[consensus-1]

def re_median_absolute_deviation(timeseries):
    threshold = 6
    series = pd.Series([x for x in timeseries])
    median = series.median()
    demedianed = np.abs(series - median)
    median_deviation = demedianed.median()
    high = median+threshold*median_deviation
    low = max(median-threshold*median_deviation,0)
    return high,low

def re_grubbs(timeseries):
    series = array(timeseries)
    stdDev = std(series)
    mean = np.mean(series)
    len_series = len(series)
    threshold = stats.t.isf(.05 / (2 * len_series), len_series - 2)
    threshold_squared = threshold * threshold
    grubbs_score = ((len_series - 1) / np.sqrt(len_series)) * np.sqrt(threshold_squared / (len_series - 2 + threshold_squared))
    high = grubbs_score*stdDev+mean
    return high

def re_first_hour_average(timeseries,FULL_DURATION,INTERVAL):
    """
    Calcuate the simple average over one hour, FULL_DURATION seconds ago.
    A timeseries is anomalous if the average of the last three datapoints
    are outside of three standard deviations of this value.
    """
    threshold = 3
    series = pd.Series(timeseries[-1*FULL_DURATION*1440//INTERVAL:])
    mean = series.mean()
    stdDev = series.std()
    high =  mean+threshold*stdDev
    low = max(mean-threshold*stdDev,0)
    return high, low

def re_stddev_from_average(timeseries):
    threshold = 3
    series = pd.Series([x for x in timeseries])
    mean = series.mean()
    stdDev = series.std()
    high =  mean+threshold*stdDev
    low = max(mean-threshold*stdDev,0)
    return high, low

def re_stddev_from_moving_average(timeseries):
    threshold = 3
    series = pd.Series([x for x in timeseries])
    expAverage = pd.Series.ewm(series, com=50).mean()
    stdDev = pd.Series.ewm(series, com=50).std()
    high = expAverage.iat[-1]+threshold*stdDev.iat[-1]
    low = max(0,expAverage.iat[-1]-threshold*stdDev.iat[-1])
    return high, low

def re_mean_subtraction_cumulation(timeseries):
    """
    A timeseries is anomalous if the value of the next datapoint in the
    series is farther than three standard deviations out in cumulative terms
    after subtracting the mean from each data point.
    """
    threshold = 3
    series = pd.Series([x for x in timeseries])
    temp_mean = series.mean()
    series = series - temp_mean
    expAverage = pd.Series.ewm(series, com=15).mean()
    stdDev = pd.Series.ewm(series, com=15).std()
    high = expAverage.iat[-1]+threshold*stdDev.iat[-1]+temp_mean
    low = expAverage.iat[-1]-threshold*stdDev.iat[-1]+temp_mean
    return high, low

def re_least_squares(timeseries):
    y = np.array(timeseries)
    x = np.array(range(len(timeseries)))
    A = np.vstack([x, np.ones(len(x))]).T
    results = np.linalg.lstsq(A, y, rcond=None)
    residual = results[1]
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    errors = []
    y_prime = []
    for i, value in enumerate(y):
        projected = m * x[i] + c
        y_prime.append(projected)
        error = value - projected
        errors.append(error)
    if len(errors) < 3:
        return False

    std_dev = std(errors)
    high = [y+3*std_dev for y in y_prime][-1]
    low = [max(y-3*std_dev,0) for y in y_prime] [-1] 
    return high, low

def re_histogram_bins(timeseries):
    series = array(timeseries)
    t = timeseries[-1]
    h = np.histogram(series, bins=15)
    bins = h[1]
    high = -1
    low = -1
    for index, bin_size in enumerate(h[0]):
        if bin_size <= 20:
            # Is it in the first bin?
            if index == 0:
                high = bins[0]
                low = 0

            # Is it in the current bin?
            else:
                high = max(high,bins[index+1])
                if low == -1: low = bins[index]
                else: low = min(low,bins[index])

    return high, low


if __name__ == '__main__':
    l = [1, 2, 3, 4, 5, 6] #待检测列表
    threshold1 = detect(l) #连续型数据（时间序列）的基线
    print(threshold1)
    threshold2 = detect_list(l) #离散型数据（离散数据点）的基线
    print(threshold2)