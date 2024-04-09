import os
import json
from pr_agent.algo.utils import get_settings, github_output

class TestGitHubOutput:
    def test_github_output_enabled(self, monkeypatch, tmp_path):
        get_settings().set('GITHUB_ACTION_CONFIG.ENABLE_OUTPUT', True)
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = {'key1': {'value1': 1, 'value2': 2}}
        key_name = 'key1'
        
        github_output(output_data, key_name)
        
        with open(str(tmp_path / 'output'), 'r') as f:
            env_value = f.read()
        
        actual_key = env_value.split('=')[0]
        actual_data = json.loads(env_value.split('=')[1])
        
        assert actual_key == key_name
        assert actual_data == output_data[key_name]
    
    def test_github_output_disabled(self, monkeypatch, tmp_path):
        get_settings().set('GITHUB_ACTION_CONFIG.ENABLE_OUTPUT', False)
        monkeypatch.setenv('GITHUB_OUTPUT', str(tmp_path / 'output'))
        output_data = {'key1': {'value1': 1, 'value2': 2}}
        key_name = 'key1'
        
        github_output(output_data, key_name)
        
        assert not os.path.exists(str(tmp_path / 'output'))