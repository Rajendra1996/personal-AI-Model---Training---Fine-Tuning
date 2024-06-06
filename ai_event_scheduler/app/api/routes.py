from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app import db, cache
from app.models import User, Event
from app.api import bp
from flask_caching import Cache
from openai import OpenAI
from datetime import datetime
from app.utils.data_processing import generate_engagement_report


client = OpenAI()

@bp.route('/health-status', methods=['GET'])
def index():
    current_app.logger.info("Health check accessed")
    return jsonify({"message": "All Good!"})

# User Routes
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 409
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username}), 201

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({"username": user.username, "email": user.email, "last_login": user.last_login.isoformat() if user.last_login else None})


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Update last login time and increment login count
        user.last_login = datetime.utcnow()  # Update last login to current time
        user.login_count += 1  # Increment login count
        db.session.commit()  # Commit changes to the database

        # Successfully authenticated, create an access token
        access_token = create_access_token(identity=user.id)
        current_app.logger.info(f"User logged in: {username}")
        return jsonify(access_token=access_token), 200
    else:
        # Either username does not exist or password is incorrect
        current_app.logger.warning("Failed login attempt for username: " + username)
        return jsonify({"message": "Invalid username or password"}), 401


# Event Routes
@bp.route('/events', methods=['POST'])
@jwt_required()
def create_event():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    event_type = data.get('event_type')
    if not title or not event_type:
        return jsonify({"message": "Title and event type are required"}), 400
    event = Event(title=title, description=description, user_id=user_id, event_type=event_type)
    db.session.add(event)
    db.session.commit()
    return jsonify({"id": event.id, "title": event.title}), 201

@bp.route('/events', methods=['GET'])
@cache.cached(timeout=50)  # Cache the result of this endpoint for 50 seconds
def get_events():
    events = Event.query.all()
    return jsonify([{"id": event.id, "title": event.title, "description": event.description, "event_type": event.event_type} for event in events])

@bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    event = Event.query.get_or_404(id)
    return jsonify({"id": event.id, "title": event.title, "description": event.description, "event_type": event.event_type})

@bp.route('/events/summarize/<int:event_id>', methods=['GET'])
def summarize_event(event_id):
    event = Event.query.get_or_404(event_id)
    summary = generate_summary(event.description)
    if summary is None:
        return jsonify({'error': 'Failed to generate summary'}), 500
    return jsonify({
        'event_id': event.id,
        'title': event.title,
        'original_description': event.description,
        'ai_summary': summary
    }), 200

@bp.route('/events/type/<type_name>', methods=['GET'])
def get_events_by_type(type_name):
    events = Event.query.filter_by(event_type=type_name).all()
    events_data = [
        {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'user_id': event.user_id,
            'date': event.date.isoformat() if event.date else None,
            'ticket_price': event.ticket_price,
            'total_revenue': event.total_revenue,
            'attendee_count': event.attendee_count,
            'average_rating': event.average_rating,
            'event_type': event.event_type
        } for event in events
    ]
    return jsonify(events_data)


def generate_summary(text):
    try:
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                }
            ]
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        summary = response.choices[0].message.content # Correctly extracting the content
        print(summary.strip())
        return summary.strip()
    except Exception as e:
        current_app.logger.error("Failed to generate summary with OpenAI", exc_info=e)
        return None
