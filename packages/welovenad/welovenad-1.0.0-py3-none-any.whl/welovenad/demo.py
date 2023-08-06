#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script provides several test methods."""

import pandas as pd


def interpolate_nan_values(rr_intervals, interpolation_method="linear"):
    """
    Function that interpolate Nan values with linear interpolation

    Parameters
    ---------
    rr_intervals : list
        RrIntervals list.
    interpolation_method : str
        Method used to interpolate Nan values of series.

    Returns
    ---------
    interpolated_rr_intervals : list
        new list with outliers replaced by interpolated values.
    """
    series_rr_intervals_cleaned = pd.Series(rr_intervals)
    # Interpolate nan values and convert pandas object to list of values
    interpolated_rr_intervals = series_rr_intervals_cleaned.interpolate(method=interpolation_method)
    return interpolated_rr_intervals.values.tolist()


def print_hello_NAD():
    print("Hello NAD !")
