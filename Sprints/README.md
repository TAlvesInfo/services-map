# Sprints Directory

This directory contains all sprint management files for the ReadMe Coverage Map project.

## Quick Start

1. **Check current state**: Read [MASTER-SPRINT.md](./MASTER-SPRINT.md)
2. **Find a sprint**: Check [SPRINT-INDEX.md](./SPRINT-INDEX.md)
3. **See roadmap**: Review [SPRINT-PLANNING.md](./SPRINT-PLANNING.md)

## Directory Structure

```
Sprints/
+-- sprint.config.yaml        # Configuration
+-- MASTER-SPRINT.md          # Orchestration hub (start here!)
+-- SPRINT-INDEX.md           # Quick lookup
+-- SPRINT-PLANNING.md        # Master task list
|
+-- Policies/                 # Development policies
|   +-- local/                # Project-specific
|   +-- linked/               # From external repo
|   +-- policy-manifest.yaml  # Enable/disable control
|
+-- Logs/                     # Tracking logs
|   +-- MASTER-LOG.md         # AI session history
|   +-- EXCEPTIONS-LOG.md     # Deadlock/error tracking
|   +-- LESSONS-LEARNED.md    # Continuous improvement
|   +-- sessions/             # Per-session logs
|
+-- Active/                   # Sprint folders
    +-- {branch-short}/
        +-- Sprint-XX-name/
            +-- SPRINT-PLAN.md
            +-- SPRINT-LOG.md
```

## For AI Assistants

### After /clear or New Session

1. Read `MASTER-SPRINT.md` first
2. Follow the recovery checklist
3. Resume from the active sprint

### During Sprint Execution

- Execute autonomously (don't stop to ask questions)
- Update `SPRINT-LOG.md` as tasks complete
- Log decisions in `SPRINT-LOG.md`
- If blocked 3+ times, log exception and move on

### After Sprint Completion

1. Update `SPRINT-LOG.md` with final status
2. Update `MASTER-SPRINT.md`
3. Commit changes
4. Run `/clear`
5. Start next sprint

## Configuration

See `sprint.config.yaml` for:
- Project settings
- Sprint naming patterns
- AI execution settings
- Policy configuration

## More Information

- [Sprint Framework Guide](https://github.com/github-joyngroup/SprintManagement) - Original framework with full documentation
