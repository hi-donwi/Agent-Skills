# Migration, entity, repository, audit columns

Load when adding or changing a table: the worked example of each of the four steps, in
order.

**1 — Migration first.** The schema is the source of truth; the entity follows it.

```sql
-- V20260912_1430__catalog_vendor.sql
CREATE TABLE vendor (
    id          BIGINT       GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    taxId        VARCHAR(16)  NOT NULL,
    type        VARCHAR(30)  NOT NULL,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    deleted_at  TIMESTAMPTZ,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    created_by  VARCHAR(100) NOT NULL,
    updated_at  TIMESTAMPTZ,
    updated_by  VARCHAR(100),
    CONSTRAINT ck_vendor_type CHECK (type IN ('INDIVIDUAL','COMPANY','COOPERATIVE'))
);

CREATE UNIQUE INDEX uq_vendor_taxId_live ON vendor (taxId) WHERE deleted_at IS NULL;
CREATE INDEX ix_vendor_name ON vendor (lower(name));
```

**2 — Entity.** It mirrors the table; it does not create it.

```java
@Entity
@Table(name = "vendor")
public class Vendor extends AuditableEntity {

    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    public Long id;

    @Column(nullable = false, length = 200)
    public String name;

    @Column(nullable = false, length = 16)
    public String taxId;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 30)
    public VendorType type;

    @Column(name = "is_active", nullable = false)
    public boolean active = true;

    @Column(name = "deleted_at")
    public Instant deletedAt;
}
```

`@Enumerated(EnumType.STRING)` **always**. `ORDINAL` stores the enum's position in the
source code — inserting one new value in the middle silently changes the meaning of every
existing row.

**3 — Repository.**

```java
@ApplicationScoped
public class VendorRepository implements PanacheRepository<Vendor> {

    public Optional<Vendor> findByTaxId(String taxId) {
        return find("taxId = ?1 and deletedAt is null", taxId).firstResultOptional();
    }

    public PanacheQuery<Vendor> search(String q, PageRequest page) {
        var query = (q == null || q.isBlank())
                ? find("deletedAt is null", page.toSort())
                : find("""
                       deletedAt is null
                       and (lower(name) like ?1 or taxId like ?1)
                       """, page.toSort(), "%" + q.toLowerCase() + "%");
        return query.page(page.page(), page.size());
    }
}
```

`PanacheRepository`, not active record — so services can be tested with a mock, without a
database, in milliseconds.

**4 — Automatic audit columns.**

```java
@MappedSuperclass
public abstract class AuditableEntity {
    @Column(name = "created_at", nullable = false, updatable = false)
    public Instant createdAt;
    @Column(name = "created_by", nullable = false, updatable = false)
    public String createdBy;
    @Column(name = "updated_at") public Instant updatedAt;
    @Column(name = "updated_by") public String updatedBy;

    @PrePersist void onCreate() { createdAt = Instant.now(); createdBy = CurrentUser.name(); }
    @PreUpdate  void onUpdate() { updatedAt = Instant.now(); updatedBy = CurrentUser.name(); }
}
```

---
