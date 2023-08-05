from unittest.mock import Mock

import pandas as pd
import pytest

from ctexplorer.data_processing import load_plate_layout, load_field_layout


sample_objects = {
    'one': pd.DataFrame({
        'Well': ['A1', 'B3', 'H12'],
        'Field': [1, 4, 2],
        'Left': [10, 14, 22],
        'Top': [11, 12, 25]
    }),
    'two': pd.DataFrame({
        'Well': ['A3', 'B4', 'H11'],
        'Field': [10, 14, 22],
        'Left': [100, 214, 322],
        'Top': [112, 122, 252]
    }),
    'three': pd.DataFrame({
        'Well': ['A11', 'B11', 'G12'],
        'Field': [11, 14, 12],
        'Left': [110, 114, 212],
        'Top': [111, 112, 125]
    }),
}

radio_button_text = {'one': 'Stitched image',
                     'two': 'Stitched image',
                     'three': 'Stitched image'}


@pytest.fixture(params=['one', 'two', 'three'])
def sample_object(request):
    sample_object = Mock()
    sample_object.data = sample_objects[request.param]
    sample_object.spinBox_resolution = Mock()
    sample_object.spinBox_resolution.value = Mock(return_value=0)
    sample_object.spinBox_resolution.setValue = Mock(return_value=None)
    sample_object.tp = Mock(return_value=None)
    sample_object.comboBox_x_col.currentText = Mock(return_value='Left')
    sample_object.comboBox_y_col.currentText = Mock(return_value='Top')
    load_plate_layout(sample_object)
    load_field_layout(sample_object, radio_button_text[request.param])
    return sample_object, request.param
