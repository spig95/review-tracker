import numpy as np


def moving_avg_timebased(timestamps, x, delta_days, return_np_array=True, conf_level=0.95, centered=False):
    """Computes moving average and confidence interval.

    :param timestamps: list of timestamps
    :param x: list of corresponding values
    :param delta_days: number of days to be used to compute moving avg and moving std
    :param return_np_array: if True, return numpy arrays
    :param conf_level: confidence for the confidence interval (assuming normal distribution, which is not the case)
    :param centered: if True, the time window is centered on the given time. Else, the average is taken in the time
        window going from [t - delta_days, t]

    :return moving_avg, lower_conf, upper_conf: moving average, along with upper and lower confidence bounds.
    """
    assert delta_days >= 1
    x = np.array(x)
    timestamps = np.array(timestamps)
    t0 = timestamps[0]
    tmax = timestamps[-1]
    N = len(x)  # Total number of data
    delta_s = delta_days * 24 * 60 * 60  # Convert delta in seconds (needed for timestamps)

    if centered:
        left_margin = delta_s / 2
        right_margin = delta_s / 2
    else:
        left_margin = delta_s
        right_margin = 0

    moving_avg = list()
    upper_conf = list()
    lower_conf = list()

    for i in range(N):
        left_bound = max(t0, timestamps[i] - left_margin)
        right_bound = min(timestamps[i] + right_margin, tmax)
        time_window_idx = np.where((left_bound <= timestamps) & (timestamps <= right_bound))
        x_w = x[time_window_idx]
        ws = x_w.size  # Window size
        if ws > 1:
            avg = np.mean(x_w)
            std = np.std(x_w, ddof=1)
        else:
            # If data are too sparse we take the only data-point in the window
            avg = x[i]
            std = 0
        conf_interval = conf_level * std / np.sqrt(ws)
        moving_avg.append(avg)
        upper_conf.append(avg + conf_interval)
        lower_conf.append(avg - conf_interval)

    if return_np_array:
        return np.array(moving_avg), np.array(lower_conf), np.array(upper_conf)
    else:
        return moving_avg, lower_conf, upper_conf
