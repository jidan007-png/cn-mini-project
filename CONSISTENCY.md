# Consistency guarantees

The server is the single source of truth.

Guarantees:
- accepted edits have increasing versions;
- stale edits are detected;
- accepted edits are not silently overwritten;
- reconnecting clients can obtain the current state.

Not provided:
- automatic merge of conflicting edits;
- character-level collaborative cursors;
- replicated servers.
