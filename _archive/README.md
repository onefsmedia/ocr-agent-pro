# Archive Directory

This directory contains old versions and deprecated files organized by version and purpose.

## ⚠️ Important Note

**Files in this directory are archived for historical reference only.**
- Do NOT use these files in production
- They may contain bugs or outdated approaches
- Refer to current codebase for active implementations

## Directory Structure

### `v1.0_initial/`
Initial development phase files (October 2025)
- Early prototypes
- Initial server implementations
- SQLite-based versions

### `v1.1_server_fixes/`
Server stability improvements (Mid-October 2025)
- Multiple server launcher variants
- Waitress WSGI integration attempts
- Connection reliability fixes
- Old test files from troubleshooting phase

**Key files:**
- `waitress_server.py` → Evolved into production `server.py`
- `final_server.py`, `stable_server.py` → Server stability iterations
- Various `*_server.py` files → Different approaches tested

### `v1.2_onlyoffice_integration/`
OnlyOffice Document Server integration work (Late October 2025)
- Port configuration attempts (8000, 8001, 8080)
- Admin panel access troubleshooting
- Bootstrap token handling scripts
- Configuration utilities

**Key files:**
- `configure_onlyoffice_*.py` → Various configuration approaches
- `bootstrap_bypass_manual.py` → Admin panel workarounds
- `onlyoffice_solution.py` → Integration verification script

### `deprecated/`
Completely obsolete files
- Batch file launchers (`.bat`)
- Old setup scripts
- Windows service implementations
- Education-specific feature implementations
- Temporary troubleshooting scripts

## Version Timeline

### Version 1.0 → 1.1 (Server Stability Phase)
**Problem**: Flask development server instability under load
**Solution**: Migrated to Waitress WSGI server
**Archived**: ~20 server launcher variations

### Version 1.1 → 1.2 (OnlyOffice Integration)
**Problem**: OnlyOffice port configuration and admin panel access
**Solution**: Port 8080 with direct configuration (admin panel not required)
**Archived**: ~15 configuration scripts and admin panel workarounds

### Version 1.2 → 1.3 (Current Production)
**Changes**:
- Project reorganization
- Production-ready structure
- Comprehensive documentation
- Clean codebase

## When to Reference Archive

### Useful References:
- Understanding evolution of server implementation
- Reviewing troubleshooting approaches
- Learning from previous integration attempts
- Historical context for architectural decisions

### Don't Use For:
- Production deployments
- New features
- Current bug fixes
- Code examples (use current codebase instead)

## Migration Notes

If you need to extract logic from archived files:
1. Review current implementation first
2. Check if the problem still exists
3. Adapt code to current architecture
4. Test thoroughly
5. Update documentation

## File Count Summary

- **v1.0_initial/**: ~5 files
- **v1.1_server_fixes/**: ~35 files (servers + tests)
- **v1.2_onlyoffice_integration/**: ~25 files (configs + scripts)
- **deprecated/**: ~15 files

**Total archived**: ~80 files

## Cleanup Policy

Archive files are retained for:
- 6 months: All files
- 12 months: Major version archives
- Indefinitely: Critical architectural decision references

---

**Last Updated**: November 1, 2025  
**Current Version**: 1.3.0 (Production)
