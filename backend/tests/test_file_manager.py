import os
import json
import pytest
from unittest.mock import MagicMock

from Agents.FileManager import FileManager


def test_build_service_raises_when_no_credentials(monkeypatch, tmp_path):
    # Ensure env vars are not set
    monkeypatch.delenv('GOOGLE_SERVICE_ACCOUNT_PATH', raising=False)
    monkeypatch.delenv('GOOGLE_SERVICE_ACCOUNT_JSON', raising=False)

    fm = FileManager(name='fm')
    # _build_service should raise when no credentials are configured
    with pytest.raises(RuntimeError):
        fm._build_service()


def test_list_files_pagination(monkeypatch):
    # Create a FileManager and monkeypatch its _build_service to return a mock service
    fm = FileManager(name='fm')

    mock_service = MagicMock()
    # Prepare two pages of results
    resp_page1 = {'files': [{'id': '1', 'name': 'file_a'}], 'nextPageToken': 'token1'}
    resp_page2 = {'files': [{'id': '2', 'name': 'file_b'}], 'nextPageToken': None}

    # files().list(...).execute() should return page1 then page2
    mock_service.files.return_value.list.return_value.execute.side_effect = [resp_page1, resp_page2]

    # Monkeypatch the internal _build_service to return our mock
    monkeypatch.setattr(fm, '_build_service', lambda: mock_service)

    files = fm.list_files(q="trashed = false", page_size=50)

    assert isinstance(files, list)
    assert len(files) == 2
    assert files[0]['name'] == 'file_a'
    assert files[1]['name'] == 'file_b'


def test_get_file_count_pages(monkeypatch):
    fm = FileManager(name='fm')
    mock_service = MagicMock()

    # Simulate three pages of results
    resp1 = {'files': [{'id': '1'}], 'nextPageToken': 't1'}
    resp2 = {'files': [{'id': '2'}, {'id': '3'}], 'nextPageToken': 't2'}
    resp3 = {'files': [], 'nextPageToken': None}

    mock_service.files.return_value.list.return_value.execute.side_effect = [resp1, resp2, resp3]

    monkeypatch.setattr(fm, '_build_service', lambda: mock_service)

    count = fm.get_file_count(q="trashed = false")
    assert count == 3


def test_execute_dispatches_actions(monkeypatch):
    fm = FileManager(name='fm')

    # Mock underlying methods to verify execute routes correctly
    monkeypatch.setattr(fm, 'list_files', lambda q=None, page_size=100: [{'id': 'x'}])
    monkeypatch.setattr(fm, 'get_file_count', lambda q=None: 42)
    monkeypatch.setattr(fm, 'get_file_metadata', lambda file_id: {'id': file_id, 'name': 'meta'})

    res_list = fm.execute({'action': 'list_files'})
    assert 'files' in res_list and isinstance(res_list['files'], list)

    res_count = fm.execute({'action': 'count_files'})
    assert res_count.get('count') == 42

    res_get = fm.execute({'action': 'get_file', 'file_id': 'abc'})
    assert res_get['file']['id'] == 'abc'

    # list_folder should call list_files with a folder query
    monkeypatch.setattr(fm, 'list_files', lambda q=None, page_size=100: [{'id': 'in_folder'}])
    res_folder = fm.execute({'action': 'list_folder', 'folder_id': 'F123'})
    assert res_folder['files'][0]['id'] == 'in_folder'


# If you want to run these tests locally:
# python -m pytest backend/tests/test_file_manager.py -q
