---
name: environmental-telemetry
description: >-
  Implement environmental telemetry, Modbus RTU acquisition, Parshall flume volumetric flow, sensor calibration drift limits, and offline spooling.
metadata:
  pack: core
  keywords: telemetry, iot, modbus, sparing, sispek, parshall flume, flow rate, calibration drift, span drift, zero drift, spooling queue, klhk
---

# Environmental Telemetry

## Overview
Environmental telemetry systems (such as SPARING for wastewater and SISPEK for stack
emissions) require continuous, verifiable acquisition of environmental parameters.
Ingested readings must be mathematically sound, calibrated within regulatory tolerances,
and durable against field network disruptions.

## When to use
- Connecting industrial dataloggers or sensors over RS485 / Modbus RTU.
- Computing open-channel water flow using Parshall flumes or weir equations.
- Evaluating daily zero and span calibration drift against regulatory thresholds (drift <= 2.5%).
- Implementing store-and-forward edge spooling queues for intermittent uplinks.

## Hand off when
| Need | Skill |
|---|---|
| Inbound HTTP partner webhooks and signature verification | `webhook-integrations` |
| Durable async background workers and lease recovery | `background-jobs` |
| Service telemetry, OpenTelemetry, and structured metrics | `observability` |

## Process
1. **Acquire and Validate Modbus RTU Frames.** Compute CRC-16 (IBM/ANSI polynomial 0xA001).
   Decode 16-bit holding and input registers into IEEE 754 32-bit floats. Handle byte-order
   permutations (Big-Endian / Little-Endian word swaps) deterministically. Reject frames with
   corrupted checksums or out-of-range sensor values before persisting.
2. **Compute Open-Channel Flow Rate.** For Parshall flumes, apply $Q = C \times H^n$ based on
   flume throat width $W$. Validate head measurement $H$ at the gauge point (2/3 upstream).
   Verify that downstream submergence $H_b / H_a$ does not exceed free-flow thresholds (50% to 70%).
3. **Audit Daily Sensor Calibration Drift.** Compare observed zero gas/water and span standard
   concentrations against reference standards:
   $$\text{Drift (\%)} = \left| \frac{\text{Observed} - \text{Reference}}{\text{Span Range}} \right| \times 100\%$$
   Enforce the regulatory threshold: $\text{Drift} \le 2.5\%$. Flag any sensor exceeding 2.5%
   as Out-of-Calibration (`DRIFT_EXCEEDED`) and generate an audit record.
4. **Buffer Telemetry in a Durable Offline Spool.** Implement a local persistent queue (SQLite WAL
   or append-only storage) at the edge. Buffer samples when 4G/LTE connectivity drops. Replay
   buffered samples chronologically with exponential backoff and batch acknowledgments once
   connectivity is restored.
5. **Enforce Idempotency and Auditability.** Assign monotonically increasing sequence numbers and
   hardware timestamps. Store raw sensor millivolts/registers alongside transformed engineering
   units for verifiable compliance audits.

## Red flags
- Trusting Modbus registers without CRC validation or range sanity checks.
- Assuming free-flow discharge when downstream water backs up into the Parshall throat.
- Suppressing calibration drift errors or rounding drift values to bypass the 2.5% threshold.
- Dropping telemetry packets when edge networking disconnects instead of queuing to disk.

## Verification
- Unit test CRC-16 calculation against known test vectors (`0xFFFF` initial seed).
- Verify Parshall flume calculation matches empirical tables for 1-inch through 3-foot throats.
- Drift calculation unit tests confirm Pass at 2.49% and Fail at 2.51%.
- Edge spooling recovers gracefully across process restarts and simulated network partitions.

## References
- `references/telemetry-standards.md` - Modbus CRC-16 vectors, Parshall equations, and drift algorithms.
