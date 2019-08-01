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
    for dsn in result:
        #put the data data each tag into the data frame
        for tag in result[dsn].items():
            tag = tag[1]
            name = dsn + " " + tag["TagName"]

            is_numeric = reduce(lambda x, y: x and y["IsNumeric"], tag["Values"], True)
            if (is_numeric):
                values = list(map(lambda x: x["NumericValue"], tag["Values"]))
            else:
                values = list(map(lambda x: x["TextValue"], tag["Values"]))

            frame_data[name] = values

    return pd.DataFrame(frame_data)