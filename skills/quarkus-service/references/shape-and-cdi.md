# Service shape, CDI, and configuration

Load when creating a class and deciding what belongs in it, which scope it takes, and where its configuration lives.

## The correct shape

```java
@Path("/api/v1/catalog/vendors")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
@Tag(name = "Catalog")
public class VendorResource {

    @Inject VendorService vendorService;

    @POST
    @RolesAllowed({"ADMIN", "COMMITTEE"})
    @Operation(summary = "Register a new vendor")
    @APIResponse(responseCode = "201", description = "Vendor created")
    @APIResponse(responseCode = "422", description = "tax ID already registered")
    public Response create(@Valid CreateVendorRequest request, @Context UriInfo uriInfo) {
        var created = vendorService.create(request);
        return Response.created(uriInfo.getAbsolutePathBuilder().path(String.valueOf(created.id())).build())
                .entity(created)
                .build();
    }
}
```

A resource does not contain: queries, business rules, `@Transactional`, or `try/catch`
blocks turning exceptions into status codes (that is the global `ExceptionMapper`'s job).

## CDI and scopes

| Scope | For |
|---|---|
| `@ApplicationScoped` | Default for services, repositories, clients — stateless |
| `@RequestScoped` | Only when genuinely per-request (user identity, request context) |
| `@Singleton` | **Don't.** Use `@ApplicationScoped`. |

Use constructor injection for classes that need testing without CDI; field injection
(`@Inject`) is fine in resources.

```java
@ApplicationScoped
public class VendorService {
    private final VendorRepository vendors;

    @Inject
    public VendorService(VendorRepository vendors) {   // can be `new`ed in a unit test
        this.vendors = vendors;
    }
}
```

**An `@ApplicationScoped` bean must not hold mutable state.** One instance serves all
concurrent requests; a mutable field is a race condition that only appears under load —
usually during UAT or in production.

## Configuration

Typed, not `@ConfigProperty` scattered around:

```java
@ConfigMapping(prefix = "app.export")
public interface ExportConfig {
    @WithDefault("5000") int batchSize();
    @WithDefault("PT10M") Duration jobTimeout();
    Path spoolDir();
}
```

The benefit is concrete: missing configuration fails at **startup** rather than the first
time the endpoint is called in production.

Secrets always come from the environment: `quarkus.datasource.password=${DB_PASSWORD}`.
