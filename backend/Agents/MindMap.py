from __future__ import annotations

from .BaseTool import BaseTool
from typing import Any, Dict, List, Optional
from pathlib import Path
import json
import uuid
import math
import matplotlib.pyplot as plt


class MindMap(BaseTool):

    """
    Mind Map generator. 
    A tool for Gemini to give inputs to and it generates a mind map for the user to visualize their file usage.
    The bigger the files, the bigger the bubbles are.
    Goal is so that it can be organized by file type, category, size, and date. 
    """

    def __init__(self, task: str = "File type mind map"):

        super().__init__(
            name="Mind Map Generator", 
            description="An automated tool that outputs an image for users to visualize their file system", 
            supported_file_types=[".json"]
        )

        self.task = task

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Main executor for MindMap tool.

        payload may include:
          - json_path: path to a JSON file with data
          - data: a Python dict representing the JSON
          - map_type: one of ['file_type','file_name','file_size','file_category']
          - output_path: optional path to save image

        The JSON is expected to contain a list of files under either
        'CategorizedFileList' or 'files' where each item is a dict with
        keys like name, size, mimeType, category.
        """
        # Load input data
        data = None
        if 'data' in payload and payload['data']:
            data = payload['data']
        elif 'json_path' in payload and payload['json_path']:
            jp = payload['json_path']
            text = self.read_text_file(jp)
            data = json.loads(text)
        else:
            raise ValueError('payload must include data or json_path')

        map_type = payload.get('map_type', 'file_type')
        output_path = payload.get('output_path')

        # Extract file list from common keys
        files = []
        if isinstance(data, dict):
            if 'CategorizedFileList' in data and isinstance(data['CategorizedFileList'], list):
                files = data['CategorizedFileList']
            elif 'files' in data and isinstance(data['files'], list):
                files = data['files']
            elif 'files' in data and isinstance(data['files'], dict) and 'files' in data['files']:
                files = data['files']['files']
            elif 'Message' in data and isinstance(data['Message'], str):
                # no structured file list; return the message as a single node
                files = [{'name': 'message', 'size': 0, 'category': None}]
            else:
                # try to find any list-like value
                for v in data.values():
                    if isinstance(v, list):
                        files = v
                        break
        elif isinstance(data, list):
            files = data

        # Normalize file entries
        normalized = []
        for f in files:
            if not isinstance(f, dict):
                continue
            name = f.get('name') or f.get('file_name') or f.get('id') or 'unnamed'
            size = f.get('size') or f.get('bytes') or 0
            # try to coerce size
            try:
                size = int(size)
            except Exception:
                size = 0
            mime = f.get('mimeType') or ''
            category = f.get('category') or f.get('Category') or f.get('label') if isinstance(f.get('category') or f.get('Category') or f.get('label'), str) else None
            normalized.append({'name': name, 'size': size, 'mime': mime, 'category': category})

        if not normalized:
            raise ValueError('No files found in provided data')

        # Aggregate according to map_type
        groups = {}
        if map_type == 'file_type':
            for f in normalized:
                ext = Path(f['name']).suffix.lower() or (f['mime'].split('/')[-1] if f['mime'] else 'unknown')
                groups.setdefault(ext or 'unknown', {'count': 0, 'size': 0}).update({
                    'count': groups.get(ext, {'count': 0})['count'] + 1,
                    'size': groups.get(ext, {'size': 0})['size'] + f['size']
                })
        elif map_type == 'file_name':
            # group by first token of filename (e.g., project prefix)
            for f in normalized:
                token = f['name'].split('_')[0] if '_' in f['name'] else f['name'].split()[0]
                groups.setdefault(token, {'count': 0, 'size': 0})
                groups[token]['count'] += 1
                groups[token]['size'] += f['size']
        elif map_type == 'file_size':
            # bucket sizes into ranges
            def bucket(sz: int) -> str:
                if sz == 0:
                    return '0'
                exp = int(math.floor(math.log10(max(1, sz))))
                base = 10 ** exp
                return f"{base:,}~"

            for f in normalized:
                b = bucket(f['size'])
                groups.setdefault(b, {'count': 0, 'size': 0})
                groups[b]['count'] += 1
                groups[b]['size'] += f['size']
        elif map_type == 'file_category':
            for f in normalized:
                cat = f.get('category') or 'uncategorized'
                groups.setdefault(cat, {'count': 0, 'size': 0})
                groups[cat]['count'] += 1
                groups[cat]['size'] += f['size']
        else:
            raise ValueError(f'Unsupported map_type: {map_type}')

        # Prepare bubble chart
        labels = list(groups.keys())
        counts = [groups[k]['count'] for k in labels]
        sizes = [groups[k]['size'] for k in labels]

        # scale sizes for plotting (avoid zero-size bubbles)
        max_size = max(sizes) if sizes else 1
        plot_sizes = [max(50, int((s / max_size) * 2000)) for s in sizes]

        x = list(range(len(labels)))
        y = [0] * len(labels)

        fig, ax = plt.subplots(figsize=(max(6, len(labels) * 1.2), 6))
        scatter = ax.scatter(x, y, s=plot_sizes, alpha=0.6)

        # annotate labels
        for xi, yi, lbl, cnt in zip(x, y, labels, counts):
            ax.text(xi, yi, f"{lbl}\n{cnt}", ha='center', va='center', fontsize=8)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"Mind Map - {map_type}")

        # Save image
        if not output_path:
            out_name = f"mindmap_{map_type}_{uuid.uuid4().hex[:8]}.png"
            output_path = str(Path.cwd() / out_name)

        fig.savefig(output_path, bbox_inches='tight')
        plt.close(fig)

        return {'image_path': output_path, 'groups': groups}

    # Backwards-compatible wrapper
    def process_task(self, fileName: str = ".json") -> Dict[str, Any]:
        return self.execute({'json_path': fileName, 'map_type': self.task})  