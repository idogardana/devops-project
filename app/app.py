from flask import Flask, jsonify

app = Flask(__name__)

# GET / — מחזיר את הסטטוס והגרסה
@app.route('/')
def home():
    return jsonify({"status": "ok", "version": "1.0"})

# GET /health — משמש את Kubernetes לבדיקת תקינות (Liveness Probe)
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # host='0.0.0.0' קריטי להמשך כדי שהשרת יוכל לקבל בקשות מחוץ לקונטיינר של דוקר
    app.run(host='0.0.0.0', port=5000)