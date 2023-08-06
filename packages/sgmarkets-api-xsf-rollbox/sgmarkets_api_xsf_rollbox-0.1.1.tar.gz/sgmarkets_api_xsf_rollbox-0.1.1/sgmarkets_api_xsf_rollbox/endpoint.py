
from ._obj_from_dict import ObjFromDict

from .request_rollbox_underlyings import RequestRollboxUnderlyings
from .response_rollbox_underlyings import ResponseRollboxUnderlyings

from .request_rollbox_relative_roll import RequestRollboxRelativeRoll
from .response_rollbox_relative_roll import ResponseRollboxRelativeRoll

from .request_rollbox_analysis_types import RequestRollboxAnalysisTypes
from .response_rollbox_analysis_types import ResponseRollboxAnalysisTypes

from .request_rollbox_analysis import RequestRollboxAnalysis
from .response_rollbox_analysis import ResponseRollboxAnalysis


dic_endpoint = {
    'v1_underlyings': {
        'request': RequestRollboxUnderlyings,
        'response': ResponseRollboxUnderlyings,
    },
    'v1_relative_roll': {
        'request': RequestRollboxRelativeRoll,
        'response': ResponseRollboxRelativeRoll,
    },
    'v1_analysis_types': {
        'request': RequestRollboxAnalysisTypes,
        'response': ResponseRollboxAnalysisTypes,
    },
    'v1_analysis': {
        'request': RequestRollboxAnalysis,
        'response': ResponseRollboxAnalysis,
    },
    # to add new endpoint here after creating the corresponding
    # Request Response and optionally Slice objects
}

endpoint = ObjFromDict(dic_endpoint)
