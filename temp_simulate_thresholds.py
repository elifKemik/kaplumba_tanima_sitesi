import random
from pathlib import Path
from agents.researcher import Researcher
from agents.identification_agent import IdentificationAgent

root = Path('data')
folders = ['t001', 't014']
researcher = Researcher()
model = IdentificationAgent()
random.seed(0)

for folder in folders:
    folder_path = root / folder
    if not folder_path.exists():
        print(folder, 'missing')
        continue
    files = sorted([p for p in folder_path.iterdir() if p.is_file()])
    print('\nFolder', folder, 'count', len(files))
    results = []
    for f in files:
        analysis = researcher.analyze(str(f))
        prediction = model.predict(str(f), analysis)
        results.append((f.name, analysis['status'], analysis['sharpness'], prediction['accuracy'], prediction['status']))
    for name, status, sharp, accuracy, ps in results[:10]:
        print(name, 'status=', status, 'sharpness=', round(sharp, 2), 'accuracy=', accuracy, 'pred=', ps)
    avg_acc = sum(r[3] for r in results) / len(results) if results else 0
    warn = sum(1 for r in results if r[1] == 'warning')
    fail = sum(1 for r in results if r[1] == 'fail')
    ident = sum(1 for r in results if r[4] == 'identified')
    print('summary:', 'avg_acc=', round(avg_acc, 2), 'warnings=', warn, 'fails=', fail, 'identified=', ident, 'of', len(results))
