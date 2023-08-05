# system modules
import logging
import json
import io
import math
import time
import re
import inspect
import functools
import itertools
from posixpath import join as urljoin

# internal modules
from sensemapi import paths
from sensemapi.reprobject import ReprObject
from sensemapi.senseBox import senseBox
from sensemapi.senseBoxSensorData import senseBoxSensorData
from sensemapi.errors import *
from sensemapi.utils import *
from sensemapi import compat

# external modules
import requests

logger = logging.getLogger(__name__)

class SenseMapClient(ReprObject):
    """
    Client to interface the `OpenSenseMap API <https://api.opensensemap.org>`_

    Args:
        api (str, optional): the api server to use. You may use
            :any:`OPENSENSEMAP_API_LIVE` (default) or
            :any:`OPENSENSEMAP_API_TEST` for testing purposes.
    """
    def __init__(self, api = paths.OPENSENSEMAP_API_LIVE):
        frame = inspect.currentframe()
        args = inspect.getargvalues(frame)[0]
        for arg in args[1:]:
            val = locals().get(arg)
            if val is not None:
                setattr(self, arg, val)

    RETRY_AFTER_HEADER_REGEX = re.compile("retry.*after$", re.IGNORECASE)
    """
    Regex used to determine the header field containing the time to wait until
    issuing the next request
    """

    @simplegetter
    def api(self):
        return None

    @simplesetter(api)
    def api(self, new):
        return new

    def retry_after_time_if_too_many_requests(decorated_function):
        """
        Decorator to call a decorated method, catching an
        :any:`OpenSenseMapAPITooManyRequestsError`, trying to determine how
        long to wait from the error message, waiting that time and then
        retries.
        """
        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            try:
                return decorated_function(self, *args, **kwargs)
            except OpenSenseMapAPITooManyRequestsError as e:
                logger.debug(e)
                m = re.search(pattern=
                    "(?:(?P<seconds>\d+\.\d+)\s*s)|"
                    "(?:(?P<milliseconds>\d+\.\d+)\s*ms)"
                    ,string=str(e))
                try:
                    d = m.groupdict()
                    retry_after_seconds = 0
                    seconds = d.get("seconds")
                    milliseconds = d.get("milliseconds")
                    if seconds:
                        retry_after_seconds += float(seconds)
                    if milliseconds:
                        retry_after_seconds += float(milliseconds) / 1000
                except (AttributeError, ValueError, KeyError, IndexError):
                    raise OpenSenseMapAPITooManyRequestsError(
                        "Could not determine "
                        "time to wait until next retry.")
                logger.debug("Waiting {} seconds until retry..."
                    .format(retry_after_seconds))
                time.sleep(retry_after_seconds)
            logger.debug("Now trying again to call {}"
                .format(decorated_function))
            return decorated_function(self, *args, **kwargs)
        return wrapper

    @retry_after_time_if_too_many_requests
    def request(self, method, *args, **kwargs):
        """
        Wrapper around corresponding methods of :mod:`requests`, raising
        specific exceptions depending of the response.

        Args:
            method (str): the method to use. Needs to be a method of
                :any:`requests`.
            args, kwargs : arguments passed to the method

        Returns:
            requests.models.Response : the request response

        Raises:
            OpenSenseMapAPITooManyRequestsError : if the client issued too many
                requests
        """
        # perform the request
        method = getattr(requests, method)
        response = method(*args, **kwargs)
        logger.debug("API responded [status code {}]:\n{}".format(
            response.status_code, response.text))
        # too many requests
        if response.status_code == 429:
            headers = response.headers.copy()
            retry_after_header = next(
                filter(self.RETRY_AFTER_HEADER_REGEX.search, headers.keys()),
                None)
            retry_after = headers.get(retry_after_header)
            raise OpenSenseMapAPITooManyRequestsError(
                "retry after {}".format(retry_after) if retry_after else "")
        try:
            logger.debug("API responded JSON [status code {}]:\n{}".format(
                response.status_code, response.json()))
        except compat.JSONDecodeError:
            pass
        return response

    def _get_box(self, id, format = None):
        """
        Issue the request to retreive a single senseBox

        Args:
            id (str) : the senseBox id to retreive
            format (str, optional): one of ``"json"`` and ``"geojson"``

        Returns:
            dict : the API response
        """
        response = self.request("get",
            urljoin(self.api,paths.BOXES,id),
            params = {"format":format} if format else {}
            )
        response_json = response.json()
        if response.status_code == 200:
            return response_json
        else:
            message = response_json.get("message")
            raise OpenSenseMapAPIError("Could not retreive with id '{}'{}"
                .format(id, ": {}".format(message) if message else ""))

    def get_box(self, id):
        """
        Retreive one :any:`senseBox`

        Args:
            id (str) : the senseBox id to retreive

        Returns:
            senseBox : the retreived senseBox
        """
        box = senseBox.from_api_json(self._get_box(id = id, format = "json"))
        box.client = self
        return box

    def post_measurement(self, box_id, sensor_id, value, time = None,
        lat = None, lon = None, height = None):
        """
        Issue a request to upload a new measurement

        Args:
            box_id (str) : the senseBox id
            sensor_id (str) : the sensor's id
            value (float) : the current measurement value
            time (datetime.datetime, optional) : the time of the measurement
            lat, lon, height (float,optional) : the current position

        Returns:
            True : on success
        """
        assert box_id is not None, "box_id must  be defined"
        assert sensor_id is not None, "sensor_id must  be defined"
        d = {}
        d["value"] = float(value)
        if time:
            d["createdAt"] = date2str(time)
        try:
            d["location"] = location_dict(lat, lon, height)
        except ValueError:
            pass
        logger.debug("Sending Request with JSON:\n{}"
            .format(pretty_json(d)))
        response = self.request("post",
            urljoin(self.api,paths.BOXES,box_id,sensor_id),
            json = d,
            )
        try:
            response_json = response.json()
        except compat.JSONDecodeError: # pragma: no cover
            raise OpenSenseMapAPIError("Posting measurement didn't work: {}"
                .format(response.text))
        if hasattr(response_json, "get"): # is a dict
            message = response_json.get("message")
            raise OpenSenseMapAPIError("Posting measurement didn't work{}"
                .format(": "+ message or ""))
        else: # no dict
            if re.search("measurement\s+saved\s+in\s+box",response_json):
                return True

    @classmethod
    @needs_pandas
    def dataframe_to_csv_for_upload(self, df, discard_incomplete = False):
        """
        Convert a dataframe to csv for the upload

        Args:
            df (pandas.DataFrame): a dataframe with the at least the
                columns ``sensor_id`` (string), ``value`` (float) and
                optionally ``time`` (datetime), ``lat`` (float) **and** ``lon``
                (float) and ``height`` (float).
            discard_incomplete (bool, optional): use as much data as possible.
                If ``True``, drops parts of incomplete datasets for the API to
                accept the data. If ``False`` (default), raises
                :any:`ValueError` if the dataset is incomplete.

        Returns:
            str : the csv string

        Raises
            ValueError : if ``discard_incomplete=False`` and any row is
                incomplete
        """
        data = df.copy()
        # convert time to utc
        if "time" in data:
            try: # timezone-unaware
                data["time"] = data["time"].dt.tz_localize("UTC")
            except TypeError: # already timezone-aware
                data["time"] = data["time"].dt.tz_convert("UTC")
        duplicated = list(df["sensor_id"][df["sensor_id"].duplicated(
            keep=False)].unique())
        if duplicated:
            raise ValueError("The sensor id{s1} {ids} occur{s2} more than once. "
                "Posting 'multiple' new measurements does not mean "
                "'upload of timeseries'".format(
                    s1="s" if len(duplicated)>1 else "",
                    s2="" if len(duplicated)>1 else "s",
                    ids=",".join(duplicated)))
        groups = list(itertools.accumulate(
            (("sensor_id", "value"),("time",),("lon","lat"),("height",))
            ))
        csv_string = ""
        for group,smaller_group in \
            zip(reversed(groups),list(reversed(groups))[1:]+[[]]):
            logger.debug("current group: {}".format(group))
            logger.debug("smaller group: {}".format(smaller_group))
            try:
                part = data[list(group)]
            except KeyError as e:
                logger.debug("data is missing columns {}" .format(e))
                continue
            subset = set(group) - set(smaller_group)
            part_smaller_kept = part.dropna(axis = "index", how = "all",
                subset = subset)
            part_smaller_dropped = part.drop(part_smaller_kept.index)
            if not part_smaller_dropped.empty:
                logger.debug("These {} rows are incomplete "
                    "and obviously for smaller group {}:\n{}"
                    .format(len(part_smaller_dropped.index), subset,
                        part_smaller_dropped))
            part_kept = part_smaller_kept.dropna(axis = "index", how="any")
            part_dropped = part_smaller_kept.drop(part_kept.index)
            if not part_dropped.empty:
                logger.warning("These {} rows are incomplete, "
                    "this {} data will be discarded:\n{}"
                    .format(len(part_dropped.index), subset, part_dropped))
                if not discard_incomplete:
                    raise ValueError("In these rows, "
                        "none of columns {} must be NaN:\n{}"\
                        .format(smaller_group,part_dropped))
            logger.debug("Keeping these {} rows for group {}:\n{}".format(
                len(part_kept.index), group, part_kept))
            if part_kept.empty:
                continue
            csv_string += part_kept.to_csv(
                header = False,
                index = False,
                sep = ",",
                date_format = OPENSENSEMAP_DATETIME_FORMAT_UTC,
                )
            data.drop(part_kept.index, inplace = True)
        if not data.empty:
            logger.warning("Skipping these {} rows of data "
                "due to missing information:\n{}".format(len(data.index),data))
        return csv_string

    def post_measurements(self, box_id, measurements,
        discard_incomplete = False):
        """
        Post multiple measurements to sensors in a :class:`senseBox`

        Args:
            box_id (str): the senseBox id
            measurements (pandas.DataFrame): a dataframe with the at least the
                columns ``sensor_id`` (string), ``value`` (float) and
                optionally ``time`` (datetime), ``lat`` (float) **and** ``lon``
                (float) and ``height`` (float).
            discard_incomplete (bool, optional): use as much data as possible.
                If ``True``, drops parts of incomplete datasets for the API to
                accept the data. If ``False`` (default), raises
                :any:`ValueError` if the dataset is incomplete.

        Returns:
            bool : whether the upload was successful
        """
        csv_string = self.dataframe_to_csv_for_upload(
            measurements, discard_incomplete = discard_incomplete)
        logger.debug("Attempting to upload CSV data to senseBox '{}':\n{}"
            .format(box_id, csv_string))
        response = self.request("post",
            url = urljoin(self.api,paths.BOXES,box_id,"data"),
            headers = {"content-type": "text/csv"},
            data = csv_string,
            )
        if response.status_code == requests.codes.CREATED:
            return True
        try:
            response_json = response.json()
        except compat.JSONDecodeError: # pragma: no cover
            raise OpenSenseMapAPIError("Posting measurement didn't work: {}"
                .format(response.text))
        message = response_json.get("message")
        raise OpenSenseMapAPIError("Posting measurement didn't work{}"
            .format(": "+ message or ""))

    def get_measurements(self, box_id, sensor_id,
        from_date = None, to_date = None,
        format = None, download = None, outliers = None,
        outlier_window = None, delimiter = None,
        ):
        """
        Retrieve the 10000 latest measurements for a sensor

        Args:
            box_id (str): the senseBox id
            sensor_id (str): the sensor id
            from_date (datetime.datetime, optional): beginning date of
                measurement data (default: 48 hours ago from now)
            to_date (datetime.datetime, optional): end date of measurement data
                (default: now)
            format (str, optional): either ``"json"`` (default) or ``"csv"``
            outliers (bool, optional): add outlier marker `isOutlier` to data?
            outlier_window (int, optional):
                outlier window size (1-50, default: 15)
            delimiter (str, optional): either ``"comma"`` (default) or
                ``"semicolon"``

        Returns:
            senseBoxSensorData : the retrieved data
        """
        assert box_id is not None, "box_id must  be defined"
        assert sensor_id is not None, "sensor_id must  be defined"
        d = {}
        if from_date is not None:
            d["from-date"] = date2str(from_date)
        if to_date is not None:
            d["to-date"] = date2str(to_date)
        if format is not None:
            d["format"] = str(format)
        if outliers is not None:
            d["outliers"] = bool(outliers)
        if outlier_window is not None:
            d["outlier-window"] = int(outlier_window)
        logger.debug("Sending GET request with parameters:\n{}"
            .format(pretty_json(d)))
        response = self.request("get",
            urljoin(self.api,paths.BOXES,box_id,"data",sensor_id),
            params = d,
            )
        try:
            response_json = response.json()
            raise NotImplementedError("Parsing JSON-formatted measurements "
                "is not yet implemented. Use format='csv'")
        except compat.JSONDecodeError:
            return senseBoxSensorData.from_csv(io.StringIO(response.text))
