"""Minimal test runner (pytest is not installable in this workspace)."""
import sys, pathlib, importlib.util, traceback
sys.path.insert(0, str(pathlib.Path(__file__).parent))
passed = failed = 0
for f in sorted((pathlib.Path(__file__).parent / "tests").glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(f.stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    for name in sorted(n for n in dir(m) if n.startswith("test_")):
        try:
            getattr(m, name)(); passed += 1; print(f"PASS {name}")
        except Exception:
            failed += 1; print(f"FAIL {name}"); traceback.print_exc()
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
