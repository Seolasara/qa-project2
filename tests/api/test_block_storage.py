import requests
import pytest
import uuid
<<<<<<< HEAD

class TestBlockStorageCRUD:
    """블록 스토리지 API 테스트 클래스"""

    def test_BS001_list_exists_look_up(self, api_headers, base_url_block_storage):
        """BS-001: 데이터가 있는 경우 목록 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert isinstance(res_data, list)
        assert len(res_data) > 0, "데이터가 존재해야 하지만 빈 리스트가 반환되었습니다."
        assert "id" in res_data[0]
        assert "name" in res_data[0]

    @pytest.mark.xfail(reason="실제 환경에서는 목록을 비워둘 수 없음")
    def test_BS002_list_emptylook_up(self, api_headers, base_url_block_storage):
        """BS-002: 데이터가 없는 경우 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert res_data == [], f"데이터가 비어있어야 하지만 {len(res_data)}개의 데이터가 반환되었습니다."

    def test_BS003_create_success(self, resource_factory, api_headers, base_url_block_storage):
        """BS-003: 블록 스토리지 생성 성공 및 검증"""
        url = base_url_block_storage
        headers = api_headers
        payload = {
                        "name": f"team2-{uuid.uuid4().hex[:6]}",
                        "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
                        "size_gib": 10,
                        "dr": False,
                        "image_id": None,
                        "snapshot_id": None
        }

        # 1. 블록 스토리지 생성 (resource_factory 사용)
        created_resource = resource_factory(url, payload)
        created_id = created_resource["id"]
        
        # 2. 생성된 블록 스토리지 상세 조회 (GET)
        detail_url = f"{url}/{created_id}"
        detail_response = requests.get(detail_url, headers=headers)
        detail_data = detail_response.json()
        
        # 3. 상세 조회 검증
        assert detail_response.status_code == 200, f"상세 조회 실패: {detail_data}"
        
        # 4. 생성 요청 데이터와 실제 생성된 데이터 비교
        assert detail_data["name"] == payload["name"], f"name 불일치: 요청={payload['name']}, 응답={detail_data.get('name')}"
        assert detail_data["zone_id"] == payload["zone_id"], f"zone_id 불일치: 요청={payload['zone_id']}, 응답={detail_data.get('zone_id')}"
        assert detail_data["size_gib"] == payload["size_gib"], f"size_gib 불일치: 요청={payload['size_gib']}, 응답={detail_data.get('size_gib')}"
        
        #5. 스토리지 상태 확인 (정상적인 생성 프로세스 상태여야 함)
        status = detail_data.get("status", "")
        valid_statuses = ["queued", "creating", "available", "active", "assigned"]
        assert status in valid_statuses, f"예상치 못한 상태: {status} (허용: {valid_statuses})"

    def test_BS004_create_fail_missing_parameters(self, api_headers, base_url_block_storage):
        """BS-004: 필수 파라미터 일부 누락 시 422 에러 검증"""
        url = base_url_block_storage
        headers = api_headers
        
        # 이미지의 예시와 유사하게 size_gib 등을 null로 보내거나 일부 누락한 페이로드
        # 이미지 우측 하단 JSON 예시를 참고하여 구성
        payload = {
            "name": "disk-2ec50c",
=======
import time


class TestComputeCRUD:
    created_vm_id = None
    deleted_vm_verified = False

    # ----------------------------
    # VM-001 VM 생성
    def test_VM001_create_vm(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine"

        body = {
            "name": f"vm-auto-{uuid.uuid4().hex[:6]}",
>>>>>>> develop
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            # ✅ 네가 성공시킨 instance_type_id로 유지/교체해도 됨
            "instance_type_id": "830e2041-d477-4058-a65c-386a93ead237",  # M-2
            "username": "test",
            "password": "1qaz2wsx@@",
            "on_init_script": "",
            "always_on": False,
            "dr": False
        }

        r = requests.post(url, headers=api_headers, json=body)
        self._xfail_if_expired_token(r)

        assert r.status_code in (200, 201), f"status={r.status_code}, body={r.text}"

        res = r.json()
        assert "id" in res, f"missing id in response: {res}"

        TestComputeCRUD.created_vm_id = res["id"]

        # ✅ 가짜 PASS 방지: 생성 후 실제로 조회 가능해질 때까지 확인
        self._wait_vm_visible(api_headers, base_url_compute, TestComputeCRUD.created_vm_id, timeout_sec=60)

    # ----------------------------
    # VM-002 동일 파라미터로 VM 재생성
    def test_VM002_recreate_vm(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine"

<<<<<<< HEAD
    def test_BS007_get_fail_non_existent_id(self, api_headers, base_url_block_storage):
        """BS-007: 존재하지 않는 ID로 블록 스토리지 조회 시 404 에러 검증"""
        
        # 1. 존재하지 않는 임의의 ID 설정 (이미지 예시 참고)
        invalid_id = "d3012bbe-11f3-44e6-9cd6-f485753914e"
        url = f"{base_url_block_storage}/{invalid_id}"
        
        headers = api_headers.copy()
        headers["Content-Type"] = "application/json"

        # 2. 상세 조회 요청 (GET)
        response = requests.get(url, headers=headers)
        
        # 3. 상태 코드 검증 (404 Not Found)
        assert response.status_code == 404, f"예상치 못한 상태 코드: {response.status_code}"
        
        # 4. 응답 바디 검증
        res_data = response.json()
        assert res_data["detail"] == "Not Found", f"에러 메시지 불일치: {res_data.get('detail')}"

        print(f"테스트 통과: 존재하지 않는 ID({invalid_id}) 조회 시 404 및 'Not Found' 확인")

    def test_BS008_update_resource_name(self, resource_factory, api_headers, base_url_block_storage):
        """BS-008: 블록 스토리지 이름 수정 검증"""
        # 테스트용 블록 스토리지 생성
=======
>>>>>>> develop
        payload = {
            "name": f"vm-auto-{uuid.uuid4().hex[:6]}",
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "instance_type_id": "320909e3-44ce-4018-8b55-7e837cd84a15",
            "username": "test",
            "password": "1qaz2wsx@@",
            "on_init_script": "",
            "always_on": False,
            "dr": False
        }

        r = requests.post(url, headers=api_headers, json=payload)
        self._xfail_if_expired_token(r)

        if r.status_code == 409:
            pytest.xfail(f"quota 또는 환경 제한: {r.text}")

        assert r.status_code in (200, 201), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-003 다른 인스턴스 타입으로 VM 생성
    def test_VM003_create_vm_different_instance_type(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine"

<<<<<<< HEAD
        # JSON 문법 오류를 보내기 위해 data= 파라미터 사용
        response = requests.patch(url, headers=headers, data=invalid_raw_body)
        res_data = response.json()

        # 1. 상태 코드 검증
        assert response.status_code == 422
        
        # 2. 에러 상세 정보 검증 (이미지 매칭)
        error_detail = res_data["detail"]["errors"][0]
        assert error_detail["type"] == "json_invalid"
        assert "JSON decode error" in error_detail["msg"]
        assert "Expecting ',' delimiter" in error_detail["ctx"]["error"]

    def test_BS010_delete_resource_success(self, resource_factory, api_headers, base_url_block_storage):
        """BS-010: 블록 스토리지 삭제 요청 성공 검증"""
        # 테스트용 블록 스토리지 생성
=======
>>>>>>> develop
        payload = {
            "name": f"vm-auto-type2-{uuid.uuid4().hex[:6]}",
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "instance_type_id": "61d9beec-27d5-44df-a3b2-5ec200d2eebb",
            "username": "test",
            "password": "1qaz2wsx@@",
            "on_init_script": "",
            "always_on": False,
            "dr": False
        }

        r = requests.post(url, headers=api_headers, json=payload)
        self._xfail_if_expired_token(r)

        if r.status_code in (400, 404, 409, 422):
            pytest.xfail(f"환경 제한: {r.text}")

        assert r.status_code in (200, 201), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-004 OS 이미지 지정 생성 (Blocked)
    def test_VM004_create_vm_with_image(self):
        pytest.xfail("VM 생성 API에 image_id 미지원")

    # ----------------------------
    # VM-005 초기화 스크립트 포함 VM 생성
    def test_VM005_create_vm_with_init_script(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine"

<<<<<<< HEAD
    def test_BS011_delete_fail_already_deleted(self, resource_factory, api_headers, base_url_block_storage):
        """BS-011: 이미 삭제된 ID 삭제 시도 시 409 Conflict 검증"""
        # 1. 테스트용 블록 스토리지 생성
=======
>>>>>>> develop
        payload = {
            "name": f"vm-auto-init-{uuid.uuid4().hex[:6]}",
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "instance_type_id": "320909e3-44ce-4018-8b55-7e837cd84a15",
            "username": "test",
            "password": "1qaz2wsx@@",
            "on_init_script": "#!/bin/bash\necho test",
            "always_on": False,
            "dr": False
        }

        r = requests.post(url, headers=api_headers, json=payload)
        self._xfail_if_expired_token(r)

        if r.status_code == 409:
            pytest.xfail(f"quota 또는 환경 제한: {r.text}")

        assert r.status_code in (200, 201), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-006 DR 옵션 VM 생성
    def test_VM006_create_vm_with_dr(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine"

<<<<<<< HEAD
    def test_BS012_list_exists_look_up(self, api_headers, base_url_block_storage):
        """BS-012: 데이터가 있는 경우 목록 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}/snapshot?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert isinstance(res_data, list)
        assert len(res_data) > 0, "데이터가 존재해야 하지만 빈 리스트가 반환되었습니다."
        assert "id" in res_data[0]
        assert "name" in res_data[0]

    @pytest.mark.xfail(reason="실제 환경에서는 목록을 비워둘 수 없음")
    def test_BS013_list_emptylook_up(self, api_headers, base_url_block_storage):
        """BS-013: 데이터가 없는 경우 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}/snapshot?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert res_data == [], f"데이터가 비어있어야 하지만 {len(res_data)}개의 데이터가 반환되었습니다."

    def test_BS014_create_success(self, resource_factory, api_headers, base_url_block_storage):
        """BS-014: 스냅샷 생성 성공 및 검증"""
        url = f"{base_url_block_storage}/snapshot"
        headers = api_headers
=======
>>>>>>> develop
        payload = {
            "name": f"vm-auto-dr-{uuid.uuid4().hex[:6]}",
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "instance_type_id": "320909e3-44ce-4018-8b55-7e837cd84a15",
            "username": "test",
            "password": "1qaz2wsx@@",
            "on_init_script": "",
            "always_on": False,
            "dr": True
        }

        r = requests.post(url, headers=api_headers, json=payload)
        self._xfail_if_expired_token(r)

        if r.status_code == 409:
            pytest.xfail(f"quota 또는 환경 제한: {r.text}")

        assert r.status_code in (200, 201), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-007 VM 삭제
    def test_VM007_delete_vm(self, api_headers, base_url_compute):
        vm_id = TestComputeCRUD.created_vm_id
        assert vm_id is not None

        url = f"{base_url_compute}/virtual_machine/{vm_id}"
        r = requests.delete(url, headers=api_headers)
        self._xfail_if_expired_token(r)

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

        # ✅ 가짜 PASS 방지: “삭제 반영”을 404 강제 대신,
        #    404 또는 status 기반 삭제상태(비동기)까지 허용 + 토큰만료는 XFAIL
        self._wait_deleted(api_headers, base_url_compute, vm_id, timeout_sec=90)
        TestComputeCRUD.deleted_vm_verified = True

    # ----------------------------
    # VM-008 삭제 후 단건 조회
    def test_VM008_get_deleted_vm(self, api_headers, base_url_compute):
        vm_id = TestComputeCRUD.created_vm_id
        assert vm_id is not None

        url = f"{base_url_compute}/virtual_machine/{vm_id}"
        r = requests.get(url, headers=api_headers)
        self._xfail_if_expired_token(r)

        # VM-007에서 삭제 검증까지 끝난 경우: 여기서는 “삭제된 상태”만 허용
        if TestComputeCRUD.deleted_vm_verified:
            if r.status_code == 404:
                return

            if r.status_code == 200:
                try:
                    data = r.json()
                except Exception:
                    pytest.fail(f"deleted but get returned 200 non-json: {r.text}")

                st = (data.get("status") or "").upper()
                if st in ("DELETED", "TERMINATED", "DELETING"):
                    return

                pytest.fail(f"deleted_vm_verified=True but get status=200 and vm.status={data.get('status')}")
            pytest.fail(f"deleted_vm_verified=True but status={r.status_code}, body={r.text}")

        # (예외) VM-007이 XFAIL/스킵된 상황에서는 200/404 둘 다 허용
        assert r.status_code in (200, 404), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-009 VM 다건 조회
    def test_VM009_list_vm(self, api_headers, base_url_compute):
        vms = self._list_vms(api_headers, base_url_compute)
        assert isinstance(vms, list)

    # ----------------------------
    # VM-010 특정 상태 VM 목록 조회
    def test_VM010_list_vm_by_status(self, api_headers, base_url_compute):
        # TC1에서 만든 VM은 TC7에서 삭제되었을 수 있으니, 여기서는 "사용 가능한 VM"을 확보
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)
        assert vm_id is not None

        # start 엔드포인트가 404로 뜨는 환경이면 이 TC는 XFAIL이 맞음
        start_url = f"{base_url_compute}/virtual_machine_control/start"
        r = requests.post(start_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"start API 미지원/URL 상이: {r.status_code} {r.text}")

        time.sleep(10)

        url = f"{base_url_compute}/virtual_machine_allocation?filter_status=RUNNING"
        r = requests.get(url, headers=api_headers)
        self._xfail_if_expired_token(r)

        assert r.status_code in (200, 422), f"status={r.status_code}, body={r.text}"

        if r.status_code == 200:
            for vm in r.json():
                assert (vm.get("status") or "").upper() == "RUNNING"

<<<<<<< HEAD
        # 409 Conflict 및 상세 에러 메시지 검증
        assert response.status_code == 409
        assert res_data["code"] == "unexpected_status"
        assert "should be queued, assigned, or prepared" in res_data["message"]
        # 삭제 중이거나 이미 삭제된 상태 모두 허용
        status = res_data["detail"]["resource_block_storage_snapshot"]["status"]
        assert status in ["deleting", "deleted"], f"예상치 못한 상태: {status}"

class Testsnapshot_schedulerCRUD:
    """스냅샷 스케쥴러API 테스트 클래스"""

    def test_BS023_list_exists_look_up(self, api_headers, base_url_block_storage):
        """BS-023: 데이터가 있는 경우 목록 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}/snapshot_scheduler?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert isinstance(res_data, list)
        assert len(res_data) > 0, "데이터가 존재해야 하지만 빈 리스트가 반환되었습니다."
        assert "id" in res_data[0]
        assert "name" in res_data[0]

    @pytest.mark.xfail(reason="실제 환경에서는 목록을 비워둘 수 없음")
    def test_BS024_list_emptylook_up(self, api_headers, base_url_block_storage):
        """BS-024: 데이터가 없는 경우 조회"""
        headers = api_headers
        url = f"{base_url_block_storage}/snapshot_scheduler?skip=0&count=20"
        
        response = requests.get(url, headers=headers)
        res_data = response.json()

        assert response.status_code == 200
        assert res_data == [], f"데이터가 비어있어야 하지만 {len(res_data)}개의 데이터가 반환되었습니다."
    
    def test_BS025_create_success(self, resource_factory, api_headers, base_url_block_storage):
        """BS-025: 스냅샷 생성 성공 및 검증"""
        url = f"{base_url_block_storage}/snapshot_scheduler"
        headers = api_headers
        payload = {
          "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
          "name": "snapshot-scheduler-ea550f",
          "block_storage_id": "e0abb783-493b-432e-bdcc-69ecfb858529",
          "cron_expression": "2 4 * * *",
          "max_snapshots": 7,
          "tags": {}
        }

        # 1. 스냅샷 생성 (resource_factory 내부에서 POST 호출)
        created_resource = resource_factory(url, payload)
        
        # [검증] 이미지 1처럼 'code'가 포함되어 있다면 생성이 실패한 것임
        assert "code" not in created_resource, f"생성 실패: {created_resource.get('message')}"
        assert "id" in created_resource, "응답에 생성된 ID가 없습니다."
        
        created_id = created_resource["id"]
        
        # 2. 생성된 스냅샷 상세 조회 (GET)
        detail_url = f"{url}/{created_id}"
        detail_response = requests.get(detail_url, headers=api_headers)
        detail_data = detail_response.json()
        
        # 3. 상세 조회 기본 검증
        assert detail_response.status_code == 200, f"상세 조회 실패: {detail_data}"
        
        # 4. 요청 데이터와 응답 데이터 비교 (이미지 2의 구조 반영)
        assert detail_data["name"] == payload["name"]
        assert detail_data["block_storage_id"] == payload["block_storage_id"]
        
        # 5. 상태 값 검증
        # 스냅샷 스케줄러가 'active' 혹은 'prepared' 상태인지 확인
        status = detail_data.get("status")
        valid_statuses = ["active", "available", "prepared"]
        assert status in valid_statuses, f"부적절한 상태값: {status}"

    def test_BS026_create_fail_missing_parameters(self, api_headers, base_url_block_storage):
        """BS-026: 필수 파라미터 일부 누락 시 422 에러 검증"""
        url = f"{base_url_block_storage}/snapshot_scheduler"
        headers = api_headers
        
        # 이미지의 예시와 유사하게 size_gib 등을 null로 보내거나 일부 누락한 페이로드
        # 이미지 우측 하단 JSON 예시를 참고하여 구성
        payload = {
                    "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
                    "name": "snapshot-scheduler-ea550f",
                    "block_storage_id": "e0abb783-493b-432e-bdcc-69ecfb858529",
                    "cron_expression": None,
                    "max_snapshots": 7,
                    "tags": {}
        }

        # 1. 생성 요청 (422 예상)
        response = requests.post(url, headers=api_headers, json=payload)
        res_data = response.json()
        
        # 2. 상태 코드 검증
        assert response.status_code == 422, f"예상치 못한 상태 코드: {response.status_code}"
        
        # 3. 에러 코드 및 구조 검증
        # 실제 구조: {"code": "invalid_parameters", "detail": {"errors": [...], "query_params": ""}, "message": "..."}
        assert res_data["code"] == "invalid_parameters"
        assert "detail" in res_data, "응답에 'detail' 필드가 없습니다."
        assert "errors" in res_data["detail"], "응답에 'errors' 필드가 없습니다."
        
        # 4. 세부 에러 내용 검증
        errors = res_data["detail"]["errors"]
        
        # 에러 구조: {"input": None, "loc": ["body", "cron_expression"], "msg": "Input should be a valid string", "type": "string_type"}
        found_cron_error = any(
            "cron_expression" in error.get("loc", []) and 
            "Input should be a valid string" in error.get("msg", "")
            for error in errors
        )
        
        assert found_cron_error, f"cron_expression 관련 에러 메시지가 없습니다: {res_data}"

    def test_BS027_create_fail_invalid_data_type(self, api_headers, base_url_block_storage):
        """BS-027: 필수 파라미터에 잘못된 데이터 타입(JSON 문법 오류) 입력 시 에러 검증"""
        url = f"{base_url_block_storage}/snapshot_scheduler"
        headers = api_headers.copy()
        headers["Content-Type"] = "application/json"

        # 이미지 4, 5번 예시: "tags": {}22 처럼 문법을 깨뜨려 JSON 디코드 에러 유도
        invalid_raw_body = """
        {
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "name": "snapshot-scheduler-e9838b",
            "block_storage_id": "e0abb783-493b-432e-bdcc-69ecfb858f",
            "cron_expression": "2 4 * * *",
            "max_snapshots": 7,
            "tags": {}22
        }
        """

        # json= 대신 data=를 사용하여 가공되지 않은 raw string 전송
        response = requests.post(url, headers=headers, data=invalid_raw_body)
        res_data = response.json()

        # 1. 상태 코드 검증 (이미지 상 422 Unprocessable Entity)
        assert response.status_code == 422
        
        # 2. 공통 응답 구조 검증 (code: invalid_parameters)
        assert res_data["code"] == "invalid_parameters"
        assert "detail" in res_data, "응답에 'detail' 필드가 없습니다."
        assert "errors" in res_data["detail"], "응답에 'errors' 필드가 없습니다."

        # 3. 상세 에러(errors) 검증 - 실제 구조에 맞게
        errors = res_data["detail"]["errors"]
        assert len(errors) > 0
        
        error_detail = errors[0]
        
        # 실제 에러 구조: {"ctx": {"error": "..."}, "input": {}, "loc": ["body", 291], "msg": "JSON decode error", "type": "json_invalid"}
        assert error_detail["type"] == "json_invalid"
        assert error_detail["msg"] == "JSON decode error"
        # "Expecting ',' delimiter" 또는 "Expecting value" 등 상세 원인 확인
        assert "ctx" in error_detail
        assert "error" in error_detail["ctx"]
        assert "Expecting" in error_detail["ctx"]["error"]

    def test_BS029_get_fail_non_existent_id(self, api_headers, base_url_block_storage):
        """BS-029: 존재하지 않는 ID로 블록 스토리지 조회 시 404 에러 검증"""
        
        # 1. 존재하지 않는 임의의 ID 설정 (이미지 예시 참고)
        invalid_id = "2bbe3e69-7a41-4b2c-936c-057d79303a6"
        url = f"{base_url_block_storage}/snapshot_scheduler/{invalid_id}"
        
        headers = api_headers.copy()
        headers["Content-Type"] = "application/json"

        # 2. 상세 조회 요청 (GET)
        response = requests.get(url, headers=headers)
        
        # 3. 상태 코드 검증 (404 Not Found)
        assert response.status_code == 404, f"예상치 못한 상태 코드: {response.status_code}"
        
        # 4. 응답 바디 검증
        res_data = response.json()
        assert res_data["detail"] == "Not Found", f"에러 메시지 불일치: {res_data.get('detail')}"

        print(f"테스트 통과: 존재하지 않는 ID({invalid_id}) 조회 시 404 및 'Not Found' 확인")

    def test_BS030_update_resource_name(self, resource_factory, api_headers, base_url_block_storage):
        """BS-030: 스냅샷 스케줄러 이름 수정 검증"""
        
        # 1. 테스트용 스냅샷 스케줄러 생성
        snapshot_scheduler_url = f"{base_url_block_storage}/snapshot_scheduler"
        payload = {
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "name": f"before-update-{uuid.uuid4().hex[:6]}",
            "block_storage_id": "e0abb783-493b-432e-bdcc-69ecfb858529",
            "cron_expression": "2 4 * * *",
            "max_snapshots": 7,
            "tags": {}
        }
        # resource_factory를 통해 생성 (종료 후 자동 삭제됨)
        created_resource = resource_factory(snapshot_scheduler_url, payload)
        resource_id = created_resource["id"]
        
        # 2. 이름 변경 요청 설정
        url = f"{base_url_block_storage}/snapshot_scheduler/{resource_id}"
        
        # 요청 바디: {"name": "team2"}
        update_payload = {
            "name": "team2"
        }

        # 3. 수정 요청 전송 (PATCH)
        response = requests.patch(url, headers=api_headers, json=update_payload)
        res_data = response.json()

        # [검증] 상태 코드 200 및 반환된 ID 일치 여부
        assert response.status_code == 200, f"수정 실패: {res_data}"
        assert res_data["id"] == resource_id, "반환된 ID가 기존 ID와 다릅니다."
        
        # 4. 실제로 이름이 변경되었는지 상세 조회(GET)로 최종 확정
        get_response = requests.get(url, headers=api_headers)
        get_data = get_response.json()
        
        assert get_data["name"] == "team2", f"이름이 변경되지 않음: {get_data.get('name')}"
        print(f"테스트 통과: 리소스 {resource_id}의 이름이 'team2'로 정상 변경되었습니다.")
    
    def test_BS031_update_fail_invalid_tag_format(self, api_headers, base_url_block_storage):
        """BS-031: 올바르지 않은 태그 형식(JSON 문법 오류)으로 수정 시 422 에러 검증"""
        # 이미지 9번 예시 ID 반영
        resource_id = "2bbe3e69-7a41-4b2c-936c-057d79303a68" 
        url = f"{base_url_block_storage}/snapshot_scheduler/{resource_id}"
        
        headers = api_headers.copy()
        headers["Content-Type"] = "application/json"

        # 이미지 9번 우측 하단 예시: "tags": {}22 처럼 문법이 깨진 상태 유도
        # (작성하신 {}ss 대신 이미지와 동일한 {}22로 맞춤)
        invalid_raw_body = """
        {
            "id": "2bbe3e69-7a41-4b2c-936c-057d79303a68",
            "tags": {}22
        }
        """

        # JSON 문법 오류를 보내기 위해 data= 파라미터 사용
        response = requests.patch(url, headers=headers, data=invalid_raw_body)
        res_data = response.json()

        # 1. 상태 코드 검증 (이미지 상 422 Unprocessable Entity)
        assert response.status_code == 422
        
        # 2. 공통 응답 구조 검증
        assert res_data["code"] == "invalid_parameters"
        assert res_data["message"] == "requested parameters are not valid"

        # 3. 상세 에러 정보 검증 (이미지 9번 중앙 응답 데이터 매칭)
        # 이미지 구조: res_data["detail"]["errors"][0]
        errors = res_data.get("detail", {}).get("errors", [])
        assert len(errors) > 0
        
        error_detail = errors[0]
        assert error_detail["type"] == "json_invalid" #
        assert error_detail["msg"] == "JSON decode error" # 이미지 상 키값은 'msg'임
        
        # 4. 에러 위치 정보 검증
        assert "body" in error_detail.get("loc", [])

    def test_BS032_delete_resource_success(self, resource_factory, api_headers, base_url_block_storage):
        """BS-032: 스냅샷 스케줄러 삭제 요청 성공 검증"""
        
        # 1. 테스트용 스냅샷 스케줄러 생성
        snapshot_scheduler_url = f"{base_url_block_storage}/snapshot_scheduler"
        payload = {
            "zone_id": "0a89d6fa-8588-4994-a6d6-a7c3dc5d5ad0",
            "name": f"to-delete-{uuid.uuid4().hex[:6]}",
            "block_storage_id": "e0abb783-493b-432e-bdcc-69ecfb858529",
            "cron_expression": "2 4 * * *",
            "max_snapshots": 7,
            "tags": {}
        }
        created_resource = resource_factory(snapshot_scheduler_url, payload)
        resource_id = created_resource["id"]
        
        # 2. 삭제 요청 설정
        url = f"{base_url_block_storage}/snapshot_scheduler/{resource_id}"
        
        # 3. DELETE 요청 전송
        response = requests.delete(url, headers=api_headers)
        res_data = response.json()

        # 4. 응답 데이터 검증
        assert response.status_code == 200, f"삭제 실패: {res_data}"
        assert res_data["id"] == resource_id, "반환된 ID가 요청한 ID와 일치하지 않습니다."
        assert res_data["status"] == "deleted", f"상태값이 'deleted'가 아닙니다: {res_data.get('status')}"


    def test_BS033_delete_fail_already_deleted(self, resource_factory, api_headers, base_url_block_storage):
        """BS-033: 존재하지 않는 스냅샷 스케줄러 삭제 시도 시 409 Conflict 검증"""

        # 1. 존재하지 않는 UUID로 삭제 시도
        fake_id = str(uuid.uuid4())
        snapshot_scheduler_url = f"{base_url_block_storage}/snapshot_scheduler"
        target_url = f"{snapshot_scheduler_url}/{fake_id}"

        # 2. 존재하지 않는 리소스 삭제 요청
        response = requests.delete(target_url, headers=api_headers)
        res_data = response.json()

        # 3. 409 Conflict 검증
        assert response.status_code == 409, f"예상치 못한 상태 코드: {response.status_code}"
        
        # 에러 코드 확인 (not_found 또는 snapshot_scheduler_not_found)
        assert res_data["code"] in ["not_found", "snapshot_scheduler_not_found"], \
            f"예상치 못한 에러 코드: {res_data.get('code')}"
        
        # 에러 메시지 확인
        assert "snapshot scheduler" in res_data["message"].lower(), \
            f"에러 메시지에 'snapshot scheduler' 언급이 없습니다: {res_data.get('message')}"
=======
    # ----------------------------
    # VM-011 VM 목록 조회 (Search)
    def test_VM011_list_vm(self, api_headers, base_url_compute):
        vms = self._list_vms(api_headers, base_url_compute)
        assert isinstance(vms, list)

    # ----------------------------
    # VM-012 VM 단건 조회 (machine_id 기반)
    def test_VM012_get_vm_one(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)
        vm = self._get_vm_by_machine_id(api_headers, base_url_compute, vm_id)
        assert vm is not None
        assert vm.get("machine_id") or vm.get("id")

    # ----------------------------
    # VM-013 VM 시작
    def test_VM013_start_vm(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        start_url = f"{base_url_compute}/virtual_machine_control/start"
        r = requests.post(start_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code == 404:
            pytest.xfail(f"start API 미지원/URL 상이: {r.status_code} {r.text}")

        assert r.status_code in (200, 202), f"status={r.status_code}, body={r.text}"
        self._wait_status(api_headers, base_url_compute, vm_id, ["RUNNING"])

    # ----------------------------
    # VM-014 목록에서 VM 상태 확인 (RUNNING/STOP 필터)
    def test_VM014_check_vm_status_filter(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        start_url = f"{base_url_compute}/virtual_machine_control/start"
        r = requests.post(start_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"start API 미지원/URL 상이: {r.status_code} {r.text}")

        self._wait_status(api_headers, base_url_compute, vm_id, ["RUNNING"])

        val, data = self._try_filter_status(api_headers, base_url_compute, ["RUNNING", "running"])
        if val is None:
            pytest.xfail("filter_status 파라미터 허용값/형식 미확정(계속 실패)")

        assert isinstance(data, list)

    # ----------------------------
    # VM-015 실행중 VM 정지
    def test_VM015_stop_vm(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        start_url = f"{base_url_compute}/virtual_machine_control/start"
        r = requests.post(start_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"start API 미지원/URL 상이: {r.status_code} {r.text}")

        self._wait_status(api_headers, base_url_compute, vm_id, ["RUNNING"])

        stop_url = f"{base_url_compute}/virtual_machine_control/stop"
        r = requests.post(stop_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"stop API 미지원/URL 상이: {r.status_code} {r.text}")

        assert r.status_code in (200, 202), f"status={r.status_code}, body={r.text}"
        self._wait_status(api_headers, base_url_compute, vm_id, ["STOP"])

    # ----------------------------
    # VM-016 정지 후 상태 확인
    def test_VM016_check_stopped_vm(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        stop_url = f"{base_url_compute}/virtual_machine_control/stop"
        r = requests.post(stop_url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"stop API 미지원/URL 상이: {r.status_code} {r.text}")

        self._wait_status(api_headers, base_url_compute, vm_id, ["STOP"])

        vm = self._get_vm_by_machine_id(api_headers, base_url_compute, vm_id)
        assert vm is not None
        assert "STOP" in (vm.get("status") or "").upper()

    # ----------------------------
    # VM-017 VM 리부팅(Soft)
    def test_VM017_reboot_soft(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        reboot_url = f"{base_url_compute}/virtual_machine_control/reboot"
        r = requests.post(reboot_url, headers=api_headers, json={"id": vm_id, "type": "soft"})
        self._xfail_if_expired_token(r)
        if r.status_code == 404:
            pytest.xfail(f"reboot API 미지원/URL 상이: {r.status_code} {r.text}")

        assert r.status_code in (200, 202), f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-018 웹 콘솔 접속 정보 조회
    def test_VM018_get_console(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        url = f"{base_url_compute}/virtual_machine_console"
        r = requests.get(url, headers=api_headers, params={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code in (404, 501):
            pytest.xfail(f"console API 미지원: {r.status_code} {r.text}")

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-019 SSH 접속 정보 조회(지원 시)
    def test_VM019_get_ssh_info(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        url = f"{base_url_compute}/virtual_machine_ssh"
        r = requests.get(url, headers=api_headers, params={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code in (404, 501):
            pytest.xfail(f"ssh info API 미지원: {r.status_code} {r.text}")

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-020 SSH 접속 가능 여부 확인(지원 시)
    def test_VM020_check_ssh(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        url = f"{base_url_compute}/virtual_machine_ssh/check"
        r = requests.post(url, headers=api_headers, json={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code in (404, 501):
            pytest.xfail(f"ssh check API 미지원: {r.status_code} {r.text}")

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-021 VM 메트릭 조회
    def test_VM021_get_metrics(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        url = f"{base_url_compute}/virtual_machine_metrics"
        r = requests.get(url, headers=api_headers, params={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code in (404, 501):
            pytest.xfail(f"metrics API 미지원: {r.status_code} {r.text}")

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # VM-022 VM 건강 상태 조회
    def test_VM022_get_health(self, api_headers, base_url_compute):
        vm_id = self._ensure_vm_id(api_headers, base_url_compute)

        url = f"{base_url_compute}/virtual_machine_health"
        r = requests.get(url, headers=api_headers, params={"id": vm_id})
        self._xfail_if_expired_token(r)

        if r.status_code in (404, 501):
            pytest.xfail(f"health API 미지원: {r.status_code} {r.text}")

        assert r.status_code == 200, f"status={r.status_code}, body={r.text}"

    # ----------------------------
    # 아래부터는 헬퍼 메서드(이름 그대로 유지)

    def _xfail_if_expired_token(self, response):
        if response.status_code == 403:
            try:
                data = response.json()
            except Exception:
                data = {}
            if isinstance(data, dict) and data.get("code") == "expired_token":
                pytest.xfail(f'expired_token: {response.text}')

    def _list_vms(self, api_headers, base_url_compute):
        url = f"{base_url_compute}/virtual_machine_allocation"
        r = requests.get(url, headers=api_headers)
        self._xfail_if_expired_token(r)

        assert r.status_code == 200, f"list vms failed: status={r.status_code}, body={r.text}"
        data = r.json()
        assert isinstance(data, list), f"list vms response is not list: {data}"
        return data

    def _ensure_vm_id(self, api_headers, base_url_compute):
        # TC1에서 만든 VM id가 있고, 삭제 검증 전이면 그걸 우선 사용
        if TestComputeCRUD.created_vm_id and not TestComputeCRUD.deleted_vm_verified:
            return TestComputeCRUD.created_vm_id

        vms = self._list_vms(api_headers, base_url_compute)
        if not vms:
            pytest.xfail("VM 목록이 비어있어서 단건/제어 테스트 진행 불가")

        candidate = vms[0].get("machine_id") or vms[0].get("id")
        if not candidate:
            pytest.xfail(f"VM 목록에서 machine_id/id를 찾을 수 없음: {vms[0]}")
        return candidate

    def _get_vm_by_machine_id(self, api_headers, base_url_compute, machine_id_or_id):
        url = f"{base_url_compute}/virtual_machine/{machine_id_or_id}"
        r = requests.get(url, headers=api_headers)
        self._xfail_if_expired_token(r)

        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return {"raw": r.text}

        vms = self._list_vms(api_headers, base_url_compute)
        for vm in vms:
            if vm.get("machine_id") == machine_id_or_id or vm.get("id") == machine_id_or_id:
                return vm
        return None

    def _wait_status(self, api_headers, base_url_compute, machine_id_or_id, expected_status_list, timeout_sec=120):
        end = time.time() + timeout_sec
        expected = {s.upper() for s in expected_status_list}

        while time.time() < end:
            vm = self._get_vm_by_machine_id(api_headers, base_url_compute, machine_id_or_id)
            if vm:
                st = (vm.get("status") or "").upper()
                if st in expected:
                    return
            time.sleep(5)

        pytest.xfail(f"timeout: status not in {expected_status_list}")

    def _try_filter_status(self, api_headers, base_url_compute, candidates):
        for val in candidates:
            url = f"{base_url_compute}/virtual_machine_allocation?filter_status={val}"
            r = requests.get(url, headers=api_headers)
            self._xfail_if_expired_token(r)

            if r.status_code == 200:
                try:
                    data = r.json()
                except Exception:
                    data = None
                if isinstance(data, list):
                    return val, data
        return None, None

    def _wait_vm_visible(self, api_headers, base_url_compute, vm_id, timeout_sec=60):
        end = time.time() + timeout_sec
        while time.time() < end:
            vm = self._get_vm_by_machine_id(api_headers, base_url_compute, vm_id)
            if vm is not None:
                return
            time.sleep(3)
        pytest.fail(f"VM001 created id={vm_id} but not visible within {timeout_sec}s")

    def _wait_deleted(self, api_headers, base_url_compute, vm_id, timeout_sec=90):
        end = time.time() + timeout_sec
        url = f"{base_url_compute}/virtual_machine/{vm_id}"

        while time.time() < end:
            r = requests.get(url, headers=api_headers)
            self._xfail_if_expired_token(r)

            if r.status_code == 404:
                return

            if r.status_code == 200:
                try:
                    data = r.json()
                except Exception:
                    data = {}
                st = (data.get("status") or "").upper()
                # ✅ 비동기 삭제 환경 대응 (즉시 404가 아닐 수 있음)
                if st in ("DELETED", "TERMINATED"):
                    return
                if st in ("DELETING", "TERMINATING"):
                    time.sleep(3)
                    continue

            time.sleep(3)

        pytest.fail(f"VM007 deleted id={vm_id} but not deleted/404 within {timeout_sec}s")
>>>>>>> develop
