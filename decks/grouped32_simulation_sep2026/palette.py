"""High-contrast orange foregrounds; darker orange only for filled accents."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def tokens():
    data = json.loads((ROOT.parents[1] / 'templates/dune-professional/design-tokens.json').read_text())
    data['colors']['primary']['hex'] = data['colors']['editorial-accent-deep']['hex']
    data['colors']['editorial-accent']['hex'] = data['colors']['coral']['hex']
    return data

def colors():
    return {key: value['hex'] for key, value in tokens()['colors'].items()}

if __name__ == '__main__':
    (ROOT / 'design-tokens.json').write_text(json.dumps(tokens(), indent=2) + '\n')
