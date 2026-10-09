# Conflict test

Initial state: version 10.

1. Client A and B both have version 10.
2. A sends an edit based on version 10.
3. Server accepts it and becomes version 11.
4. B sends its version-10 edit.
5. Server rejects B as stale.
6. B receives the latest server state.
7. No accepted edit may be silently overwritten.
