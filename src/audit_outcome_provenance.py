"""Read-only consistency audit of existing simulator traces, not a new experiment."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    files = sorted((ROOT / 'analysis/validation-v1').glob('*.json'))
    checked = steps = 0
    failures = []
    inputs = []
    for path in files:
        raw = path.read_bytes()
        obj = json.loads(raw)
        if not isinstance(obj, dict) or 'episodes' not in obj:
            continue
        inputs.append({'file': path.relative_to(ROOT).as_posix(),
                       'sha256': hashlib.sha256(raw).hexdigest()})
        for episode in obj['episodes']:
            targets = set(episode['protected_targets'])
            impacts = {row['observed']['target'] for row in episode['trace']
                       if row['observed']['action'] == 'impact'
                       and row['observed']['success']
                       and row['observed']['target'] in targets}
            expected = 1 - len(impacts) / len(targets) if targets else None
            if expected is None or abs(expected - episode['protection']) > 1e-12 or impacts != set(episode['impacted_targets']):
                failures.append({'file': path.name, 'episode': episode['episode']})
            checked += 1
            steps += len(episode['trace'])
    if not checked:
        raise RuntimeError('No episode traces found')
    report = {'scope': 'Internal consistency of existing simulator metadata only; no defender-visibility or real-world validation',
              'world_files': len(inputs), 'episodes_checked': checked,
              'trace_steps_checked': steps, 'failures': failures, 'inputs': inputs}
    output = ROOT / 'analysis/outcome-provenance-audit.json'
    output.write_bytes((json.dumps(report, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({k: v for k, v in report.items() if k != 'inputs'}, indent=2))
    if failures:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
