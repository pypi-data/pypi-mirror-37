from scipy.signal import butter, filtfilt
from ..data_formatting import validator


def butterworth(input_data, sr, cutoffs, order, btype='low'):
    '''Apply butterworth filter to the input array or dataframe each column'''
    nyquist = sr / 2.0

    if(isinstance(cutoffs, list)):
        cutoffs = [cutoff / nyquist for cutoff in cutoffs]
        B, A = butter(order, cutoffs, btype=btype, output='ba')
    else:
        B, A = butter(order, cutoffs/nyquist, btype=btype, output='ba')

    output_data = input_data
    if validator.is_sensor_dataframe(input_data):
        cols = input_data.columns[1:]
        X = input_data[cols].values
        result = filtfilt(B, A, X, axis=0, padtype=None)
        output_data[cols] = result
    elif validator.is_numpy_array(input_data):
        X = input_data
        result = filtfilt(B, A, X, axis=0, padtype=None)
        output_data = result
    return output_data
