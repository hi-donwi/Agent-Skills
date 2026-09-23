# Flaky tests

Load when a test passes and fails without the code changing.

## Flaky tests

| Symptom | Cause | Fix |
|---|---|---|
| Red when order changes | Shared state | Build data in `@BeforeEach` |
| Intermittently red | `Thread.sleep`, time dependence | Await on a condition, inject a `Clock` |
| Red in CI, green locally | Timezone, locale, Docker | Pin `TZ=UTC` and locale in test config |
| Slow | `@QuarkusTest` for pure logic | Drop it to a unit test |
