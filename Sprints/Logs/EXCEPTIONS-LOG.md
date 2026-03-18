# Exceptions Log - Deadlock & Error Tracking

> **Documents blockers, deadlocks, and exceptions requiring human intervention**

---

## Exception Summary

| Code | Category | Count | Status |
|------|----------|-------|--------|
| DL001 | Task Deadlock | 0 | OK |
| DL002 | Sprint Deadlock | 0 | OK |
| CTX001 | Context Exhausted | 0 | OK |
| API001 | API Unavailable | 0 | OK |
| AUTH001 | Auth Failure | 0 | OK |
| NET001 | Network Error | 0 | OK |

---

## Active Exceptions

*No active exceptions*

---

## Exception Categories

| Code | Category | Auto-Action | Human Required |
|------|----------|-------------|----------------|
| DL001 | Task deadlock (3+ attempts) | Skip task, log | Review needed |
| DL002 | Sprint deadlock (3+ tasks blocked) | Skip sprint, log | Review needed |
| CTX001 | Context exhausted (3x resets on same task) | Reset, retry | If persistent |
| API001 | API unavailable | Retry later | If persistent |
| AUTH001 | Auth failure | Skip platform | Credentials needed |
| NET001 | Network error | Retry 3x | If persistent |

---

## Resolved Exceptions

*No resolved exceptions yet*

---

*Last Updated: 2026-03-18*
