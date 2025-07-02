# Claude Code Multi-Version Feature Development Workflow

This workflow allows you to create multiple parallel implementations of a feature using Claude Code, then select and merge the best version.

## Phase 1: Feature Version Creation

### Step 1: Initialize Multi-Version Feature Development

```bash
# Ask Claude Code to create multiple versions of a feature
claude-code "Create 3 different versions of a user authentication feature. For each version:
1. Create a directory structure: auth-feature-tree/version1, auth-feature-tree/version2, auth-feature-tree/version3
2. Create git worktrees for each version with new branches: auth-v1, auth-v2, auth-v3
3. Add a spec.md file in each directory outlining the implementation approach
4. Use different architectural approaches for each version (e.g., JWT tokens, session-based, OAuth integration)"
```

### Step 2: Parallel Development

```bash
# Have Claude Code work on all versions simultaneously using task agents
claude-code "Using task agents, implement the features described in each spec.md file in parallel:
- Version 1: Focus on simplicity and basic JWT implementation
- Version 2: Implement session-based auth with Redis
- Version 3: Create OAuth2 integration with multiple providers

Work on all three versions concurrently and provide progress updates."
```

### Expected Directory Structure After Phase 1:
```
project-root/
├── auth-feature-tree/
│   ├── version1/           # Git worktree
│   │   ├── spec.md
│   │   ├── src/
│   │   └── ...
│   ├── version2/           # Git worktree  
│   │   ├── spec.md
│   │   ├── src/
│   │   └── ...
│   └── version3/           # Git worktree
│       ├── spec.md
│       ├── src/
│       └── ...
└── main-project/          # Original worktree
```

## Phase 2: Selection and Integration

### Step 3: Choose and Merge Selected Version

```bash
# After reviewing, select version (e.g., version 2)
claude-code "I've chosen version 2 as the implementation to merge. Please:
1. Switch to the main branch in the root directory
2. Merge the auth-v2 branch into main
3. Resolve any merge conflicts
4. Run final integration tests to ensure everything works"
```

### Step 4: Cleanup Worktrees and Branches

```bash
# Clean up the unused versions and worktrees
claude-code "Clean up the multi-version feature development:
1. Remove all auth-feature-tree worktrees (version1, version2, version3)
2. Delete the feature branches (auth-v1, auth-v2, auth-v3)
3. Remove the auth-feature-tree directory structure
4. Provide confirmation that cleanup is complete"
```

## General Template Commands

### For Any Feature Development:

**Initial Setup:**
```bash
claude-code "Create X versions of [FEATURE_NAME]. For each version:
1. Create directory structure: [FEATURE_NAME]-tree/version1, version2, etc.
2. Create git worktrees with branches: [FEATURE_NAME]-v1, [FEATURE_NAME]-v2, etc.
3. Add spec.md files with different implementation approaches
4. Begin parallel development using task agents"
```

**Development Phase:**
```bash
claude-code "Implement all [FEATURE_NAME] versions in parallel using different approaches:
- Version 1: [APPROACH_1_DESCRIPTION]
- Version 2: [APPROACH_2_DESCRIPTION]  
- Version 3: [APPROACH_3_DESCRIPTION]
Provide regular progress updates and completion status."
```

**Selection Phase:**
```bash
claude-code "I've selected version [X] for [FEATURE_NAME]. Please:
1. Merge [FEATURE_NAME]-v[X] into the main branch
2. Clean up all worktrees and branches for this feature
3. Remove the [FEATURE_NAME]-tree directory
4. Confirm successful integration"
```

## Best Practices

1. **Clear Feature Specifications**: Provide detailed requirements for each version approach
2. **Distinct Approaches**: Ensure each version takes a meaningfully different implementation strategy
3. **Regular Check-ins**: Ask for progress updates during parallel development
4. **Thorough Testing**: Test each version before making selection
5. **Clean Documentation**: Maintain clear spec.md files for each approach
6. **Backup Consideration**: Consider tagging or archiving rejected versions before cleanup

## Troubleshooting

### If Worktree Creation Fails:
```bash
claude-code "Debug worktree creation issues:
1. Check if branches already exist
2. Verify directory permissions
3. Ensure no conflicts with existing worktrees
4. Provide detailed error analysis"
```

### If Merge Conflicts Occur:
```bash
claude-code "Resolve merge conflicts for [FEATURE_NAME]-v[X]:
1. Identify conflicting files
2. Analyze conflict sources
3. Propose resolution strategies
4. Execute merge conflict resolution"
```

### If Cleanup Fails:
```bash
claude-code "Force cleanup of failed worktree removal:
1. Use git worktree prune to clean orphaned references
2. Manually remove directories if needed
3. Clean up branch references
4. Verify repository state is clean"
```

## Example Usage

```bash
# Real example for a payment system feature
claude-code "Create 3 versions of a payment processing feature. For each version:
1. Create directory structure: payment-tree/version1, payment-tree/version2, payment-tree/version3
2. Create git worktrees with branches: payment-v1, payment-v2, payment-v3
3. Add spec.md files with these approaches:
   - Version 1: Stripe integration with webhooks
   - Version 2: PayPal SDK implementation  
   - Version 3: Multi-provider abstraction layer
4. Implement all versions in parallel using task agents"
```

This workflow leverages Claude Code's ability to manage multiple development streams while maintaining clean Git practices and enabling easy selection and integration of the best implementation.
