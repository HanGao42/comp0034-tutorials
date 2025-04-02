# flask_paralympics/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'paralympics.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    # 注册路由
    with app.app_context():
        from student.flask_paralympics.routes import main
        app.register_blueprint(main)

        # 导入模型并创建表
        from student.flask_paralympics import models
        db.create_all()

    return app
