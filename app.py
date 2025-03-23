import sqlite3
import uuid
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # 启用跨域请求支持

# 配置
app.config.update(
    DATABASE='database.db',
    SECRET_KEY='dev',  # 在生产环境中应该使用一个安全的密钥
    DEBUG=True
)

# 设置日志
def setup_logger():
    if not app.debug:
        file_handler = RotatingFileHandler('scheduler.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Scheduler startup')

# 数据库连接函数
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# 请求结束时关闭数据库连接
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# 初始化数据库
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r', encoding='utf-8') as f:
            db.executescript(f.read())
        db.commit()

# 初始化命令
@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('数据库已初始化。')

# 数据验证函数
def validate_course_data(data):
    required_fields = ['name', 'day', 'time', 'color']
    return all(field in data and data[field] for field in required_fields)

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# 路由：主页
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# API: 获取所有事件
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        db = get_db()
        cursor = db.cursor()

        # 获取课程
        cursor.execute('SELECT * FROM courses')
        courses = [dict(row) for row in cursor.fetchall()]

        # 获取固定事件
        cursor.execute('SELECT * FROM fixed_events')
        fixed_events = [dict(row) for row in cursor.fetchall()]

        return jsonify({
            'courses': courses,
            'fixedEvents': fixed_events
        })
    except sqlite3.Error as e:
        app.logger.error(f'Database error: {str(e)}')
        return jsonify({'error': '数据库错误'}), 500

# API: 添加课程
@app.route('/api/courses', methods=['POST'])
def add_course():
    try:
        data = request.json

        if not validate_course_data(data):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 从请求中获取数据
        name = data.get('name')
        teacher = data.get('teacher', '')
        location = data.get('location', '')
        day = data.get('day')
        time = data.get('time')
        color = data.get('color')
        course_id = str(uuid.uuid4())  # 生成唯一ID

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            'INSERT INTO courses (id, name, teacher, location, day, time, color, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (course_id, name, teacher, location, day, time, color, 'course')
        )
        db.commit()

        return jsonify({
            'id': course_id,
            'name': name,
            'teacher': teacher,
            'location': location,
            'day': day,
            'time': time,
            'color': color,
            'type': 'course'
        }), 201

    except sqlite3.Error as e:
        app.logger.error(f'Database error: {str(e)}')
        return jsonify({'error': '数据库错误'}), 500
    except Exception as e:
        app.logger.error(f'Server error: {str(e)}')
        return jsonify({'error': '服务器错误'}), 500

# API: 更新课程
@app.route('/api/courses/<course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        data = request.json

        if not validate_course_data(data):
            return jsonify({'error': '缺少必要的字段'}), 400

        # 从请求中获取数据
        name = data.get('name')
        teacher = data.get('teacher', '')
        location = data.get('location', '')
        day = data.get('day')
        time = data.get('time')
        color = data.get('color')

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            'UPDATE courses SET name = ?, teacher = ?, location = ?, day = ?, time = ?, color = ? WHERE id = ?',
            (name, teacher, location, day, time, color, course_id)
        )
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': '未找到课程'}), 404

        return jsonify({
            'id': course_id,
            'name': name,
            'teacher': teacher,
            'location': location,
            'day': day,
            'time': time,
            'color': color,
            'type': 'course'
        })

    except sqlite3.Error as e:
        app.logger.error(f'Database error: {str(e)}')
        return jsonify({'error': '数据库错误'}), 500
    except Exception as e:
        app.logger.error(f'Server error: {str(e)}')
        return jsonify({'error': '服务器错误'}), 500

# API: 删除课程
@app.route('/api/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': '未找到课程'}), 404

        return jsonify({'message': '课程已删除'})

    except sqlite3.Error as e:
        app.logger.error(f'Database error: {str(e)}')
        return jsonify({'error': '数据库错误'}), 500
    except Exception as e:
        app.logger.error(f'Server error: {str(e)}')
        return jsonify({'error': '服务器错误'}), 500

if __name__ == '__main__':
    setup_logger()
    app.run(debug=True)