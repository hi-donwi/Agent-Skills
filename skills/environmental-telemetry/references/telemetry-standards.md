# Environmental Telemetry Standards & Calculations

Reference specifications and mathematical formulations for industrial environmental monitoring (SPARING & SISPEK).

## 1. Modbus RTU Frame & CRC-16 Calculation

Industrial telemetry interfaces communicate with edge sensors (pH, COD, TSS, NH3-N, dissolved oxygen, flow meters) using RS-485 Modbus RTU.

### CRC-16 (IBM / ANSI) Algorithm
- Polynomial: `0xA001` (reversed representation of `0x8005`)
- Initial Value: `0xFFFF`
- Bitwise computation:

```typescript
export function computeModbusCRC16(buffer: Uint8Array): number {
  let crc = 0xFFFF;
  for (let i = 0; i < buffer.length; i++) {
    crc ^= buffer[i];
    for (let j = 0; j < 8; j++) {
      if ((crc & 0x0001) !== 0) {
        crc = (crc >> 1) ^ 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc & 0xFFFF;
}
```

### Word Swapping for IEEE 754 32-bit Floats
Many field transmitters store single-precision floats across two 16-bit registers:
- `Big-Endian (ABCD)`: High Word First, High Byte First.
- `Little-Endian Word Swap (CDAB)`: Low Word First, High Byte First (common in Emerson, Yokogawa, Endress+Hauser).
Transmitter drivers must explicitly declare the endianness mapping in device configuration.

---

## 2. Parshall Flume Discharge Equations

Open channel discharge through a Parshall flume under free-flow conditions follows the empirical power equation:

$$Q = C \times H_a^n$$

Where:
- $Q$ is volumetric flow rate (in cubic meters per second, $\text{m}^3/\text{s}$).
- $H_a$ is the water depth (head) measured at the standard gauge point ($2/3$ length of the converging section upstream of the throat).
- $C$ is the flume discharge coefficient.
- $n$ is the flume head exponent.

### Standard Flume Coefficients (SI Units: Head in Meters, Flow in $\text{m}^3/\text{s}$)

| Throat Width ($W$) | Coefficient ($C$) | Exponent ($n$) | Maximum Submergence Ratio ($S_t$) |
|---|---|---|---|
| 1 inch (25 mm) | 0.0604 | 1.550 | 0.50 |
| 2 inch (51 mm) | 0.1207 | 1.550 | 0.50 |
| 3 inch (76 mm) | 0.1771 | 1.550 | 0.50 |
| 6 inch (152 mm) | 0.3812 | 1.580 | 0.60 |
| 9 inch (229 mm) | 0.5354 | 1.530 | 0.60 |
| 1.0 ft (305 mm) | 0.6900 | 1.522 | 0.70 |
| 1.5 ft (457 mm) | 1.0560 | 1.538 | 0.70 |
| 2.0 ft (610 mm) | 1.4260 | 1.550 | 0.70 |
| 3.0 ft (914 mm) | 2.1840 | 1.566 | 0.70 |

### Submergence Boundary Check
When downstream water level $H_b$ rises such that the submergence ratio $S = H_b / H_a > S_t$, submergence correction must be applied to deduct backwater restriction. If $S > 0.95$, open channel calculation is invalidated and an alarm must be raised.

---

## 3. Sensor QA/QC Calibration Drift Compliance

Regulatory standards (such as KLHK KepMen LHK P.80 / P.93) mandate automated or manual daily zero and span calibration tests.

### Drift Formula

$$\text{Drift (\%)} = \left| \frac{\text{Observed Concentration} - \text{Reference Concentration}}{\text{Full Span Range}} \right| \times 100\%$$

### Compliance Criteria
- **Zero Drift Limit**: $\le 2.5\%$ of full scale.
- **Span Drift Limit**: $\le 2.5\%$ of full scale.
- **Status Evaluation**:
  - `PASSED`: Both zero and span drift $\le 2.5\%$.
  - `DRIFT_EXCEEDED`: Either zero or span drift $> 2.5\%$. Immediate recalibration required.
  - `INVALID_READING`: Sensor negative or overflowing full scale.

```typescript
export interface DriftAuditResult {
  sensorId: string;
  parameter: string;
  zeroDriftPercent: number;
  spanDriftPercent: number;
  status: "PASSED" | "DRIFT_EXCEEDED";
  compliant: boolean;
}

export function evaluateCalibrationDrift(
  zeroObserved: number,
  zeroReference: number,
  spanObserved: number,
  spanReference: number,
  fullScale: number
): DriftAuditResult {
  const zeroDrift = Math.abs((zeroObserved - zeroReference) / fullScale) * 100;
  const spanDrift = Math.abs((spanObserved - spanReference) / fullScale) * 100;
  const compliant = zeroDrift <= 2.5 && spanDrift <= 2.5;

  return {
    sensorId: "sens-01",
    parameter: "pH",
    zeroDriftPercent: Number(zeroDrift.toFixed(3)),
    spanDriftPercent: Number(spanDrift.toFixed(3)),
    status: compliant ? "PASSED" : "DRIFT_EXCEEDED",
    compliant
  };
}
```

---

## 4. Edge Spooling Queue & Store-and-Forward

Cellular (4G/LTE/NB-IoT) modems at industrial discharge points experience signal fading and base station downtime. Dataloggers must never drop readings.

### Invariants:
1. **Durable Local Storage**: Telemetry is committed to a local persistent SQLite WAL queue before network transmission is attempted.
2. **Monotonic Sequences**: Every payload includes a monotonically increasing counter and RFC 3339 timestamp.
3. **Exponential Backoff**: On HTTP 5xx or network timeout, the daemon retries with randomized exponential backoff ($2^n \times \text{delay} \pm \text{jitter}$).
4. **Batch Acknowledgment**: Buffered records are drained in chunks (e.g., 50 records) and only removed from the spool once the central ingest endpoint returns HTTP `200 OK` or `201 Created`.
