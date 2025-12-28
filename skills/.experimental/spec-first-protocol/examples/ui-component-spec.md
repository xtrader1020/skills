# Example Spec: UI Component - User Settings Panel

## 1. Overview

### Problem Statement
Users struggle to find and modify their account settings. Settings are scattered across multiple pages with inconsistent UI patterns. This creates confusion and support burden.

### Objectives
- Consolidate all user settings into a single, intuitive panel
- Provide consistent UI/UX across all setting types
- Enable quick access to commonly changed settings
- Reduce support tickets for "how to change X"

### Success Criteria
- [ ] All user settings accessible from one panel
- [ ] Settings organized into logical groups
- [ ] Changes save immediately with clear feedback
- [ ] Mobile-responsive design
- [ ] Settings load in < 500ms
- [ ] User satisfaction score > 8/10

### Non-Goals
- Admin settings (separate interface)
- Organization-level settings (future work)
- Billing/subscription management (separate flow)

---

## 2. Context and Background

### Current State
- Settings spread across 5 different pages
- Each page has different save mechanisms
- No visual indication of unsaved changes
- Mobile experience is poor
- No search or categorization

### Proposed State
- Single settings panel with tabbed/sidebar navigation
- Auto-save with visual feedback
- Responsive design works on all devices
- Search functionality for quick access
- Organized by category with clear labels

### Stakeholders
- **Primary**: All users (50K active)
- **Secondary**: Support team, design team
- **Reviewers**: Design lead, product manager, accessibility specialist

---

## 3. Requirements

### Functional Requirements

#### Must Have
1. **Settings Categories**
   - Acceptance criteria:
     - [ ] Profile settings (name, bio, avatar)
     - [ ] Account settings (email, password)
     - [ ] Preferences (theme, language, notifications)
     - [ ] Privacy settings (profile visibility, data sharing)
     - [ ] Connected accounts (OAuth integrations)

2. **Navigation**
   - Acceptance criteria:
     - [ ] Sidebar navigation on desktop (>768px)
     - [ ] Tab navigation on mobile (<768px)
     - [ ] Current section highlighted
     - [ ] Smooth scrolling between sections

3. **Save Behavior**
   - Acceptance criteria:
     - [ ] Auto-save on blur for text inputs
     - [ ] Immediate save for toggles/dropdowns
     - [ ] Visual feedback during save (spinner, then checkmark)
     - [ ] Error handling with retry option
     - [ ] Unsaved changes warning on navigation

4. **Validation**
   - Acceptance criteria:
     - [ ] Inline validation for all fields
     - [ ] Clear error messages
     - [ ] Disable save if validation fails
     - [ ] Show validation state (error/success)

#### Should Have
- Search within settings
- Keyboard shortcuts for navigation
- Setting change history
- Export settings as JSON

#### Could Have
- Settings templates/presets
- Import settings from file
- Dark mode for settings panel
- Settings sync across devices

### Non-Functional Requirements

- **Performance**:
  - Initial load < 500ms
  - Save operation < 300ms
  - Smooth animations (60fps)
  - Lazy load category content

- **Accessibility**:
  - WCAG 2.1 AA compliant
  - Full keyboard navigation
  - Screen reader support
  - High contrast mode support
  - Focus indicators

- **Usability**:
  - Intuitive categorization
  - Clear labels and help text
  - Consistent with design system
  - Mobile-first approach

---

## 4. Technical Design

### Component Architecture

```
SettingsPanel
├── SettingsSidebar (desktop) / SettingsTabs (mobile)
│   ├── NavigationItem (x5)
│   └── SearchBox
├── SettingsContent
│   ├── ProfileSettings
│   │   ├── TextField (name)
│   │   ├── TextArea (bio)
│   │   └── AvatarUpload
│   ├── AccountSettings
│   │   ├── EmailField
│   │   └── PasswordChange
│   ├── PreferencesSettings
│   │   ├── ThemeSelector
│   │   ├── LanguageDropdown
│   │   └── NotificationToggles
│   ├── PrivacySettings
│   │   └── ToggleList
│   └── ConnectedAccounts
│       └── AccountCard (x N)
└── SaveIndicator
```

### Component Specifications

