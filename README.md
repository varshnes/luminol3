# luminol3

[![Python Versions](https://img.shields.io/badge/Python-2.7%2C%203.5%2C%203.6-blue.svg)](https://travis-ci.org/brennv/luminol)
[![Build Status](https://travis-ci.org/brennv/luminol.svg?branch=master)](https://travis-ci.org/brennv/luminol)
[![Test Coverage](https://codeclimate.com/github/brennv/luminol3/badges/coverage.svg)](https://codeclimate.com/github/brennv/luminol3/coverage)
[![Code Climate](https://codeclimate.com/github/brennv/luminol3/badges/gpa.svg)](https://codeclimate.com/github/brennv/luminol3)
[![Issue Count](https://codeclimate.com/github/brennv/luminol3/badges/issue_count.svg)](https://codeclimate.com/github/brennv/luminol3)

A Python 3 compatible fork of [luminol](https://github.com/linkedin/luminol) for detecting anomalies in a time series, and correlating anomalies between two time series.

### Installation
```
pip install luminol3
```

### Getting started

#### Calculate anomaly scores

```python
from luminol.anomaly_detector import AnomalyDetector

ts = {0: 0, 1: 0.5, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0}

my_detector = AnomalyDetector(ts)
score = my_detector.get_all_scores()

for timestamp, score in score.iteritems():
    print(timestamp, ts[timestamp], score)

""" Output:
time  value  score
0     0      0.0
1     0.5    0.873128250131
2     1      1.57163085024
3     1      2.13633686334
4     1      1.70906949067
5     0      2.90541813415
6     0      1.17154110935
7     0      0.937232887479
8     0      0.749786309983
"""
```

#### Correlate anomaly periods between two time series

```python
from luminol.anomaly_detector import AnomalyDetector
from luminol.correlator import Correlator

ts1 = {0: 0, 1: 0.5, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0}
ts2 = {0: 0, 0: 0.5, 2: 1, 3: 0.5, 4: 1, 5: 0, 6: 1, 7: 1, 8: 1}

my_detector = AnomalyDetector(ts1, score_threshold=1.5)
score = my_detector.get_all_scores()
anomalies = my_detector.get_anomalies()
for a in anomalies:
    time_period = a.get_time_window()
    my_correlator = Correlator(ts1, ts2, time_period)
    if my_correlator.is_correlated(threshold=0.8):
        print("ts2 correlate with ts1 at time period (%d, %d)" % time_period)

""" Output:
ts2 correlates with ts1 at time period (2, 5)
"""
```

### Overview

The primary features of luminol are anomaly detection and correlation. By comparing scored time series from separate events, it can aid in the investigation of possible causes of anomaly.

* Score a time series for anomalies and identify corresponding time windows.
* Correlate anomaly periods between two time series.

Luminol is configurable in a sense that scoring thresholds are tunable and you can choose from several algorithms utilized for anomaly detection and/or correlation.

### Typical workflow

Conduct anomaly detection on a single time series ts.
```python
detector = luminol.anomaly_detector.AnomalyDetector(ts)
anomalies = detector.get_anomalies()
```

If there is anomaly, correlate the first anomaly period with a secondary time series ts2.
```python
if anomalies:
    time_period = anomalies[0].get_time_window()
    correlator = luminol.correlator.Correlator(ts, ts2, time_period)
```

Get the correlation coefficient
```python
print correlator.get_correlation_result().coefficient
```

### Modules
Modules in Luminol refers to customized classes developed for better data representation, which are `Anomaly`, `CorrelationResult` and `TimeSeries`.

#### Anomaly
_class_ luminol.modules.anomaly.**Anomaly**
<br/> It contains these attributes:
```python
self.start_timestamp: # epoch seconds represents the start of the anomaly period.
self.end_timestamp: # epoch seconds represents the end of the anomaly period.
self.anomaly_score: # a score indicating how severe is this anomaly.
self.exact_timestamp: # epoch seconds indicates when the anomaly reaches its severity.
```
It has these public methods:
* `get_time_window()`: returns a tuple (start_timestamp, end_timestamp).

#### CorrelationResult
_class_ luminol.modules.correlation_result.**CorrelationResult**
<br/> It contains these attributes:
```python
self.coefficient: # correlation coefficient.
self.shift: # the amount of shift needed to get the above coefficient.
self.shifted_coefficient: # a correlation coefficient with shift taken into account.
```

#### TimeSeries
_class_ luminol.modules.time_series.**TimeSeries**
```python
__init__(self, series)
```
* `series(dict)`: timestamp -> value

It has a various handy methods for manipulating time series, including generator `iterkeys`, `itervalues`, and `iteritems`. It also supports binary operations such as add and subtract. Please refer to the [code](https://github.com/linkedin/naarad/blob/master/lib/luminol/src/luminol/modules/time_series.py) and inline comments for more information.

### API
The library contains two classes: `AnomalyDetector` and `Correlator`, and there are two sets of APIs, one corresponding to each class. There are also customized modules for better data representation. The [Modules](#modules) section in this documentation may provide useful information as you walk through the APIs.

#### AnomalyDetector
_class_ luminol.anomaly_detector.**AnomalyDetecor**
```python
__init__(self, time_series, baseline_time_series=None, score_only=False, score_threshold=None,
score_percentile_threshold=None, algorithm_name=None, algorithm_params=None,
refine_algorithm_name=None, refine_algorithm_params=None)
```
*  `time_series`: The metric you want to conduct anomaly detection on. It can have the following three types:

```python
1. string: # path to a csv file
2. dict: # timestamp -> value
3. lumnol.modules.time_series.TimeSeries
```

* `baseline_time_series`: an optional baseline time series of one the types mentioned above.
* `score only(bool)`: if asserted, anomaly scores for the time series will be available, while anomaly periods will not be identified.
* `score_threshold`: if passed, anomaly scores above this value will be identified as anomaly. It can override score_percentile_threshold.
* `score_precentile_threshold`: if passed, anomaly scores above this percentile will be identified as anomaly. It can not override score_threshold.
* `algorithm_name(string)`: if passed, the specific algorithm will be used to compute anomaly scores.
* `algorithm_params(dict)`: additional parameters for algorithm specified by algorithm_name.
* `refine_algorithm_name(string)`: if passed, the specific algorithm will be used to compute the time stamp of severity within each anomaly period.
* `refine_algorithm_params(dict)`: additional parameters for algorithm specified by refine_algorithm_params.

Available algorithms and their additional parameters are:

```python
1.  'bitmap_detector': # behaves well for huge data sets, and it is the default detector.
    {
      'precision'(4): # how many sections to categorize values,
      'lag_window_size'(2% of the series length): # lagging window size,
      'future_window_size'(2% of the series length): # future window size,
      'chunk_size'(2): # chunk size.
    }
2.  'default_detector': # used when other algorithms fails, not meant to be explicitly used.
3.  'derivative_detector': # meant to be used when abrupt changes of value are of main interest.
    {
      'smoothing factor'(0.2): # smoothing factor used to compute exponential moving averages
                                # of derivatives.
    }
4.  'exp_avg_detector': # meant to be used when values are in a roughly stationary range.
                        # and it is the default refine algorithm.
    {
      'smoothing factor'(0.2): # smoothing factor used to compute exponential moving averages.
      'lag_window_size'(20% of the series length): # lagging window size.
      'use_lag_window'(False): # if asserted, a lagging window of size lag_window_size will be used.
    }
```

It may seem vague for the meanings of some parameters above. Here are some useful insights:
* [Bitmap](http://alumni.cs.ucr.edu/~ratana/SSDBM05.pdf)
* [Exponential Moving Avg](http://en.wikipedia.org/wiki/Exponential_smoothing)

The **AnomalyDetector** class has the following public methods:
* `get_all_scores()`: returns an anomaly score time series of type [TimeSeries](#modules).
* `get_anomalies()`: return a list of [Anomaly](#modules) objects.

#### Correlator
_class_ luminol.correlator.**Correlator**
```python
__init__(self, time_series_a, time_series_b, time_period=None, use_anomaly_score=False,
algorithm_name=None, algorithm_params=None)
```
* `time_series_a`: a time series, for its type, please refer to time_series for AnomalyDetector above.
* `time_series_b`: a time series, for its type, please refer to time_series for AnomalyDetector above.
* `time_period(tuple)`: a time period where to correlate the two time series.
* `use_anomaly_score(bool)`: if asserted, the anomaly scores of the time series will be used to compute correlation coefficient instead of the original data in the time series.
* `algorithm_name`: if passed, the specific algorithm will be used to calculate correlation coefficient.
* `algorithm_params`: any additional parameters for the algorithm specified by algorithm_name.

Additional parameters are:

```python
1.  'cross_correlator': # when correlate two time series, it tries to shift the series around so that it
                       # can catch spikes that are slightly apart in time.
    {
      'max_shift_seconds'(60): # maximal allowed shift room in seconds,
      'shift_impact'(0.05): # weight of shift in the shifted coefficient.
    }
```

The **Correlator** class has the following public methods:
* `get_correlation_result()`: return a [CorrelationResult](#modules) object.
* `is_correlated(threshold=0.7)`: if coefficient above the passed in threshold, return a [CorrelationResult](#modules) object. Otherwise, return false.

### Contributing
Clone source and install package and dev requirements:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pylama
```

Tests and linting run with:

```bash
pytest -v --cov=luminol/ tests/ && pylama -i E501 luminol/
```
