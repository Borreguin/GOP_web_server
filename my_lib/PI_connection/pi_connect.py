""" coding: utf-8
Created by rsanchez on 03/05/2018
Este proyecto ha sido desarrollado en la Gerencia de Operaciones de CENACE
Mateo633
"""

import pandas as pd
import sys
import clr
import datetime

sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *


class PIserver:
    def __init__(self, ):
        piServers = PIServers()
        self.server = piServers.DefaultPIServer

    def find_PI_point(self, tag_name):
        """
        Find a PI_point in PIserver
        :param tag_name: name of the tag
        :return: PIpoint
        """
        pt = None
        try:
            pt = PIPoint.FindPIPoint(self.server, tag_name)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}] not found".format(tag_name))
        return pt

    @staticmethod
    def time_range(ini_time, end_time):
        """
        AFTimeRange
        :param ini_time: initial time (yyyy-mm-dd HH:MM:SS)
        :param end_time: ending time (yyyy-mm-dd HH:MM:SS)
        :return: AFTimeRange
        """
        timerange = None
        try:
            timerange = AFTimeRange(ini_time, end_time)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}, {1}] no correct format".format(ini_time, end_time))
        return timerange

    @property
    def time_range_for_today(self, ):
        """
        Time range of the current day from 0:00 to current time
        :return:
        """
        dt = datetime.datetime.now()
        str_td = dt.strftime("%Y-%m-%d")
        return AFTimeRange(str_td, str(dt))

    @staticmethod
    def span(delta_time):
        """
        AFTimeSpan object
        :param delta_time: ex: "30m"
        :return: AFTimeSpan object
        """
        span = None
        try:
            span = AFTimeSpan.Parse(delta_time)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}] no correct format".format(ini_time, end_time))
        return span

    def interpolated_of_tag_list(self, tag_list, time_range, span):
        """
        Return a DataFrame that contains the values of each tag in column
        and the timestamp as index
        :param tag_list: list of tags
        :param time_range: PIServer.time_range
        :param span: PIServer.span
        :return: DataFrame
        """
        pi_points = list()
        for tag in tag_list:
            pi_points.append(PI_point(self, tag))

        df_result = pi_points[0].interpolated(time_range, span, as_df=True, numeric=False)

        for piPoint in pi_points[1:]:
            df_result = pd.concat([df_result, piPoint.interpolated(time_range, span, numeric=False)], axis=1)

        return df_result


class PI_point:

    def __init__(self, server, tag_name):
        assert isinstance(server, PIserver)
        self.server = server
        self.tag_name = tag_name
        self.pt = server.find_PI_point(tag_name)

    def interpolated(self, time_range, span, as_df=True, numeric=True):
        """
        returns the interpolate values of a PIpoint
        :param numeric: try to convert to numeric values
        :param as_df: return as DataFrame
        :param time_range: PIServer.time_range
        :param span: PIServer.span
        :return: returns the interpolate values of a PIpoint
        """
        values = None
        try:
            values = self.pt.InterpolatedValues(time_range, span, "", False)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}, {1}] no correct object".format(time_range, span))
        if as_df:
            values = to_df(values, self.tag_name, numeric=numeric)
        return values

    def plot_values(self, time_range, n_samples, as_df=True, numeric=True):
        """
        n_samples of the tag in time range
        :param numeric: try to convert to numeric values
        :param as_df: return as DataFrame
        :param time_range:  PIServer.timerange
        :param n_samples:
        :return: OSIsoft.AF.Asset.AFValues
        """
        values = None
        try:
            values = self.pt.PlotValues(time_range, n_samples)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}, {1}] no correct object".format(time_range, n_samples))
        if as_df:
            values = to_df(values, self.tag_name, numeric)
        return values

    def recorded_values(self, time_range, AFBoundary=AFBoundaryType.Inside, as_df=True, numeric=True):
        """
        recorded values for a tag
        :param numeric: Convert to numeric
        :param as_df: return as DataFrame
        :param time_range: PIServer.time_range
        :param AFBoundary: AFBoundary
        :return: OSIsoft.AF.Asset.AFValues
        """
        values = None
        try:
            values = self.pt.RecordedValues(time_range, AFBoundary, "", False)
        except Exception as e:
            print(e)
            print("[pi_connect] [{0}, {1}] no correct object".format(time_range, n_samples))
        if as_df:
            values = to_df(values, self.tag_name, numeric)
        return values

    def summaries(self, time_range, span, AFSummaryTypes=AFSummaryTypes.Average,
                  AFCalculationBasis=AFCalculationBasis.TimeWeighted,
                  AFTimestampCalculation=AFTimestampCalculation.Auto):
        """
        Returns a list of summaries
        :param time_range: PIServer.time_range
        :param span: PIServer.span
        :param AFSummaryTypes:
        :param AFCalculationBasis:
        :param AFTimestampCalculation:
        :return: Returns a list of summaries
        """
        values = None
        try:
            values = self.pt.Summaries(time_range, span, AFSummaryTypes,
                                       AFCalculationBasis,
                                       AFTimestampCalculation)
        except Expection as e:
            print(e)
            print("[pi_connect] [{0}, {1}, {2}] no correct object".format(time_range, span, AFSummaryTypes))

        return values

    def snapshot(self):
        return self.pt.Snapshot()

    def current_value(self):
        return self.pt.CurrentValue()

    def average(self, time_range, span):
        summaries_list = self.summaries(time_range, span, AFSummaryTypes.Average)
        df = pd.DataFrame()
        for summary in summaries_list:
            df = to_df(summary.Value, tag=self.tag_name)
        return df