#### SettingsPanel
```typescript
interface SettingsPanelProps {
  userId: string;
  initialCategory?: SettingsCategory;
  onClose?: () => void;
}

type SettingsCategory = 
  | 'profile'
  | 'account'
  | 'preferences'
  | 'privacy'
  | 'connected-accounts';

interface SettingsPanelState {
  currentCategory: SettingsCategory;
  settings: UserSettings;
  isDirty: boolean;
  isSaving: boolean;
  lastSaved: Date | null;
  errors: Record<string, string>;
}
```

#### SettingsField (Base Component)
```typescript
interface SettingsFieldProps {
  label: string;
  value: any;
  onChange: (value: any) => void;
  onSave?: () => Promise<void>;
  error?: string;
  helpText?: string;
  required?: boolean;
  disabled?: boolean;
}
```

### Data Models

#### UserSettings
```typescript
interface UserSettings {
  profile: ProfileSettings;
  account: AccountSettings;
  preferences: PreferencesSettings;
  privacy: PrivacySettings;
  connectedAccounts: ConnectedAccount[];
}

interface ProfileSettings {
  name: string;
  bio: string;
  avatar: string | null;
  location: string;
  website: string;
}

interface PreferencesSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  emailNotifications: boolean;
  pushNotifications: boolean;
  weeklyDigest: boolean;
}

interface PrivacySettings {
  profilePublic: boolean;
  showEmail: boolean;
  allowIndexing: boolean;
  dataSharing: boolean;
}

interface ConnectedAccount {
  id: string;
  provider: 'github' | 'google' | 'twitter';
  username: string;
  connectedAt: Date;
}
```

### State Management

Using React Context + Hooks:

```typescript
const SettingsContext = React.createContext<SettingsContextValue>();

function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) throw new Error('useSettings must be within SettingsProvider');
  return context;
}

interface SettingsContextValue {
  settings: UserSettings;
  updateSetting: (path: string, value: any) => Promise<void>;
  isDirty: boolean;
  isSaving: boolean;
  lastSaved: Date | null;
  errors: Record<string, string>;
}
```

### API Integration

```typescript
// GET /api/v2/settings
async function fetchSettings(): Promise<UserSettings> {
  const response = await fetch('/api/v2/settings', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
}

// PATCH /api/v2/settings/{category}
async function updateSettings(
  category: SettingsCategory,
  updates: Partial<any>
): Promise<void> {
  await fetch(`/api/v2/settings/${category}`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
}
```

---

## 5. User Experience

### Desktop Layout (>768px)

```
┌────────────────────────────────────────────────────────────┐
│  Settings                                           [X]     │
├───────────────┬────────────────────────────────────────────┤
│               │  Profile                                   │
│ > Profile     │  ┌──────────────────────────────────────┐ │
│   Account     │  │ Name:    [John Doe            ]      │ │
│   Preferences │  │ Bio:     [Software engineer...  ]    │ │
│   Privacy     │  │ Location: [San Francisco       ]     │ │
│   Connected   │  │ Website: [https://...          ]     │ │
│               │  └──────────────────────────────────────┘ │
│ [Search...]   │  Saved 2 minutes ago ✓                   │
└───────────────┴────────────────────────────────────────────┘
```

### Mobile Layout (<768px)

```
┌────────────────────────────────┐
│  Settings              [X]     │
├────────────────────────────────┤
│ [Profile] Account Prefs Privacy│
├────────────────────────────────┤
│  Profile                       │
│  ┌──────────────────────────┐ │
│  │ Name:  [John Doe       ] │ │
│  │ Bio:   [Software...    ] │ │
│  └──────────────────────────┘ │
│  Saved just now ✓             │
└────────────────────────────────┘
```

### User Flows

#### Flow 1: Update Profile Name
1. User clicks "Settings" in navigation
2. Settings panel slides in from right
3. Profile section is active by default
4. User clicks on name field
5. User types new name
6. On blur, name is validated
7. If valid, save indicator shows spinner
8. API call to save name
9. Success: checkmark appears, "Saved just now"
10. Error: error message shown, retry button

