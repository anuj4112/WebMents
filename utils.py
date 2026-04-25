"""
Utility functions for WebMents Backend
Author: Anuj Singla (2210991317)
"""

import os
import re
from datetime import datetime
from bson import ObjectId
from werkzeug.utils import secure_filename
import bcrypt


# ================= FILE HANDLING =================

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_unique_filename(original_filename):
    """Generate unique filename with timestamp"""
    filename = secure_filename(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    name, ext = os.path.splitext(filename)
    return f"{timestamp}_{name}{ext}"


def delete_file(filepath):
    """Safely delete a file"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


# ================= DATA SERIALIZATION =================

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    
    # Convert ObjectId to string
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    
    # Convert datetime to ISO format
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, ObjectId):
            doc[key] = str(value)
    
    return doc


def serialize_docs(docs):
    """Convert list of MongoDB documents to JSON-serializable list"""
    return [serialize_doc(doc) for doc in docs]


# ================= VALIDATION =================

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password, min_length=6):
    """Validate password strength"""
    if len(password) < min_length:
        return False, f"Password must be at least {min_length} characters"
    return True, "Valid password"


def validate_objectid(id_string):
    """Validate if string is a valid ObjectId"""
    return ObjectId.is_valid(id_string)


def validate_required_fields(data, required_fields):
    """Validate that all required fields are present"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, "All required fields present"


# ================= PASSWORD HASHING =================

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


# ================= RESPONSE HELPERS =================

def success_response(message, data=None, status_code=200):
    """Create success response"""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return response, status_code


def error_response(message, status_code=400):
    """Create error response"""
    return {'success': False, 'message': message}, status_code


# ================= PAGINATION =================

def paginate(query, page=1, per_page=20):
    """Paginate query results"""
    skip = (page - 1) * per_page
    items = list(query.skip(skip).limit(per_page))
    total = query.count()
    
    return {
        'items': serialize_docs(items),
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': (total + per_page - 1) // per_page
    }


# ================= SEARCH HELPERS =================

def build_search_query(search_term, fields):
    """Build MongoDB search query for multiple fields"""
    if not search_term:
        return {}
    
    # Create regex pattern for case-insensitive search
    pattern = re.compile(search_term, re.IGNORECASE)
    
    # Build OR query for all fields
    or_conditions = [{field: pattern} for field in fields]
    
    return {'$or': or_conditions}


# ================= DATE HELPERS =================

def format_datetime(dt):
    """Format datetime for display"""
    if dt is None:
        return None
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def parse_datetime(date_string):
    """Parse datetime from string"""
    try:
        return datetime.fromisoformat(date_string)
    except:
        return None


# ================= FILE SIZE HELPERS =================

def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def get_file_size(filepath):
    """Get file size in bytes"""
    try:
        return os.path.getsize(filepath)
    except:
        return 0


# ================= SANITIZATION =================

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not isinstance(text, str):
        return text
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()


def sanitize_dict(data):
    """Sanitize all string values in a dictionary"""
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, dict):
            sanitized[key] = sanitize_dict(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_input(v) if isinstance(v, str) else v for v in value]
        else:
            sanitized[key] = value
    return sanitized


# ================= LOGGING HELPERS =================

def log_request(request):
    """Log incoming request details"""
    print(f"[{datetime.now()}] {request.method} {request.path}")
    if request.args:
        print(f"  Query Params: {dict(request.args)}")
    if request.is_json:
        print(f"  JSON Data: {request.get_json()}")


def log_error(error, context=""):
    """Log error with context"""
    print(f"[ERROR] {context}: {str(error)}")


# ================= DATABASE HELPERS =================

def get_or_404(collection, query):
    """Get document or return 404 error"""
    doc = collection.find_one(query)
    if not doc:
        raise ValueError("Document not found")
    return doc


def update_timestamp(doc):
    """Add updatedAt timestamp to document"""
    doc['updatedAt'] = datetime.utcnow()
    return doc


# ================= STATISTICS HELPERS =================

def calculate_statistics(collection, match_query=None):
    """Calculate basic statistics for a collection"""
    pipeline = []
    
    if match_query:
        pipeline.append({'$match': match_query})
    
    pipeline.extend([
        {
            '$group': {
                '_id': None,
                'count': {'$sum': 1},
                'avgPrice': {'$avg': '$price'} if 'price' in collection.find_one() or {} else None
            }
        }
    ])
    
    result = list(collection.aggregate(pipeline))
    return result[0] if result else {'count': 0}


# ================= EXPORT HELPERS =================

def export_to_csv(data, filename):
    """Export data to CSV file"""
    import csv
    
    if not data:
        return False
    
    try:
        keys = data[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
