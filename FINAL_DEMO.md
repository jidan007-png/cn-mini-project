# Final demo

## Three clients
- Start server.
- Open A, B and C.
- Connect all three.

## Normal edit
- A edits.
- B and C receive the accepted update.

## Conflict
- A and B start from the same version.
- A sends first.
- B sends stale edit.
- B gets a conflict.
- No silent overwrite occurs.

## Reconnect
- Disconnect C.
- Make edits from A.
- Reconnect C.
- C synchronizes to current content/version.
