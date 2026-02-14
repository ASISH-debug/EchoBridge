from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
import os
import random
from functools import wraps

# 🤖 Hugging Face
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import base64
import io

# 🤖 OpenAI
try:
    from openai import OpenAI
    client = OpenAI()
    openai_loaded = True
except ImportError:
    openai_loaded = False
    client = None


app = Flask(__name__,
            template_folder='templete',
            static_folder='static')

app.secret_key = os.urandom(24)

# =======================
# 🔐 DATABASE SETUP
# =======================

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS emotions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        emotion TEXT,
        confidence REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1_id INTEGER,
        user2_id INTEGER,
        emotion TEXT,
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        sender_id INTEGER,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    conn.commit()
    conn.close()

init_db()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# =======================
# 🎯 MATCHING LOGIC
# =======================

def find_emotion_match(user_id, emotion):
    """
    Find another user with the same most recent emotion.
    Returns (matched_user_id, username) if found, else (None, None)
    Excludes users who already have an active match.
    """
    conn = get_db()
    
    # Find another user whose latest emotion matches (excluding current user)
    # Also exclude users who already have an active match
    match = conn.execute('''
        SELECT e.user_id, u.username 
        FROM emotions e
        JOIN users u ON e.user_id = u.id
        WHERE e.user_id != ? 
        AND e.emotion = ?
        AND e.id = (
            SELECT MAX(e2.id) 
            FROM emotions e2 
            WHERE e2.user_id = e.user_id
        )
        AND e.user_id NOT IN (
            SELECT CASE 
                WHEN m.user1_id = ? THEN m.user2_id 
                ELSE m.user1_id 
            END
            FROM matches m
            WHERE m.active = 1 AND (m.user1_id = ? OR m.user2_id = ?)
        )
        ORDER BY e.created_at DESC
        LIMIT 1
    ''', (user_id, emotion, user_id, user_id, user_id)).fetchone()
    
    conn.close()
    
    if match:
        return match['user_id'], match['username']
    return None, None


def create_match(user1_id, user2_id, emotion):
    """Create a new match record"""
    conn = get_db()
    conn.execute(
        "INSERT INTO matches (user1_id, user2_id, emotion, active) VALUES (?, ?, ?, 1)",
        (user1_id, user2_id, emotion)
    )
    conn.commit()
    match_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    return match_id


def get_user_active_match(user_id):
    """Get user's current active match if any"""
    conn = get_db()
    match = conn.execute('''
        SELECT m.id, m.user1_id, m.user2_id, m.emotion, m.active, m.created_at
        FROM matches m
        WHERE m.active = 1 AND (m.user1_id = ? OR m.user2_id = ?)
        ORDER BY m.created_at DESC
        LIMIT 1
    ''', (user_id, user_id)).fetchone()
    conn.close()
    return match


def validate_match_access(user_id, match_id):
    """Validate that the user has access to this match"""
    conn = get_db()
    match = conn.execute('''
        SELECT * FROM matches 
        WHERE id = ? AND active = 1 AND (user1_id = ? OR user2_id = ?)
    ''', (match_id, user_id, user_id)).fetchone()
    conn.close()
    return match is not None


def end_match(match_id):
    """End a match by setting active = 0"""
    conn = get_db()
    conn.execute("UPDATE matches SET active = 0 WHERE id = ?", (match_id,))
    conn.commit()
    conn.close()


def save_message(match_id, sender_id, message, sender_type='user'):
    """Save a chat message"""
    conn = get_db()
    conn.execute(
        "INSERT INTO chat_messages (match_id, sender_id, message, sender_type) VALUES (?, ?, ?, ?)",
        (match_id, sender_id, message, sender_type)
    )
    conn.commit()
    conn.close()


def get_messages(match_id):
    """Get all messages for a match"""
    conn = get_db()
    messages = conn.execute('''
        SELECT * FROM chat_messages 
        WHERE match_id = ? 
        ORDER BY created_at ASC
    ''', (match_id,)).fetchall()
    conn.close()
    return messages