def to_df(values, tag, numeric=True):
    """
    returns a DataFrame based on PI values
    :param numeric: try to convert to numeric values
    :param values: PI values
    :param tag: name of the PI tag
    :return: DataFrame
    """
    df = pd.DataFrame()
    try:
        timestamp = [x.Timestamp.ToString("yyyy-MM-dd HH:mm:s") for x in values]
        df = pd.DataFrame(index=pd.to_datetime(timestamp))
        if numeric:
            df[tag] = pd.to_numeric([x.Value for x in values], errors='coerce')
        else:
            df[tag] = [x.Value for x in values]
    except Expection as e:
        print(e)
        print("[pi_connect] [{0}] to pdf".format(values))
    return df


def test():
    pi_svr = PIserver()
    tag_name = "CAL_DIST_QUITO_P.CARGA_TOT_1_CAL.AV"
    pt = PI_point(pi_svr, tag_name)
    time_range = pi_svr.time_range("2018-02-12", "2018-02-14")
    time_range2 = pi_svr.time_range_for_today
    span = pi_svr.span("30m")
    df1 = pt.interpolated(time_range, span)
    df2 = pt.plot_values(time_range, 200)
    df3 = pt.recorded_values(time_range2)
    value1 = pt.snapshot()
    value2 = pt.current_value()

    tag_list = ['JAMONDIN230POMAS_1_P.LINEA_ICC.AV', 'POMASQUI230JAMON_1_P.LINEA_RDV.AV',
                'JAMONDIN230POMAS_1_P.LINEA_ICC.AQ', 'POMASQUI230JAMON_1_P.LINEA_RDV.AQ']
    df1 = pi_svr.interpolated_of_tag_list(tag_list, time_range, span)
    df1.plot()
    df2.plot()
    df3.plot()

    df_average = pt.average(time_range, span)
    print(df_average)
    # from my_lib.holidays import holidays as hl
    # rs = hl.get_holiday_dates_as_df()
    # print(rs)


if __name__ == "__main__":
    perform_test = False
    if perform_test:
        test()

# piServers = PIServers()
# piServer = piServers.DefaultPIServer
# tag_name = "CAL_DIST_QUITO_P.CARGA_TOT_1_CAL.AV"
# tag_name = "SNI_GENERACION_P.TOTAL_CAL.AV"
# pt2 = PIPoint.FindPIPoint(piServer, tag_name)
# summaries = pt2.Summaries(timerange, span, AFSummaryTypes.Average,
# AFCalculationBasis.TimeWeighted, AFTimestampCalculation.Auto)
