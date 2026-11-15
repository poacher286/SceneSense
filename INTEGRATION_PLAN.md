# Steamworks Authentication Integration Plan for SceneSense

## Current Application Architecture

**Type**: Local Python desktop application (no web server, no database)
**Entry Point**: `app/bootstrap.py` → `app/main.py`
**Architecture**: Event-driven with isolated modules (capture, ai, device, events, etc.)
**No persistent user storage** required by default

---

## Option 1: Steam Guard Token Auth (Recommended for Desktop Apps)

### Why This Works Best
- **Privacy-first**: No data leaves local machine (matches CLAUDE.md principles)
- **Zero server dependencies**: Works entirely offline
- **Steamworks API compliance**: Uses official token validation
- **Minimal integration**: No backend changes needed

### Implementation Approach

#### 1. Steam Guard Token Module (`app/auth/steam_guard.py`)
```python
from dataclasses import dataclass
from datetime import datetime
import subprocess
import re

@dataclass
class SteamGuardSession:
    steamid: str
    token: str
    code: str  # email verification code
    expires: datetime | None = None
```

#### 2. Token Validation Workflow
- User launches app → `Bootstrap.start()` wires auth subscriber
- App prompts for Steam Guard MFA token from email
- Validates via Steamworks API (`ISteamUserAuth->AuthenticateWithTokenAsync`)
- Stores validated session in memory (no persistence needed for privacy)

#### 3. Key Files to Create:
```
app/
├── auth/
│   ├── __init__.py          # Auth subsystem registration
│   └── steam_guard.py        # Token validation logic
├── events/
│   └── events.py            # Add SteamAuthSuccess/SteamAuthFailed events
└── main.py                  # Update to support auth initialization
```

---

## Option 2: Steam Login Redirect (Advanced)

### Flow
1. App presents HTML login dialog via WebView2 or electron-style shell
2. User authenticates with Steam overlay (`steam://login`)
3. Callback token validated via local HTTP server on localhost
4. Session stored in `~/.scenesense/config/auth.json`

### Pros/Cons:
- **Pros**: Seamless UX, remembers logged-in state
- **Cons**: Requires GUI dependencies, more complex

---

## Recommendation

**Start with Option 1 (Steam Guard Token)** because it:
- ✅ Follows "Local First" principle from CLAUDE.md
- ✅ Works offline (ideal for desktop scene recognition)
- ✅ Simplest implementation path
- ✅ Can upgrade to Option 2 later if needed

---

## Migration Path

1. **Phase 1**: Implement token auth module
2. **Phase 2**: Wire into EventBus system  
3. **Phase 3**: Test with sample Steam Guard codes
4. **Phase 4**: Optional: Add optional persistent storage for convenience
5. **Phase 5**: Consider login dialogs if user retention justifies complexity

---

## Example Usage Context

```python
# Event flow when user authenticates:
ScentTriggered → UserAuthenticated → DeviceOnline
FrameCaptured → SceneDetected → [authentication check optional]

# Auth is opt-in, doesn't block core functionality
```

---

## Next Steps

1. Review this plan
2. Decide on Option 1 vs 2 (or both)
3. I can implement the auth module following the existing Bootstrap pattern
4. Add event types for auth flow to events.py
5. Wire into bootstrap initialization

Would you like me to:
- A) Implement Option 1 (token auth) now
- B) Wait to review the plan and discuss approach first  
- C) Consider a different approach entirely
