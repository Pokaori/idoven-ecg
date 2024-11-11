from datetime import date

import pytest
from httpx import AsyncClient

from app.models.user import User


@pytest.mark.parametrize("test_data,expected_status", [
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sampling_rate": 250},
                {"name": "II", "signal": [1, 2, 3, 4, 5], "sampling_rate": 250},
            ],
        },
        422  # Missing date
    ),
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sampling_rate": 250},
                {"name": "II", "sampling_rate": 250},  # Missing signal
            ],
            "date": date.today().isoformat(),
        },
        422
    ),
    (
        {
            "leads": [
                {"name": "I", "signal": [1, 2, 3, 4, 5], "sampling_rate": 250},
                {"name": "V", "signal": [1, 2, 3, 4, 5], "sampling_rate": 250},  # Invalid lead name
            ],
            "date": date.today().isoformat(),
        },
        422
    ),
])
@pytest.mark.asyncio
async def test_invalid_ecg_data(
    client: AsyncClient,
    authenticated_user: tuple[User, str, str],
    test_data: dict,
    expected_status: int,
):
    """Test validation of invalid ECG data submissions"""
    _, access_token, _ = authenticated_user
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/api/v1/ecg", json=test_data, headers=headers)
    assert response.status_code == expected_status
