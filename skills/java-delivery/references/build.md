# Build: parent POM and gating plugins

Load when setting up or fixing the Maven build itself.

### Parent POM essentials

```xml
<properties>
  <maven.compiler.release>21</maven.compiler.release>
  <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  <quarkus.platform.version>3.33.3.2</quarkus.platform.version>
  <jacoco.line.min>0.80</jacoco.line.min>
</properties>
```

Every version pinned. No ranges, no `LATEST`. A build today and a build in three months
produce the same artifact.

### Plugins that gate the build

| Plugin | Gate |
|---|---|
| `maven-enforcer-plugin` | Java 21, `dependencyConvergence`, no duplicate versions |
| `spotless-maven-plugin` | Formatting |
| `jacoco-maven-plugin` | Coverage thresholds |
| `dependency-check-maven` | CVSS ≥ 7 |
| `maven-failsafe-plugin` | Integration tests (`*IT`) |
| `spotbugs-maven-plugin` | High-priority static findings |

`dependencyConvergence` is the one people want to disable first. What it prevents is two
libraries pulling different versions of the same transitive dependency, producing a
`NoSuchMethodError` in production on a rarely-exercised path.

---
