
import os
import json

import pandas as pd
import ezhc as hc
from ipyaggrid import Grid


class Plot:
    """
    """

    @staticmethod
    def build_series_data(df):
        """
        """
        data = df.reset_index().values.tolist()
        return data

    @staticmethod
    def price_evolution(dfi,
                        undl,
                        rollKey,
                        save=False,
                        folder_save='dump',
                        name=None,
                        tagged=True,
                        x_axis_ordinal=False,
                        **kwargs):
        """
        """
        msg = 'df must be a DataFrame'
        assert isinstance(dfi, pd.DataFrame), msg
        for e in ['date', 'bid', 'ask', 'trade', 'volume']:
            msg = 'df must have column {}'.format(e)
            assert e in dfi, msg
        msg = 'column date must be datetime'
        assert dfi['date'].dtype.kind == 'M', msg

        df0 = dfi[dfi['trade'] != 0]
        df1 = df0[['date', 'trade', 'bid', 'ask']]
        df1 = df1.set_index('date')

        df2 = df0[['date', 'volume']]
        df2 = df2.set_index('date')

        g = hc.Highstock()

        g.exporting.enabled = False
        g.chart.width = 900
        g.chart.height = 500
        g.chart.marginRight = 60
        g.legend.enabled = True
        g.legend.layout = 'horizontal'
        g.legend.align = 'center'
        g.legend.maxHeight = 100
        g.tooltip.enabled = True
        g.tooltip.valueDecimals = 2

        g.xAxis.ordinal = x_axis_ordinal
        if x_axis_ordinal:
            g.rangeSelector.buttons = [{
                'type': 'all',
                'text': 'All'
            }]
        else:
            g.rangeSelector.buttons = [{
                'type': 'day',
                'count': 1,
                'text': '1d'
            }, {
                'type': 'week',
                'count': 1,
                'text': '1w'
            }, {
                'type': 'week',
                'count': 2,
                'text': '2w'
            }, {
                'type': 'month',
                'count': 1,
                'text': '1m'
            }, {
                'type': 'month',
                'count': 2,
                'text': '2m'
            }, {
                'type': 'all',
                'text': 'All'
            }]

        g.chart.zoomType = 'x'
        title = 'Historical Trades for {} Roll {} : Price & Volume'
        g.title.text = title.format(undl, rollKey)

        g.tooltip.split = True

        # g.xAxis.gridLineWidth = 1.0
        # g.xAxis.gridLineDashStyle = 'Dot'
        # g.yAxis.gridLineWidth = 1.0
        # g.yAxis.gridLineDashStyle = 'Dot'

        g.yAxis = [{
            'labels': {
                'align': 'right',
                'x': +25,
            },
            'title': {
                'text': 'Price',
                'x': +40,
            },
            'height': '60%',
            'lineWidth': 2,
            'resize': {
                'enabled': True
            }
        }, {
            'labels': {
                'align': 'right',
                'x': +25,
            },
            'title': {
                'text': 'Volume',
                'x': +40
            },
            'top': '65%',
            'height': '35%',
            'offset': 0,
            'lineWidth': 2
        }]

        g.credits.enabled = True
        g.credits.text = 'Source: SG Markets | Futures Rollbox'
        g.credits.href = 'https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_02'


        g.series = [{
            'type': 'line',
            'name': 'trade',
            'data': Plot.build_series_data(df1[['trade']]),
            'yAxis': 0,
        }, {
            'type': 'line',
            'name': 'bid',
            'data': Plot.build_series_data(df1[['bid']]),
            'yAxis': 0,
        }, {
            'type': 'line',
            'name': 'ask',
            'data': Plot.build_series_data(df1[['ask']]),
            'yAxis': 0,
        }, {
            'type': 'column',
            'name': 'Volume',
            'data': Plot.build_series_data(df2[['volume']]),
            'yAxis': 1,
        }]


        for k, v in kwargs.items():
            setattr(g, k, v)


        if save:
            # prepare save
            if not os.path.exists(folder_save):
                os.makedirs(folder_save)
            if not name:
                name = 'plot_price_evolution'

        html = g.html(save=save,
                      save_path=folder_save,
                      save_name=name,
                      dated=tagged,
                      notebook=False,
                      center=True)
        return df0, html

    @staticmethod
    def volume_price_analysis(dfi,
                              undl,
                              rollKey,
                              save=False,
                              folder_save='dump',
                              name=None,
                              tagged=True,
                              x_axis_ordinal=False,
                              **kwargs):
        """
        """
        msg = 'df must be a DataFrame'
        assert isinstance(dfi, pd.DataFrame), msg
        for e in ['electronicVolume', 'overTheCounterVolume', 'price']:
            msg = 'df must have column {}'.format(e)
            assert e in dfi, msg

        df0 = dfi.rename(columns={
            'electronicVolume': 'electronic',
            'overTheCounterVolume': 'OTC',
        })
        df = df0.set_index('price')

        g = hc.Highcharts()

        g.exporting.enabled = False
        g.chart.width = 900
        g.chart.height = 500
        g.legend.enabled = True
        g.legend.layout = 'horizontal'
        g.legend.align = 'center'
        g.legend.maxHeight = 100

        g.xAxis.ordinal = x_axis_ordinal

        g.chart.zoomType = 'x'

        title = 'Volume vs. Price for {} Roll {}'
        g.title.text = title.format(undl, rollKey)

        g.credits.enabled = True
        g.credits.text = 'Source: SG Markets | Futures Rollbox'
        g.credits.href = 'https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_02'

        g.xAxis.title.text = 'Price'
        g.yAxis = [{
            'title': {
                'text': 'Volume'
            },
            'lineWidth': 2,
            'resize': {
                'enabled': True
            }
        }]

        g.tooltip = {
            'enabled': True,
            'shared': True,
            'useHTML': True,
            'headerFormat': 'Price: {point.key}<br/>',
            'pointFormat': '<span style="color:{series.color}">{series.name}: <b>{point.y:,.f}</b><br/>',
        }

        g.plotOptions.column.stacking = 'normal'

        g.series = [{
            'type': 'column',
            'name': 'Electronic',
            'data': Plot.build_series_data(df[['electronic']]),
            'yAxis': 0,
        }, {
            'type': 'column',
            'name': 'OTC',
            'data': Plot.build_series_data(df[['OTC']]),
            'yAxis': 0,
        }]

        for k, v in kwargs.items():
            setattr(g, k, v)

        if save:
            # prepare save
            if not os.path.exists(folder_save):
                os.makedirs(folder_save)
            if not name:
                name = 'plot_volume_price_analysis'

        html = g.html(save=save,
                      save_path=folder_save,
                      save_name=name,
                      dated=tagged,
                      notebook=False,
                      center=True)
        return df, html

    @staticmethod
    def open_interest_analysis(dfi,
                               undl,
                               rollKey,
                               save=False,
                               folder_save='dump',
                               name=None,
                               tagged=True,
                               x_axis_ordinal=False,
                               **kwargs):
        """
        """
        msg = 'df must be a DataFrame'
        assert isinstance(dfi, pd.DataFrame), msg
        for e in ['date', 'currentRollOpenInterest', 'nextRollOpenInterest', 'totalOpenInterest']:
            msg = 'df must have column {}'.format(e)
            assert e in dfi, msg
        msg = 'column date must be datetime'
        assert dfi['date'].dtype.kind == 'M', msg

        df0 = dfi.rename(columns={
            'currentRollOpenInterest': 'Current Future',
            'nextRollOpenInterest': 'Next Future',
            'totalOpenInterest': 'Total',
        })
        df = df0.set_index('date')

        g = hc.Highstock()

        g.exporting.enabled = False
        g.chart.width = 900
        g.chart.marginRight = 60
        g.chart.height = 500
        g.legend.enabled = True
        g.legend.layout = 'horizontal'
        g.legend.align = 'center'
        g.legend.maxHeight = 100
        g.tooltip.enabled = True

        g.xAxis.ordinal = x_axis_ordinal
        if x_axis_ordinal:
            g.rangeSelector.buttons = [{
                'type': 'all',
                'text': 'All'
            }]
        else:
            g.rangeSelector.buttons = [{
                'type': 'day',
                'count': 1,
                'text': '1d'
            }, {
                'type': 'week',
                'count': 1,
                'text': '1w'
            }, {
                'type': 'week',
                'count': 2,
                'text': '2w'
            }, {
                'type': 'month',
                'count': 1,
                'text': '1m'
            }, {
                'type': 'month',
                'count': 2,
                'text': '2m'
            }, {
                'type': 'all',
                'text': 'All'
            }]

        g.chart.zoomType = 'x'

        title = 'Open Interests for {} Roll {}: Current and Next Future'
        g.title.text = title.format(undl, rollKey)

        g.tooltip.split = True

        # g.xAxis.gridLineWidth = 1.0
        # g.xAxis.gridLineDashStyle = 'Dot'
        # g.yAxis.gridLineWidth = 1.0
        # g.yAxis.gridLineDashStyle = 'Dot'

        g.yAxis = [{
            'labels': {
                'align': 'right',
                'x': +25,
            },
            'title': {
                'text': 'Open Interest',
                'x': +40,
            },
            'lineWidth': 2,
        }]

        g.credits.enabled = True
        g.credits.text = 'Source: SG Markets | Futures Rollbox'
        g.credits.href = 'https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_02'


        g.series = [{
            'type': 'line',
            'name': 'Current Future',
            'data': Plot.build_series_data(df[['Current Future']]),
            'yAxis': 0,
        }, {
            'type': 'line',
            'name': 'Next Future',
            'data': Plot.build_series_data(df[['Next Future']]),
            'yAxis': 0,
        }, {
            'type': 'line',
            'name': 'Total',
            'data': Plot.build_series_data(df[['Total']]),
            'yAxis': 0,
        }]

        for k, v in kwargs.items():
            setattr(g, k, v)

        if save:
            # prepare save
            if not os.path.exists(folder_save):
                os.makedirs(folder_save)
            if not name:
                name = 'plot_price_evolution'

        html = g.html(save=save,
                      save_path=folder_save,
                      save_name=name,
                      dated=tagged,
                      notebook=False,
                      center=True)
        return df, html

    @staticmethod
    def relative_total_interest_analysis(dfi,
                                         undl,
                                         rollKey,
                                         save=False,
                                         folder_save='dump',
                                         name=None,
                                         tagged=True,
                                         x_axis_ordinal=False,
                                         **kwargs):
        """
        """
        msg = 'df must be a DataFrame'
        assert isinstance(dfi, pd.DataFrame), msg
        for e in ['date', 'ratio', 'delta']:
            msg = 'df must have column {}'.format(e)
            assert e in dfi, msg
        msg = 'column date must be datetime'
        assert dfi['date'].dtype.kind == 'M', msg

        df = dfi.set_index('date')

        g = hc.Highcharts()

        g.exporting.enabled = False
        g.chart.width = 900
        g.chart.height = 500
        g.legend.enabled = True
        g.legend.layout = 'horizontal'
        g.legend.align = 'center'
        g.legend.maxHeight = 100
        g.tooltip.enabled = True
        g.tooltip.valueDecimals = 2

        g.xAxis.ordinal = x_axis_ordinal
        g.xAxis.type = 'datetime'

        g.chart.zoomType = 'x'

        title = 'Total Open Interest for {} Roll {}'
        g.title.text = title.format(undl, rollKey)

        g.tooltip.shared = True

        g.yAxis = [{
            'title': {
                'text': 'Open Interest'
            },
            'lineWidth': 2,
        }, {
            'title': {
                'text': 'Delta'
            },
            'opposite': True,
            'lineWidth': 2,
            'min': 0,
        }]

        g.credits.enabled = True
        g.credits.text = 'Source: SG Markets | Futures Rollbox'
        g.credits.href = 'https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_02'


        g.series = [{
            'type': 'column',
            'name': 'delta',
            'data': Plot.build_series_data(df[['delta']]),
            'yAxis': 1,
        }, {
            'type': 'line',
            'name': 'ratio',
            'data': Plot.build_series_data(df[['ratio']]),
            'yAxis': 0,
        }]


        for k, v in kwargs.items():
            setattr(g, k, v)

        if save:
            # prepare save
            if not os.path.exists(folder_save):
                os.makedirs(folder_save)
            if not name:
                name = 'plot_price_evolution'

        html = g.html(save=save,
                      save_path=folder_save,
                      save_name=name,
                      dated=tagged,
                      notebook=False,
                      center=True)
        return df, html

    @staticmethod
    def build_grid(df,
                   folder_save='dump',
                   name_div='grid_div',
                   name_state='grid_state'):
        """
        """
        column_defs = [{'field': c} for c in df.columns]

        grid_options = {
            'columnDefs': column_defs,
        }
        g = Grid(grid_data=df.copy(),
                 width=700,
                 height=500,
                 grid_options=grid_options,
                 export_csv=True,
                 center=True)

        html_export = g.export_html()

        path = os.path.join(folder_save, name_div+'.html')
        with open(path, 'w') as f:
            f.write(html_export['grid_div'])

        path = os.path.join(folder_save, name_state+'.json')
        with open(path, 'w') as f:
            f.write(json.dumps(html_export['manager_state']))
