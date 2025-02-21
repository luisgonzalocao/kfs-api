from kfs.services.search_service import SearchService
from kfs.settings import settings


def test_search_service_with_test_mode(monkeypatch):
    """Tests that SearchService works correctly in TEST mode with FakeClient."""

    # Simula CLIENT_MODE = "TEST"
    monkeypatch.setattr(settings, "CLIENT_MODE", "TEST")

    # Inicializa el SearchService con la fecha, origen y destino
    search_service = SearchService(date_str="2025-03-10", origin="BUE", destination="MAD")

    # Resultados esperados
    expected_result = [
        {
            "connections": 0,
            "path": [
                {
                    "flight_number": "XX1001",
                    "from": "BUE",
                    "to": "MAD",
                    "departure_time": "2025-03-10 12:00",
                    "arrival_time": "2025-03-10 23:00"
                }
            ]
        },
        {
            "connections": 1,
            "path": [
                {
                    "flight_number": "XX1003",
                    "from": "BUE",
                    "to": "NYC",
                    "departure_time": "2025-03-10 14:00",
                    "arrival_time": "2025-03-11 04:00"
                },
                {
                    "flight_number": "XX1004",
                    "from": "NYC",
                    "to": "MAD",
                    "departure_time": "2025-03-11 06:00",
                    "arrival_time": "2025-03-11 09:00"
                }
            ]
        }
    ]

    # Obtén los resultados del servicio
    result = search_service.get_response()
    # Compara el resultado con los resultados esperados
    assert result == expected_result
