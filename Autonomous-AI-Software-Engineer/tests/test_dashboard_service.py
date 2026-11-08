import json
from unittest.mock import patch
import pytest
from frontend.service import analyze_code, save_report

def test_empty_code_rejected():
    with pytest.raises(ValueError):
        analyze_code('  ')

def test_static_review_uses_tools_without_executing_code():
    with patch('tools.code_analyzer.ruff_analyzer', return_value=[{'code':'F821'}]), patch('tools.code_analyzer.security_analyzer', return_value=[]):
        result = analyze_code('print(undefined_variable)')
    assert result['counts'] == {'syntax': 0, 'quality': 1, 'security': 0}
    assert result['code_executed'] is False

def test_missing_tool_gracefully_degrades():
    with patch('tools.code_analyzer.ruff_analyzer', side_effect=FileNotFoundError('ruff missing')), patch('tools.code_analyzer.security_analyzer', return_value=[]):
        result = analyze_code('print(1)')
    assert result['status'] == 'partial'
    assert 'ruff' in result['tool_errors']

def test_report_save(tmp_path, monkeypatch):
    import frontend.service as service
    monkeypatch.setattr(service, 'REPORTS', tmp_path)
    path = save_report({'status':'completed'})
    assert json.loads(path.read_text())['status'] == 'completed'
