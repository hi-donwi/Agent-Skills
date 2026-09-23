# Streaming and file formats

Load when writing the export itself: pulling rows without buffering them, and producing
XLSX, PDF or ZIP from a stream.

The demo works because 300 rows fit anywhere. At 100,000 rows of order transactions
the same code produces `OutOfMemoryError` — and it does so in production under real data,
not in testing under sample data.

```java
// WRONG — the whole table in a List, then a whole workbook in memory
List<TransactionRow> rows = repository.findAllForExport();
XSSFWorkbook wb = new XSSFWorkbook();
```

```java
// RIGHT — stream from the database, flush to disk every N rows
try (SXSSFWorkbook wb = new SXSSFWorkbook(100)) {   // keep 100 rows in memory
    var sheet = wb.createSheet("Transactions");
    int rowNum = 0;
    try (Stream<TransactionRow> stream = repository.streamForExport(filter)) {
        for (var row : (Iterable<TransactionRow>) stream::iterator) {
            write(sheet.createRow(rowNum++), row);
        }
    }
    try (var out = Files.newOutputStream(spoolFile)) {
        wb.write(out);
    }
    wb.dispose();   // delete the temporary files SXSSF created
}
```

`SXSSFWorkbook(100)` keeps a 100-row sliding window in memory and flushes the rest to
temporary files. `wb.dispose()` is mandatory — without it those temporary files stay on
disk, and the spool volume fills up quietly over weeks.

### Streaming from the database

```java
@ApplicationScoped
public class TransactionExportRepository {
    @Inject EntityManager em;

    public Stream<TransactionRow> streamForExport(ExportFilter filter) {
        return em.createQuery(JPQL_EXPORT, TransactionRow.class)
                 .setParameter("from", filter.from())
                 .setParameter("to", filter.to())
                 .setHint(HINT_FETCH_SIZE, 1000)   // do not buffer the whole result
                 .getResultStream();
    }
}
```

The stream must be consumed inside a transaction and closed — hence `try (…)`. Without a
fetch-size hint, the JDBC driver may still buffer everything, which defeats the purpose.

## Aggregate in the database

```java
// WRONG — 500,000 rows into memory to produce 12 summary lines
var all = repository.findAll(filter);
var byType = all.stream().collect(groupingBy(r -> r.type, reducing(...)));

// RIGHT — the database returns 12 rows
SELECT order_type, COUNT(*), SUM(amount)
FROM order
WHERE transaction_date BETWEEN :from AND :to AND deleted_at IS NULL
GROUP BY order_type
```

Most "slow report" tickets resolve to this one change. A summary report should never load
detail rows.

Every report query needs indexes on its filter and grouping columns, created in the same
migration as the report.

## PDF

OpenPDF, as in the demo. The same streaming rule applies: write page by page, do not build
the whole document in memory.

- A tabular PDF over roughly 5,000 rows is not a usable document. Offer XLSX instead, or
  paginate the report itself.
- Watermarks, headers, and footers are applied per page during writing, not by
  post-processing the finished file.
- Fonts must be embedded, or Indonesian characters will vary across viewers.

## ZIP

When an export produces several files, stream into the ZIP — do not create each file fully
then add it.

```java
try (var zos = new ZipOutputStream(Files.newOutputStream(target))) {
    for (var part : parts) {
        zos.putNextEntry(new ZipEntry(part.name()));
        part.writeTo(zos);          // streams straight into the ZIP
        zos.closeEntry();
    }
}
```
