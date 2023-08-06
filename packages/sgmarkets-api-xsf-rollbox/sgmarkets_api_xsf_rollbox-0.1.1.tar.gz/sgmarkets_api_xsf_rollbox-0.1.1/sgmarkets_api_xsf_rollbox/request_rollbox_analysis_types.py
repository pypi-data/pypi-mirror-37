
from timeit import default_timer as timer
from IPython.display import Markdown

from ._util import Util
from .response_rollbox_analysis_types import ResponseRollboxAnalysisTypes


class RequestRollboxAnalysisTypes:
    """
    """

    def __init__(self,
                 li_undl=None):
        """
        """
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/frb',
                   'endpoint': '/v1/analysis-types'}
        self.url = Util.build_url(dic_url)


    def info(self):
        """
        """
        md = """
A RequestRollboxUnderlyings object has the properties:
+ `url`: {}

and the methods:
+ `call_api()` to make the request to the url
        """.format(self.url)
        return Markdown(md)

    def call_api(self,
                 api,
                 debug=False):
        """
        See https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Analyse/Analysis_01
        """
        t0 = timer()
        print('calling API...')
        raw_response = api.get(self.url)
        t1 = timer()
        print('done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseRollboxAnalysisTypes(raw_response)
        return response
