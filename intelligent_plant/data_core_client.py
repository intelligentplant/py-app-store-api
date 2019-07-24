"""This module implments a client for the Intelligent Plant Data Core API"""
__author__ = "Ross Kelso"
__docformat__ = 'reStructuredText'

import urllib.parse as urlparse

import httplib2
import json
h = httplib2.Http(".cache")

import intelligent_plant.http_client as http_client

class DataCoreClient(http_client.HttpClient):
    """Access the Intelligent Plant Data Core API"""

    def __init__(self, authorization_header, base_url = "https://appstore.intelligentplant.com/gestalt/"):
        """
        Initialise a data core client with the specified authoriation haeder value and base URL.
        It is recommended that you use AppStoreClient.get_data_core_client(..) rather than calling this directly.

        :param authorization_header: The authorization header that will be used for all requests.
        :param base_url: The base URL to make requests from. The default value is "https://appstore.intelligentplant.com/gestalt/" (the app store data api)
        """
        http_client.HttpClient.__init__(self, authorization_header, base_url)
    
    def get_data_sources(self, filters):
        """
        Get the list of available data sources

        :param filter: A list of filters that should be applied to the search (if unsure try ["*"] to get all data sources)

        :return: The available data sources as a parsed JSON object.
        :raises: :class:`HTTPError`, if one occurred.
        :raises: An exception if JSON decoding fails.
        """
        params = {
            "filter": ",".join(filters)
        }
        
        return self.get_json("api/data/datasources", params)

    def get_tags(self, dsn, page = 1, page_size = 20, filters = {}):
        """
        Search the provided data source fo tags.

        :param dsn: The fully qualified name of the data source. seealso::get_data_sources
        :param page: The number of the current page of results. Default: 1.
        :param page_size: The number of results to return on a page. Default: 20.
        :param filters: A dictionary of filters where the key is the field name (e.g. name, description, unit)
            and the value is the filter to apply.

        :return: The available tags as a parsed JSON object.
        :raises: :class:`HTTPError`, if one occurred.
        :raises: An exception if JSON decoding fails.
        """
        params = filters.copy()
        params["dsn"] = dsn
        params["page"] = page
        params["pageSize"] = page_size
        
        return self.get_json("api/data/tags", params)

    def get_data(self, dsn, tags, function, start=None, end=None, step=None, points=None, annotations=False):
        """
        Perform a data query on a specific data source.

        :param dsn: The fully qualified name of the data source. seealso::get_data_sources
        :param tags: A list of tag names to get data for.
        :param function: The data function to use for the request ("now", "plot", "interp", "max", "min" "avg" or "raw")
        :param start: The start time of the data query. Can be relative (e.g. "*-30d") or absolute (01/01/2019) (required if function isn't "now")
        :param end: The end time of the data query. Can be relative (e.g. "*-30d") or absolute (01/01/2019) (required if function isn't "now")
        :param step: The size of a data interval (e.g. "1d", "10m", "30s") this or points required.
        :param points: The number of data points or samples to return this or step is required.
        :param annotations: Whether annotations should be included. Default: False.

        :return: The values of the specified tags, over the specified time range.
        :raises: :class:`HTTPError`, if one occurred.
        :raises: An exception if JSON decoding fails.
        """

        params = {
            "tag": tags,
            "function": function,
            "start": start,
            "end": end,
            "step": step,
            "points": points
        }

        #optinally include annotations
        if (annotations):
            params["annotations"] = "true"

        return self.get_json("api/data/values/" + dsn, params)

    def get_data_multi_data_source(self, dsns, tags, function, start, end, step=None, points=None, annotations=False):
        """
        Perform a data query on a multiple data sources simulataneously.

        :param dsns: A list of the fully qualified name of the data sources. seealso::get_data_sources
        :param tags: A list of tag names to get data for.

        The size of tags and dsns must match as the each tag will be queried on the data source in the corresponding dnns index.

        :param function: The data function to use for the request ("now", "plot", "interp", "max", "min" "avg" or "raw")
        :param start: The start time of the data query. Can be relative (e.g. "*-30d") or absolute (01/01/2019) (required if function isn't "now")
        :param end: The end time of the data query. Can be relative (e.g. "*-30d") or absolute (01/01/2019) (required if function isn't "now")
        :param step: The size of a data interval (e.g. "1d", "10m", "30s") this or points required.
        :param points: The number of data points or samples to return this or step is required.
        :param annotations: Whether annotations should be included. Default: False.

        :return: The values of the specified tags, over the specified time range.
        Note: due to how requests formats parameters with multiple values this uses an alternate library
        """
        url = self.base_url + "/api/data/values"

        #if datasource and tags are not list make them lists with 1 item
        dsns = dsns if type(dsns) is list else [dsns]
        tags = tags if type(tags) is list else [tags]

        if len(dsns) != len(tags):
            raise Exception("There must be a data source for each tag")

        params = {
            "function": function,
            "start": start,
            "end": end,
            "step": step,
            "points": points
        }

        #optinally include annotations
        if (annotations):
            params["annotations"] = "true"
        
        #add the none list parameters to the url
        url_parts = list(urlparse.urlparse(url))
        url_parts[4] = urlparse.urlencode({k: v for k, v in params.items() if v is not None})
        url = urlparse.urlunparse(url_parts)

        #add tlist parameters to the url
        for num, dsn in enumerate(dsns, start=0):
            url += "&dsn[" + str(num) + "]=" + urlparse.quote(dsn)

        for num, tag in enumerate(tags, start=0):
            url += "&tag[" + str(num) + "]=" + urlparse.quote(tag)

        if params != None:
            add_query_to_url(url, params)

        resp, content = h.request(url, "GET", headers=self.headers)

        if resp.status == 200:
            #success
            return json.loads(content)
        else:
            #handle the error
            raise Exception((resp, content))
