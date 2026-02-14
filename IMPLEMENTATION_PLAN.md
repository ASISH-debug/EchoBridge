# EchoBridge - Anonymous Emotion-Based Chat Implementation Plan

## Information Gathered

### Current System Analysis:
1. **app.py** contains:
   - Database setup with `users`, `emotions`, and `matches` tables
   - Emotion detection using local HuggingFace model
   - Basic matching logic (`find_emotion_match` function)
   - Routes: `/`, `/login`, `/signup`, `/logout`, `/dashboard`, `/auto`, `/manual`, `/detect`, `/match-status`

2. **Existing matches table** (in app.py):
   ```python
   c.execute('''CREATE TABLE IF NOT EXISTS matches (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       user1_id INTEGER,
       user2_id INTEGER,
       emotion TEXT,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   )''')
   ```
   - Missing: `active` column for match termination

3. **Frontend templates**:
   - `dashboard.html` - Emotion analytics
   - `auto.html` - Camera-based emotion detection

## Plan

### Phase 1: Database Updates
1. Add `active` column to matches table (DEFAULT 1)
2. Create `chat_messages` table with fields: id, match_id, sender_id, message, created_at

### Phase 2: Backend Logic Updates
1. Update `find_emotion_match` function to:
   - Exclude users who already have an active match
   - Prevent current user from matching twice
2. Update `create_match` function to set active=1
3. Add new helper functions:
   - `get_user_active_match(user_id)` - Get user's current match
   - `end_match(match_id)` - Deactivate a match
   - `validate_match_access(user_id, match_id)` - Security check

### Phase 3: New Routes
1. `GET /find-match` - Manual trigger for matching (returns match_id or waiting status)
2. `GET /chat/<match_id>` - Render chat page (with access validation)
3. `POST /send-message` - Save message to database
4. `GET /get-messages/<match_id>` - Get messages for polling
5. `POST /end-chat/<match_id>` - End chat session

### Phase 4: Frontend - Chat Template
1. Create `templete/chat.html` with:
   - Message display container
   - Input box and send button
   - "End Chat" button
   - Polling every 2 seconds using fetch
   - Anonymous display: "You" vs "Stranger"
   - Auto-scroll to latest message

### Phase 5: Integration Updates
1. Update `auto.html` to redirect to chat when matched
2. Update `dashboard.html` to show active match status and link to chat

## Dependent Files to be Edited
- `app.py` - Main backend logic and routes
- `templete/chat.html` - New chat frontend (create)
- `templete/auto.html` - Add redirect to chat on match
- `templete/dashboard.html` - Add match status/link

## Followup Steps
1. Run database migrations (handled automatically on app start)
2. Test matching logic
3. Test chat functionality
4. Verify security checks work properly

