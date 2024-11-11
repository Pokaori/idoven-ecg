from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.ecg import ECGCreate
from app.schemas.lead import LeadBase


def test_valid_ecg_data():
    """Test that valid ECG data passes validation"""
    data = {
        "leads": [
            {"name": "I", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
            {"name": "II", "signal": [1, 2, 3, 4, 5]},
        ],
        "date": date.today().isoformat(),
    }
    ecg = ECGCreate(**data)
    assert len(ecg.leads) == 2
    assert ecg.leads[0].name == "I"
    assert ecg.leads[1].name == "II"

@pytest.mark.parametrize("test_data,expected_error", [
    # Test missing date
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
                {"name": "II", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
            ],
        },
        "Field required",
    ),
    # Test missing signal
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
                {"name": "II", "sample_number": 250},
            ],
            "date": date.today().isoformat(),
        },
        "Field required",
    ),
    # Test invalid lead name
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
                {"name": "Invalid", "signal": [1, 2, 3, 4, 5], "sample_number": 250},
            ],
            "date": date.today().isoformat(),
        },
        "Input should be 'I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5' or 'V6'",
    ),
])
def test_invalid_ecg_data(test_data: dict, expected_error: str):
    """Test that invalid ECG data raises appropriate validation errors"""
    with pytest.raises(ValidationError) as exc_info:
         ECGCreate(**test_data)
    assert expected_error in exc_info.value.errors()[0]['msg']

def test_lead_data_validation():
    """Test LeadBase validation separately"""
    # Test valid lead data
    lead = LeadBase(name="I", signal=[1, 2, 3], sample_number=250)
    assert lead.name == "I"
    assert lead.signal == [1, 2, 3]
    assert lead.sample_number == 250

    # Test invalid lead name
    with pytest.raises(ValidationError) as exc_info:
        LeadBase(name="Invalid", signal=[1, 2, 3], sample_number=250)
    assert "Input should be" in str(exc_info.value)

    # Test invalid sampling rate
    with pytest.raises(ValidationError) as exc_info:
        LeadBase(name="I", signal=[1, 2, 3], sample_number=-1)
    assert "Input should be greater than 0" in str(exc_info.value) 