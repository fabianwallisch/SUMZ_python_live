from enum import Enum


class JsonRequestKeys(Enum):
    TimeSeries = 'timeSeries'
    PredictionSteps = 'predSteps'
    NumberOfSamples = 'numSamples'
    TimeSeriesID = 'id'
    TimeSeriesValues = 'values'
