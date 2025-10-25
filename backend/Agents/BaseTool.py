from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pathlib import Path
import hashlib
import json
import os
from datetime import datetime


class BaseTool(ABC):
	"""Abstract base class for tools used by agents.

	Provide common helpers and a simple execution contract so concrete
	tools can focus on their specific logic (e.g., listing files,
	detecting duplicates, reading metadata, categorization).
	"""

	def __init__(self, name: str, description: str, supported_file_types: Optional[List[str]] = None):
		self.name = name
		self.description = description
		# normalized suffixes like ['.docx', '.pdf']
		self.supported_file_types = [ft.lower() for ft in (supported_file_types or [])]

	@abstractmethod
	def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		"""Run the tool's main action.

		Args:
			payload: structured input for the tool (depends on tool)

		Returns:
			A dictionary with structured results.
		"""

	def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
		"""Validate payload, execute tool logic, and format the output.

		This is the method an agent should call to use the tool.
		It wraps `execute` with basic validation and error handling.
		"""
		# Basic validation hook
		self._validate_payload(payload)

		try:
			result = self.execute(payload)
		except Exception as e:
			return {"ok": False, "error": str(e)}

		# Ensure the result is serializable and well-formed
		return self._format_result(result)

	def _validate_payload(self, payload: Dict[str, Any]) -> None:
		"""Basic payload validation; subclasses can override for stricter checks."""
		if not isinstance(payload, dict):
			raise TypeError("payload must be a dict")

	def _format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
		"""Ensure result is JSON-serializable and add metadata."""
		try:
			json.dumps(result)
		except Exception:
			# Fallback: convert non-serializable pieces to strings
			safe = {k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v)) for k, v in result.items()}
			result = safe

		# add a basic ok flag if missing
		if "ok" not in result:
			result = {"ok": True, **result}

		# add timestamp
		result.setdefault("generated_at", datetime.utcnow().isoformat() + "Z")
		return result

	# --- Helper utilities that many tools will need ---
	def read_text_file(self, path: str, encoding: str = "utf-8") -> str:
		p = Path(path)
		if not p.exists():
			raise FileNotFoundError(path)
		return p.read_text(encoding=encoding)

	def compute_md5(self, path: str) -> str:
		"""Compute md5 checksum for a local file."""
		h = hashlib.md5()
		with open(path, "rb") as f:
			for chunk in iter(lambda: f.read(8192), b""):
				h.update(chunk)
		return h.hexdigest()

	def file_metadata(self, path: str) -> Dict[str, Any]:
		p = Path(path)
		if not p.exists():
			raise FileNotFoundError(path)
		stat = p.stat()
		return {
			"path": str(p),
			"name": p.name,
			"suffix": p.suffix.lower(),
			"size": stat.st_size,
			"modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
			"created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
		}

	def is_supported_file(self, path: str) -> bool:
		if not self.supported_file_types:
			return True
		return Path(path).suffix.lower() in self.supported_file_types


