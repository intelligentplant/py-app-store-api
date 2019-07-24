"""This module implments utility functions for use with the Intelligent Plant APIs"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import math
from functools import reduce

import pandas as pd

def query_result_to_data_frame(result):
    """Convert the result of a data query into a data frame
       warn: this assumes that the timestamps for eachtag match (i.e. this won't work properly for raw queries)

       :param result: The parsed JSON result object. seealso: data_core_clinet.DataCoreClient.get_data(..)

       :return: A data frame with the queried tags as column headers and a row for each data point returned.
    """
    frame_data = {}

    #put the data from each tag into the data frame
    for tag in result:
        name = tag["tagName"]

        is_numeric = reduce(lambda x, y: y and (not math.isnan(x)) and math.isfinite(x), tag["tagData"], True)
        if (is_numeric):
            values = tag["tagData"]
        else:
            values = tag["tagStringValues"]

        frame_data[name] = values

    return pd.DataFrame(frame_data)