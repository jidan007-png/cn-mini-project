# Concurrency strategy

Use optimistic concurrency control.
Every edit includes the version from which the client edited.
The server accepts only if base_version equals current server version.
Otherwise it rejects the stale edit.

This is simpler than Operational Transformation or CRDTs and is
appropriate for this mini-project.
