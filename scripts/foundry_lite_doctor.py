#!/usr/bin/env python3
"""Read-only, zero-model Foundry Lite laptop readiness diagnosis.

No cloud API calls, installations, model downloads, token use or schedules.
Optional --check-local checks only loopback Ollama /api/tags (not inference).
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

GIB = 1024 ** 3
OLLAMA_DOWNLOAD = "https://ollama.com/download"


def physical_ram_bytes(system: str) -> int | None:
    try:
        if system == "Linux":
            with open("/proc/meminfo", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("MemTotal:"):
                        return int(line.split()[1]) * 1024
        if system == "Darwin":
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], capture_output=True,
                text=True, timeout=3, check=True,
            )
            return int(result.stdout.strip())
        if system == "Windows":
            # Windows is optional, never require external packages.
            import ctypes
            from ctypes import wintypes

            class Status(ctypes.Structure):
                _fields_ = [
                    ("dwLength", wintypes.DWORD),
                    ("dwMemoryLoad", wintypes.DWORD),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = Status()
            status.dwLength = ctypes.sizeof(Status)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
    except (OSError, ValueError, subprocess.SubprocessError, AttributeError):
        return None
    return None


def get_local_models() -> tuple[str, list[str]]:
    """GET local-only /api/tags, forbid redirects and environment proxy."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            raise ValueError("redirect_refused")

    opener = urllib.request.build_opener(NoRedirect, urllib.request.ProxyHandler({}))
    try:
        with opener.open("http://127.0.0.1:11434/api/tags", timeout=2.5) as response:
            if response.status != 200:
                return "not_ready", []
            payload = response.read(32769)
        if len(payload) > 32768:
            return "response_too_large", []
        parsed = json.loads(payload)
        models = parsed.get("models", []) if isinstance(parsed, dict) else []
        if not isinstance(models, list):
            return "unexpected_reply", []
        names = [x.get("name") for x in models if isinstance(x, dict)
                 and isinstance(x.get("name"), str)]
        return "local_service_ready", names[:30]
    except Exception:
        # Never log potentially sensitive local-service errors or URLs.
        return "local_service_unavailable", []


def diagnose(*, system: str | None = None, python: tuple[int, int] | None = None,
             ram: int | None = None, disk: int | None = None,
             ollama_executable: str | None = None, check_local: bool = False,
             local_probe=None) -> dict[str, Any]:
    system = system or platform.system()
    python = python or (sys.version_info.major, sys.version_info.minor)
    if ram is None:
        ram = physical_ram_bytes(system)
    if disk is None:
        try:
            disk = shutil.disk_usage(Path.cwd()).free
        except OSError:
            disk = None
    if ollama_executable is None:
        ollama_executable = shutil.which("ollama")
    py_ok = python >= (3, 10)
    local_state, models = ("not_checked", [])
    if check_local:
        local_state, models = (local_probe or get_local_models)()
    if not isinstance(models, list):
        models = []
    # An informational heuristic, not a guarantee of successful inference.
    memory_category = (
        "unknown" if ram is None else
        "small_model_likely" if ram >= 8 * GIB else
        "limited_capacity"
    )
    if ram is not None and ram >= 16 * GIB:
        memory_category = "moderate_model_possible"
    status = "python_update_needed" if not py_ok else (
        "ollama_not_installed" if not ollama_executable else
        "local_service_unavailable" if check_local and local_state != "local_service_ready" else
        "inspect_ready"
    )
    command = (
        "py -3 scripts/foundry_lite.py" if system == "Windows"
        else "python3 scripts/foundry_lite.py"
    )
    return {
        "status": status, "system": system, "python": f"{python[0]}.{python[1]}",
        "python_supported": py_ok, "ollama_installed": bool(ollama_executable),
        "local_service": local_state, "installed_models": models,
        "ram_gib": round(ram / GIB, 1) if ram is not None else None,
        "free_disk_gib": round(disk / GIB, 1) if disk is not None else None,
        "ram_guidance": memory_category,
        "zero_model_inspect_command": command
        + " --input foundry-lite/fixtures/public-onboarding-review.json"
        + " --mode inspect --output foundry-lite-inspection.json",
        "install_url": OLLAMA_DOWNLOAD,
        "recommendation": (
            "Run zero-model inspect first; optional local model only after opt-in. "
            "Choose model based on available RAM and disk; no guaranteed automatic fit."
        ),
        "model_calls": 0, "appdeploy_credits_used": 0,
        "network_access": "only optional loopback GET /api/tags" if check_local else "none",
        "automated_download": False, "scheduler_created": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-local", action="store_true",
                        help="Optional loopback-only Ollama readiness GET, not AI inference")
    parser.add_argument("--json", action="store_true",
                        help="Machine-readable non-sensitive environment summary")
    args = parser.parse_args(argv)
    result = diagnose(check_local=args.check_local)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Foundry Lite laptop doctor — {result['status']}")
        print(f"OS: {result['system']} | Python: {result['python']}"
              f" | Ollama installed: {result['ollama_installed']}")
        print(f"RAM: {result['ram_gib']} GiB | Free disk: {result['free_disk_gib']} GiB")
        print(f"Local Ollama: {result['local_service']} | Models: "
              + (", ".join(result['installed_models']) or "not checked / none"))
        print("Next no-model test: " + result["zero_model_inspect_command"])
        if not result["ollama_installed"]:
            print("Optional local-model installer: " + OLLAMA_DOWNLOAD)
        print("No API credits, downloads, or recurring actions used.")
    return 0 if result["python_supported"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