# =======================
# 🤖 LOAD LOCAL MODEL
# =======================

try:
    model_path = "./model"
    processor = AutoImageProcessor.from_pretrained(model_path)
    model = AutoModelForImageClassification.from_pretrained(model_path)
    model.eval()
    print("✅ HuggingFace model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)
    processor = None
    model = None


# =======================
# 🌐 ROUTES
# =======================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auto')
@login_required
def auto():
    return render_template('auto.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/manual')
@login_required
def manual():
    return render_template('manual.html')


@app.route('/manual-save', methods=['POST'])
@login_required
def manual_save():
    data = request.get_json()
    emotion = data.get('emotion')
    intensity = data.get('intensity', 2)
    
    if emotion:
        conn = get_db()
        conn.execute(
            "INSERT INTO emotions (user_id, emotion, confidence) VALUES (?, ?, ?)",
            (session['user_id'], emotion, intensity * 33.33)
        )
        conn.commit()
        conn.close()
        
        # Find emotion match
        matched_user_id, matched_username = find_emotion_match(session['user_id'], emotion)
        
        if matched_user_id:
            # Create match record
            create_match(session['user_id'], matched_user_id, emotion)
            return jsonify({
                "success": True,
                "message": "Emotion saved!",
                "matched": True,
                "matched_user": matched_username,
                "emotion": emotion
            })
        else:
            return jsonify({
                "success": True,
                "message": "Emotion saved!",
                "matched": False,
                "message_match": "Waiting for someone with similar emotion...",
                "emotion": emotion
            })
    
    return jsonify({"error": "No emotion selected"}), 400


@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    emotions = conn.execute(
        "SELECT emotion, confidence, created_at FROM emotions WHERE user_id = ? ORDER BY created_at DESC",
        (session['user_id'],)
    ).fetchall()
    conn.close()

    return render_template('dashboard.html', emotions=emotions)


# =======================
# 🔐 AUTH ROUTES
# =======================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = hash_password(password)

        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE email = ? AND password = ?',
            (email, hashed_password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))

        flash("Invalid credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = hash_password(request.form.get('password'))

        conn = get_db()
        conn.execute(
            'INSERT INTO users (email, username, password) VALUES (?, ?, ?)',
            (email, username, password)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# =======================
# 🎭 EMOTION DETECTION API
# =======================

# Contextual support messages based on emotion
emotion_messages = {
    "sad": "It seems you're feeling sad. Would you like to talk to someone or try a calming activity?",
    "angry": "You look angry. Try taking a deep breath. Inhale slowly for 4 seconds.",
    "happy": "You look happy! Spread positivity and connect with others.",
    "fear": "You seem anxious. Try grounding yourself by focusing on breathing.",
    "neutral": "You seem calm and balanced. A great time for meaningful conversations.",
    "surprise": "That's surprising! Want to share what happened?",
    "disgust": "You seem uncomfortable. Take a moment and relax."
}

@app.route('/detect', methods=['POST'])
@login_required
def detect_emotion():

    if model is None or processor is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"error": "No image received"}), 400

    try:
        image_data = data["image"].split(",")[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        predicted_class_id = logits.argmax().item()

        emotion = model.config.id2label[predicted_class_id]
        confidence = torch.softmax(logits, dim=1)[0][predicted_class_id].item()

        print("🎯 Predicted Emotion:", emotion)

        # Get contextual support message
        message = emotion_messages.get(emotion, "Stay positive!")

        # Save emotion
        conn = get_db()
        conn.execute(
            "INSERT INTO emotions (user_id, emotion, confidence) VALUES (?, ?, ?)",
            (session['user_id'], emotion, confidence * 100)
        )
        conn.commit()
        conn.close()

        # Find emotion match
        matched_user_id, matched_username = find_emotion_match(session['user_id'], emotion)
        
        if matched_user_id:
            # Create match record
            create_match(session['user_id'], matched_user_id, emotion)
            return jsonify({
                "emotion": emotion,
                "confidence": round(confidence * 100, 2),
                "message": message,
                "matched": True,
                "matched_user": matched_username,
                "match_emotion": emotion
            })
        else:
            return jsonify({
                "emotion": emotion,
                "confidence": round(confidence * 100, 2),
                "message": message,
                "matched": False,
                "message_match": "Waiting for someone with similar emotion..."
            })

    except Exception as e:
        print("❌ Detection Error:", e)
        return jsonify({"error": "Detection failed"}), 500


# =======================
# 🎯 MATCH STATUS ROUTE
# =======================

@app.route('/match-status', methods=['GET'])
@login_required
def match_status():
    """Check if user has a recent match"""
    conn = get_db()
    
    # Get the most recent match for this user
    match = conn.execute('''
        SELECT m.id, m.emotion, m.created_at, 
               CASE 
                   WHEN m.user1_id = ? THEN u2.username 
                   ELSE u1.username 
               END as matched_username
        FROM matches m
        JOIN users u1 ON m.user1_id = u1.id
        JOIN users u2 ON m.user2_id = u2.id
        WHERE m.user1_id = ? OR m.user2_id = ?
        ORDER BY m.created_at DESC
        LIMIT 1
    ''', (session['user_id'], session['user_id'], session['user_id'])).fetchone()
    
    conn.close()
    
    if match:
        return jsonify({
            "matched": True,
            "matched_user": match['matched_username'],
            "emotion": match['emotion'],
            "created_at": match['created_at']
        })
    else:
        return jsonify({
            "matched": False,
            "message": "No recent match found"
        })


# =======================
# 💬 ANONYMOUS CHAT ROUTES
# =======================

@app.route('/find-match')
@login_required
def find_match():
    """Manually trigger matching logic"""
    # Check if user already has an active match
    active_match = get_user_active_match(session['user_id'])
    
    if active_match:
        # User already has an active match, redirect to chat
        return jsonify({
            "matched": True,
            "match_id": active_match['id'],
            "emotion": active_match['emotion'],
            "redirect": url_for('chat', match_id=active_match['id'])
        })
    
    # Get user's latest emotion
    conn = get_db()
    latest_emotion = conn.execute('''
        SELECT emotion FROM emotions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (session['user_id'],)).fetchone()
    conn.close()
    
    if not latest_emotion:
        return jsonify({
            "matched": False,
            "message": "No emotion detected yet. Please detect your emotion first."
        })
    
    emotion = latest_emotion['emotion']
    
    # Try to find a match
    matched_user_id, matched_username = find_emotion_match(session['user_id'], emotion)
    
    if matched_user_id:
        # Create match
        match_id = create_match(session['user_id'], matched_user_id, emotion)
        return jsonify({
            "matched": True,
            "match_id": match_id,
            "emotion": emotion,
            "redirect": url_for('chat', match_id=match_id)
        })
    else:
        return jsonify({
            "matched": False,
            "message": "Looking for someone who feels the same..."
        })


@app.route('/chat/<int:match_id>')
@login_required
def chat(match_id):
    """Render the anonymous chat page"""
    # Validate match access
    if not validate_match_access(session['user_id'], match_id):
        flash("Invalid chat session")
        return redirect(url_for('dashboard'))
    
    # Get match details
    conn = get_db()
    match = conn.execute('''
        SELECT m.*, 
               CASE 
                   WHEN m.user1_id = ? THEN u2.username 
                   ELSE u1.username 
               END as matched_username
        FROM matches m
        JOIN users u1 ON m.user1_id = u1.id
        JOIN users u2 ON m.user2_id = u2.id
        WHERE m.id = ?
    ''', (session['user_id'], match_id)).fetchone()
    conn.close()
    
    if not match:
        flash("Chat not found")
        return redirect(url_for('dashboard'))
    
    return render_template('chat.html', match=match)


@app.route('/send-message', methods=['POST'])
@login_required
def send_message():
    """Send a message in a chat"""
    data = request.get_json()
    match_id = data.get('match_id')
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({"error": "Empty message"}), 400
    
    if not match_id:
        return jsonify({"error": "No match_id provided"}), 400
    
    # Validate match access
    if not validate_match_access(session['user_id'], match_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    # Save message
    save_message(match_id, session['user_id'], message)
    
    return jsonify({"success": True})


@app.route('/get-messages/<int:match_id>')
@login_required
def get_messages_route(match_id):
    """Get messages for a match (for polling)"""
    # Validate match access
    if not validate_match_access(session['user_id'], match_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    messages = get_messages(match_id)
    
    # Format messages with sender info
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg['id'],
            "sender_id": msg['sender_id'],
            "message": msg['message'],
            "created_at": msg['created_at'],
            "is_me": msg['sender_id'] == session['user_id']
        })
    
    return jsonify({"messages": formatted_messages})


@app.route('/end-chat/<int:match_id>', methods=['POST'])
@login_required
def end_chat(match_id):
    """End a chat session"""
    # Validate match access
    if not validate_match_access(session['user_id'], match_id):
        return jsonify({"error": "Unauthorized"}), 403
    
    # End the match
    end_match(match_id)
    
    return jsonify({"success": True, "redirect": url_for('dashboard')})


# =======================
# 🤖 AI CHATBOT ROUTES
# =======================

# Emotion-aware system prompts
ai_system_prompts = {
    "sad": "You are a supportive, empathetic AI companion. Respond with kindness and understanding. Help the user process their feelings in a healthy way. Be gentle and patient.",
    "angry": "You are a calm and grounding AI companion. Respond in a peaceful, understanding tone. Help the user feel heard without escalating their emotions. Be patient and non-judgmental.",
    "happy": "You are an energetic and positive AI companion. Match the user's enthusiasm and share in their joy. Be upbeat and encouraging.",
    "fear": "You are a calming, reassuring AI companion. Help reduce anxiety with gentle words. Be supportive and help the user feel safe.",
    "neutral": "You are a friendly conversational AI companion. Have natural, warm conversations. Be personable and engaging.",
    "surprise": "You are an enthusiastic but gentle AI companion. Acknowledge the surprising element with interest but keep the tone balanced.",
    "disgust": "You are a non-judgmental, understanding AI companion. Acknowledge the user's feelings without judgment. Help them process their emotions calmly."
}

# AI chat history storage (in-memory for simplicity, can be moved to database)
ai_chat_history = {}


@app.route('/ai-chat-page')
@login_required
def ai_chat_page():
    """Render the AI chat page"""
    # Get user's latest emotion
    conn = get_db()
    latest_emotion = conn.execute('''
        SELECT emotion FROM emotions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (session['user_id'],)).fetchone()
    conn.close()
    
    emotion = latest_emotion['emotion'] if latest_emotion else 'neutral'
    
    # Initialize chat history for user if not exists
    if 'ai_chat' not in session:
        session['ai_chat'] = []
    
    # Get system prompt based on emotion
    system_prompt = ai_system_prompts.get(emotion, ai_system_prompts['neutral'])
    
    return render_template('ai-chat.html', 
                          emotion=emotion, 
                          system_prompt=system_prompt,
                          chat_history=session.get('ai_chat', []))


@app.route('/ai-chat', methods=['POST'])
@login_required
def ai_chat():
    """AI chatbot endpoint with emotion-aware responses"""
    if not openai_loaded or client is None:
        return jsonify({"error": "OpenAI library not installed"}), 500
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    # Get user's latest emotion
    conn = get_db()
    latest_emotion = conn.execute('''
        SELECT emotion FROM emotions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (session['user_id'],)).fetchone()
    conn.close()
    
    emotion = latest_emotion['emotion'] if latest_emotion else 'neutral'
    system_prompt = ai_system_prompts.get(emotion, ai_system_prompts['neutral'])
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "OpenAI API key not configured"}), 500
    
    try:
        # Build messages array
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        # Call OpenAI API with new syntax
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        ai_response = completion.choices[0].message.content
        
        # Save to chat history in session
        if 'ai_chat' not in session:
            session['ai_chat'] = []
        
        session['ai_chat'].append({"role": "user", "content": user_message})
        session['ai_chat'].append({"role": "assistant", "content": ai_response})
        
        # Keep only last 20 messages to prevent session bloat
        if len(session['ai_chat']) > 20:
            session['ai_chat'] = session['ai_chat'][-20:]
        
        return jsonify({
            "success": True,
            "response": ai_response,
            "emotion": emotion
        })
        
    except Exception as e:
        print("❌ OpenAI Error:", str(e))
        return jsonify({"reply": "AI service error."})


@app.route('/ai-get-messages')
@login_required
def ai_get_messages():
    """Get AI chat history"""
    chat_history = session.get('ai_chat', [])
    return jsonify({"messages": chat_history})


@app.route('/ai-clear', methods=['POST'])
@login_required
def ai_clear():
    """Clear AI chat history"""
    session['ai_chat'] = []
    return jsonify({"success": True})


# =======================
# 🤖 FAKE CHATBOT (Demo/Presentation)
# =======================

# Predefined responses based on emotion
emotion_responses = {
    "sad": [
        "I'm here for you.",
        "Do you want to talk about it?",
        "It's okay to feel this way.",
        "I'm listening.",
        "Take your time, I'm here.",
        "Things will get better.",
        "You don't have to face this alone."
    ],
    "angry": [
        "I understand you're upset.",
        "Take a deep breath.",
        "It's okay to feel angry.",
        "I'm here to listen.",
        "Would you like to talk about it?",
        "Let's work through this together.",
        "Your feelings are valid."
    ],
    "happy": [
        "That's amazing!",
        "I love that energy!",
        "Tell me more!",
        "That's wonderful!",
        "I'm so happy for you!",
        "That's great news!",
        "Your happiness is contagious!"
    ],
    "fear": [
        "I'm here with you.",
        "Take slow, deep breaths.",
        "You're safe here.",
        "One step at a time.",
        "I'm here to support you.",
        "You've got this.",
        "It's okay to feel afraid."
    ],
    "neutral": [
        "I see.",
        "Tell me more.",
        "That's interesting.",
        "Go on...",
        "I'm listening.",
        "What else is on your mind?",
        "How do you feel about that?"
    ],
    "surprise": [
        "Wow, that's unexpected!",
        "Tell me more about that!",
        "That's incredible!",
        "How did that happen?",
        "That's quite surprising!",
        "I'd love to hear more!",
        "What happened next?"
    ],
    "disgust": [
        "I understand that feeling.",
        "That's completely valid.",
        "I'm here to listen.",
        "Do you want to talk about it?",
        "It's okay to feel that way.",
        "Take your time.",
        "Would you like to share more?"
    ]
}

# Default responses when emotion is unknown
default_responses = [
    "I'm here for you.",
    "Tell me more.",
    "How does that make you feel?",
    "I understand.",
    "That's interesting.",
    "Go on...",
    "I'm listening."
]


@app.route('/chatbot-response', methods=['POST'])
@login_required
def chatbot_response():
    """Fake AI chatbot with predefined responses based on emotion"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    # Get user's latest emotion from database
    conn = get_db()
    latest_emotion = conn.execute('''
        SELECT emotion FROM emotions 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT 1
    ''', (session['user_id'],)).fetchone()
    conn.close()
    
    emotion = latest_emotion['emotion'] if latest_emotion else 'neutral'
    
    # Get responses based on emotion
    responses = emotion_responses.get(emotion, default_responses)
    
    # Pick a random response
    selected_response = random.choice(responses)
    
    return jsonify({
        "reply": selected_response,
        "emotion": emotion
    })


# =======================

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5001)
