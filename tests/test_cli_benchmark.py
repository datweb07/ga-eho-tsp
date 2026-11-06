from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys

from ga_eho_tsp.cli import main
from ga_eho_tsp.experiments.benchmark import benchmark

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/legacy/03Cities-6.txt'


def test_cli_subprocess_headless(tmp_path):
    output = tmp_path / 'result.json'
    environment = dict(os.environ, PYTHONPATH=str(ROOT/'src'), PYTHONIOENCODING='utf-8')
    result = subprocess.run([sys.executable,'-m','ga_eho_tsp.cli','solve','--algorithm','ga',
        '--dataset',str(DATA),'--generations','3','--json',str(output)],capture_output=True,text=True,encoding='utf-8',env=environment)
    assert result.returncode == 0, result.stderr
    assert 'distance=6' in result.stdout
    record = json.loads(output.read_text(encoding='utf-8'))
    assert record['best_route'][0] == 0 and len(record['best_route']) == 3
    assert record['iterations_completed'] == 3


def test_cli_errors_and_validate(capsys,tmp_path):
    assert main(['validate','--dataset',str(DATA)]) == 0
    assert main(['validate','--dataset',str(tmp_path/'missing')]) == 2
    assert main(['solve','--dataset',str(DATA),'--mutation-rate','-1']) == 2
    assert main(['solve','--dataset',str(DATA),'--algorithm','eho']) == 2
    assert 'not implemented' in capsys.readouterr().out


def test_benchmark_exports(tmp_path):
    config = tmp_path/'config.json'
    config.write_text(json.dumps({'seeds':[11,23,37,53,71], 'datasets':[str(DATA)],
        'ga':{'population_size':5,'generations':2},'output_dir':'output'}))
    report = benchmark(config)
    assert report['summary'][0]['distance_mean'] == 6
    assert report['summary'][0]['distance_std'] == 0
    assert len((tmp_path/'output/raw.csv').read_text().splitlines()) == 6
    assert len(list((tmp_path/'output').glob('03Cities-6-*.json'))) == 5


def test_benchmark_keeps_failures(tmp_path, monkeypatch):
    import importlib
    module = importlib.import_module('ga_eho_tsp.experiments.benchmark')
    def fail(*args, **kwargs):
        raise ValueError('injected failure for test')
    monkeypatch.setattr(module, 'solve', fail)
    config = tmp_path/'config.json'
    config.write_text(json.dumps({'seeds':[11,23,37,53,71], 'datasets':[str(DATA)],
        'ga':{'population_size':5,'generations':2},'output_dir':'output'}))
    report = benchmark(config)
    assert report['failed_runs'] == 5
    assert report['summary'][0]['distance_mean'] is None
    assert (tmp_path/'output/raw.csv').read_text().count('FAILED') == 5
