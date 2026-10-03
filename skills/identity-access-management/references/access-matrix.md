# Access Matrix and Identity Boundaries

## Matrix dimensions

Test subject type, authentication state, active tenant membership, scoped role,
resource tenant/legal entity, action, entitlement, and policy version. Include
an authenticated outsider, inactive member, read-only member, owner, platform support
actor, and service identity. Validate object access, not just route permission.

Use RBAC for stable role groupings; add attributes or relationships only where the
domain needs them. Complex systems must not collapse resource scope into role names.
Unknown attributes and policy errors deny access rather than silently widening it.

## Federation and provisioning

OIDC/SAML identity binding uses the trusted issuer and subject, with organization
configuration managed by an authorized administrator. Follow the actual pinned SDK
and protocol requirements. A supplied domain or unverified email claim cannot create
membership. Just-in-time provisioning must follow explicit invitation or enrollment
policy. SCIM provisioning and interactive authentication are separate trust channels.
Directory groups mapped to privileges require an approved mapping, not arbitrary
provider attributes. Protect against a tenant administrator claiming another tenant's issuer.

## Revocation

Define a maximum stale-access window and invalidate membership/permission caches,
sessions, refresh tokens, service credentials, and queued work where applicable.
Short access-token lifetimes alone do not provide immediate revocation. Check current
policy for critical actions and record original and effective actors for impersonation.

## Source and failure exercise

[OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
supports least privilege, deny-by-default, and permission checks on every request.
Remove a privileged identity through directory provisioning, then replay its prior
session and scoped service calls. Access must cease within the documented bound.
Attempt email-based account linking from another issuer; it must not inherit privileges.
