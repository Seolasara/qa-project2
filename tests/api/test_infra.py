import requests
import pytest


class TestInfraCRUD:
    """인프라 API 테스트 클래스"""

    def test_INFRA001_get_region_list_success(self, api_headers, base_url_infra):
        """
        INFRA-001: Region 목록 조회
        """
        headers = api_headers
        url = f"{base_url_infra}/region"

        response = requests.get(url, headers=headers)
        res_data = response.json()

        # 상태 코드 검증
        assert response.status_code == 200

        # 응답 타입 및 데이터 존재 여부
        assert isinstance(res_data, list), "Region 응답은 list 타입이어야 합니다."
        assert len(res_data) > 0, "Region 데이터가 존재해야 하지만 빈 리스트가 반환되었습니다."

        # 필수 필드 검증
        assert "id" in res_data[0], "Region 항목에 id 필드가 존재해야 합니다."
        assert "name" in res_data[0], "Region 항목에 name 필드가 존재해야 합니다."
        
    def test_INFRA002_get_zone_list_success(self, api_headers, base_url_infra):
        """
        INFRA-002: Zone 목록 조회
        """
        headers = api_headers
        url = f"{base_url_infra}/infra/zone"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()
        
        # 상태 코드 검증
        assert response.status_code == 200

        # 응답 타입 및 데이터 존재 여부
        assert isinstance(res_data, list)
        assert len(res_data) > 0, "Zone 데이터가 존재해야 하지만 빈 리스트가 반환되었습니다."

        # 필수 필드 검증
        assert "id" in res_data[0]
        assert "name" in res_data[0]
        assert "region_id" in res_data[0], "Zone 항목에 region_id 필드가 존재해야 합니다."
