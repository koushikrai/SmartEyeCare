from flask import Blueprint, request, jsonify
from db import get_db
from bson import ObjectId
import datetime

history_bp = Blueprint('history', __name__)


@history_bp.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    try:
        db = get_db()
        # validate user_id
        try:
            uid = ObjectId(user_id)
        except Exception:
            # keep as string if not a valid ObjectId
            uid = user_id

        docs = list(db.history.find({'user_id': uid}).sort('created_at', -1).limit(200))
        # Convert ObjectId to str and datetime
        for d in docs:
            d['_id'] = str(d['_id'])
            if isinstance(d.get('user_id'), ObjectId):
                d['user_id'] = str(d['user_id'])
            if isinstance(d.get('created_at'), datetime.datetime):
                d['created_at'] = d['created_at'].isoformat()
        return jsonify({'history': docs}), 200
    except Exception as e:
        print(f"Get history error: {e}")
        return jsonify({'error': str(e)}), 500


@history_bp.route('/history/add', methods=['POST'])
def add_history():
    try:
        payload = request.get_json()
        if not payload:
            return jsonify({'error': 'Missing JSON payload'}), 400

        user_id = payload.get('user_id')
        kind = payload.get('kind', 'unknown')
        input_meta = payload.get('input', {})
        result = payload.get('result', {})

        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400

        try:
            uid = ObjectId(user_id)
        except Exception:
            uid = user_id

        db = get_db()
        doc = {
            'user_id': uid,
            'kind': kind,
            'input': input_meta,
            'result': result,
            'created_at': datetime.datetime.utcnow()
        }
        res = db.history.insert_one(doc)
        return jsonify({'message': 'saved', 'id': str(res.inserted_id)}), 201
    except Exception as e:
        print(f"Add history error: {e}")
        return jsonify({'error': str(e)}), 500
