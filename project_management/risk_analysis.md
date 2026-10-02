# Risk analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Assigned maze package interface differs or fails | Medium | High | Single adapter module; catch every error and show a message; test with a stub maze |
| Config changed during the defense (new values) | High | Medium | Validate every key, clamp to safe defaults, log, never crash |
| Python traceback shown to the user | Medium | High | Top-level handler, error screen in the UI, tests with bad input |
| Graphics library limited to MLX-equivalent functions | Medium | High | Draw everything into a pixel buffer; only use MLX window/image/hook calls |
| Packaged game differs from source (missing MLX lib/config) | Medium | High | Rebuild and test the package on a clean machine; document steps |
| Ghost AI too hard / too easy | Medium | Low | Speeds and durations configurable; cheat mode to test |
| Unexplainable generated code in the defense | Medium | High | Review and explain every module with a peer before merging |
| Schedule slip | Medium | Medium | Weekly check against timeline.md; cut optional polish first |
