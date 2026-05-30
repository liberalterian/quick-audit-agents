# Routing Delivery Test

## Purpose

Verify Drive upload, Gmail draft/send, and Tracker writeback behavior.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Use test artifacts.
2. Upload to test Drive folder.
3. Create prospect draft.
4. Create team draft for HARD-PASS/SOFT-FAIL.
5. Update test Tracker row.

## Pass criteria

- Drive URLs are captured.
- Drafts contain correct recipient, subject, body, and attachment.
- HARD-FAIL does not create team alert.
- Tracker row records routing state.

## Fail criteria

- PDF is not attached.
- Internal Grading Notes are sent to prospect.
- Team alert sent for HARD-FAIL.