#### Flow 2: Change Theme
1. User navigates to Preferences section
2. User clicks on theme dropdown
3. Options displayed: Light, Dark, Auto
4. User selects "Dark"
5. Theme changes immediately (optimistic update)
6. Save indicator shows spinner briefly
7. Background save to API
8. Success: checkmark appears

### Accessibility

- **Keyboard Navigation**:
  - Tab through all interactive elements
  - Arrow keys for dropdown navigation
  - Escape to close panel
  - Enter to activate buttons

- **Screen Reader Support**:
  - Proper ARIA labels on all controls
  - Live regions for save status
  - Semantic HTML structure
  - Clear field descriptions

- **Focus Management**:
  - Visible focus indicators (2px blue outline)
  - Focus trap within panel when open
  - Focus returns to trigger on close

- **Color Contrast**:
  - All text meets WCAG AA standards (4.5:1 minimum)
  - Error states have sufficient contrast
  - Icons have text alternatives

---

## 6. Visual Design

### Design Tokens

```typescript
const colors = {
  background: {
    primary: '#ffffff',
    secondary: '#f7f7f7',
    hover: '#f0f0f0'
  },
  text: {
    primary: '#1a1a1a',
    secondary: '#666666',
    disabled: '#999999'
  },
  border: {
    default: '#e0e0e0',
    focus: '#0066ff'
  },
  status: {
    success: '#00b386',
    error: '#ff3b30',
    warning: '#ff9500'
  }
};

const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px'
};

const typography = {
  heading: {
    fontSize: '24px',
    fontWeight: 600,
    lineHeight: 1.2
  },
  sectionTitle: {
    fontSize: '18px',
    fontWeight: 600,
    lineHeight: 1.4
  },
  label: {
    fontSize: '14px',
    fontWeight: 500,
    lineHeight: 1.4
  },
  body: {
    fontSize: '14px',
    fontWeight: 400,
    lineHeight: 1.5
  },
  help: {
    fontSize: '12px',
    fontWeight: 400,
    lineHeight: 1.4,
    color: colors.text.secondary
  }
};
```

### Animations

```css
/* Slide in from right */
@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Save indicator pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

/* Error shake */
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
```

---

## 7. Testing Strategy

### Unit Tests
- SettingsPanel rendering
- Navigation between categories
- Field validation logic
- Save/update logic
- Error handling

### Component Tests
- User interactions (click, type, select)
- Form validation
- Auto-save behavior
- Error state display
- Loading states

### Integration Tests
- Full settings panel workflow
- API integration
- State management
- Navigation flow

### Visual Regression Tests
- Desktop layout screenshots
- Mobile layout screenshots
- Different states (loading, error, success)
- Theme variations

### Accessibility Tests
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- Focus management

---

## 8. Implementation Plan

### Phase 1: Foundation (2 days)
- Set up component structure
- Implement basic layout (desktop + mobile)
- Add navigation (sidebar/tabs)
- Set up state management

### Phase 2: Settings Sections (3 days)
- Profile settings
- Account settings
- Preferences settings
- Privacy settings
- Connected accounts

### Phase 3: Save Logic (1 day)
- Auto-save implementation
- Save indicators
- Error handling
- Retry logic

### Phase 4: Polish (1 day)
- Animations
- Accessibility improvements
- Mobile optimizations
- Performance tuning

### Phase 5: Testing (2 days)
- Unit tests
- Integration tests
- Visual regression tests
- Accessibility audit

**Total**: 9 days

---

## 9. Open Questions

1. Should we support bulk edit mode for power users?
   - **Status**: Deferred to v2
   - **Rationale**: Adds complexity, low user demand

2. How to handle settings conflicts (e.g., changed elsewhere)?
   - **Status**: Resolved
   - **Decision**: Show notification, allow user to choose (keep/overwrite)

---

## 10. Decisions

### Decision 1: Auto-save vs. Manual Save Button
- **Date**: 2024-03-18
- **Decision**: Auto-save
- **Rationale**: Better UX, no lost changes, modern pattern
- **Trade-off**: Requires robust error handling

### Decision 2: Sidebar vs. Tabs Navigation
- **Date**: 2024-03-18
- **Decision**: Sidebar on desktop, tabs on mobile
- **Rationale**: Maximizes space usage on each device type
- **Alternative**: Tabs only would waste horizontal space on desktop
