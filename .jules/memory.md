## Archived: 2026-11-02

* The `testing_minimal` list in `pyproject.toml` must use flexible version constraints for `torch` (e.g., `>=2.9.0`) rather than strict pinning (e.g., `==2.9.0`) to avoid `ResolutionTooDeep` errors caused by conflicts with `ultralytics` and `torchvision` dependencies.
* The project requires Python 3.11 or newer (`>=3.11`) and uses `setuptools` as the build backend.
* External tests using libraries like `nibabel` or `datasets` utilize `pytest.importorskip` at the top level to gracefully skip tests during collection if module imports fail due to missing system dependencies (e.g., `_bz2`).
* The CPU JIT compiler (`ClangJITCompiler` in `tinygrad/runtime/support/compiler_cpu.py`) falls back to `gcc` using temporary files if `clang` is missing; it includes retry logic to strip architecture flags (e.g., `-march=native`) if the initial compilation fails.
* The `ClangRenderer` in `tinygrad/renderer/cstyle.py` overrides `string_rewrite` for `Ops.BITCAST` to use a custom `BITCAST(type, value)` macro. This macro is implemented using a union and GNU statement expressions (`({ ... })`) to ensure compatibility with GCC's C mode, which lacks support for `__builtin_bit_cast`.
* Tests located in `test/external/` use the naming convention `external_test_*.py` and are excluded from default `pytest` discovery; executing them requires a custom configuration override (e.g., `-o "python_files=test_*.py *_test.py external_test_*.py"`).
* The `get_analysis` function in `tinygrad/schedule/rangeify.py` caches analysis results using a `weakref.WeakKeyDictionary` keyed by the `src` UOp to handle repeated sub-graph traversals efficiently.
* The project defines an optional `[testing]` dependency group in `pyproject.toml` (installable via `pip install -e '.[testing]'`) which includes requirements like `numpy` and `torch` necessary for the full test suite.
* The `external_test_keccak.py` script applies downsampling to the NIST test vectors (e.g., `vectors[::50]`) to ensure the test suite completes within a reasonable time frame.
* The user requires a 'deep planning mode' before any changes, involving clarifying questions to verify assumptions and ensure absolute certainty before creating a plan.
* To prevent graph recompilation and infinite rewrite loops, variable padding masks in `tinygrad` are constructed using `Tensor.arange` and comparison/`where` operations with uniform inputs, rather than `one_hot` or Python control flow.
* For AMD RDNA 3 (`gfx11`) and RDNA 4 (`gfx12`) architectures, the `vgpr_size_per_cu` is set to `0x60000` (384KB).
* AMD Stix Halo (RDNA 3.5, `gfx1150`/`gfx1151`) is supported in `tinygrad` using the same logic as RDNA 3 (`gfx11`) targets.
* The `external_test_speed_theoretical.py` benchmark adjusts `flopsmax` loop iterations (50 for floats, 5 for int8) and lowers the `MEMBW` threshold on CPU (to 2.0 GB/s) to avoid compiler timeouts and compute-bound failures.
* The `CC` environment variable determines the compiler used by the CPU backend; it defaults to `clang` but will auto-detect `gcc` if `clang` is absent.
* `sqlite3` is treated as an optional, lazy-loaded dependency in `tinygrad`; disk caching features are gracefully disabled if the module is unavailable.
* The user prioritizes running the full test suite (including external tests) and expects missing dependencies or code errors to be investigated and fixed rather than skipped.
* Tests located in `test/external/` employ `test/external/conftest.py` to patch the standard `bz2` module with `bz2file` (polyfilling missing methods like `compress`/`decompress`) to support environments lacking the native `_bz2` extension.
* `tinygrad.helpers.getenv(key, default)` casts the environment variable value to the type of `default`. If `default` is omitted, it defaults to `0` (int). Therefore, string environment variables must be requested with an explicit string default (e.g., `getenv('KEY', '')`).
* The user prefers the AI to use `request_user_input` and `message_user` for communication during the planning phase.
* The project (`tinygrad`) enforces a coding style of 2-space indentation and a maximum line length of 150 characters.
* Unit tests that involve C compilation (e.g., `test/unit/test_autogen.py`) must use `tinygrad.runtime.support.compiler_cpu.get_cc()` to dynamically select the correct compiler instead of hardcoding `clang`.
* Key code locations have been updated: the `Kernel` class is located in `tinygrad.uop.ops`, and `compile_hip` is located in `tinygrad.runtime.support.compiler_amd`.
* The `run_tests.sh` script automatically handles environment setup by creating a local virtual environment (`venv`) if one is missing, activating it, setting `PYTHONPATH=.`, and installing dependencies before running tests.
* The command `pip install -e '.[testing_minimal]'` installs the minimal set of dependencies required to run the `tinygrad` test suite, excluding heavy external dependencies.
* The C-style renderer (`tinygrad/renderer/cstyle.py`) uses `__attribute__((vector_size(N)))` instead of `ext_vector_type` for vector definitions to ensure compatibility with GCC, ensuring `N` is rounded up to the nearest power of two bytes.
* The `UOp` class in `tinygrad/uop/ops.py` implements a `has_range` method for efficient DFS-based range existence checks and optimizes `_ranges` to avoid dictionary copying when passing through single-source nodes.
* The `keccak` method in `tinygrad/tensor.py` explicitly calls `.realize()` on the state within its processing loop to prevent the UOp graph depth from exceeding recursion limits for long messages.
* The `tinygrad/helpers.py` module is strictly prohibited from importing any other modules within `tinygrad`.
* Large manually unrolled loops in Python code generate deep UOp graphs that can cause significant compilation delays on the CPU backend (`ClangJITCompiler`), necessitating reduced complexity in tests to avoid timeouts.
* The `tinygrad` compilation pipeline follows the sequence: Tensor -> UOp -> Schedule -> Codegen -> Runtime.
* The `cleanup_dead_axes` function in `tinygrad/schedule/rangeify.py` utilizes `b.src[0].has_range(rng)` rather than accessing `.ranges` directly, optimizing performance by avoiding full dictionary construction for existence checks.
* The `get_analysis` function in `tinygrad/schedule/rangeify.py` enforces a node count limit (e.g., 5000) to abort analysis on excessively large subgraphs, preventing compilation hangs on deep graphs like unrolled Keccak.
* Properties on the `UOp` class (e.g., `ranges`) use the `@recursive_property` decorator to cache results in `__dict__`, which efficiently handles potential recursion during graph traversals.
* The `ClangJITCompiler` in `tinygrad/runtime/support/compiler_cpu.py` has been updated to explicitly capture and raise `stderr` output when `gcc` compilation fails, aiding in the debugging of environment-specific build issues where standard `CalledProcessError` output is insufficient.
* The external test suite (`test/external/`) requires specific heavy dependencies: `tensorflow`, `datasets`, `torchaudio`, `ultralytics`, `jiwer`, `openai-whisper`, `bz2file`, `onnx`, and `tabulate`. These are configured in the `[testing]` optional dependency group in `pyproject.toml`.
* In `tinygrad`, functionality changes must be tested and should not be mixed with whitespace changes.
