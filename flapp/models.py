#flask_sqlalchemy, Migrate

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() #init파일에서 따로 db를 임포트 해줘야 함
migrate = Migrate() #init파일에서 연결해줘야 함 (db랑 같이)


class Check(db.Model): #__tablename__으로 이름을 지정하지 않아도 클래스 이름의 소문자로 테이블 이름을 자동지정해줌
	id = db.Column(db.String, primary_key=True)
	done = db.Column(db.String, nullable=False)
	date = db.Column(db.Integer, nullable=False)
	#'이게뭐지' = db.relationship('Post', backref='user', lazy=True)

	def __repr__(self):
		return f"User id : {self.id}, Check : {self.done}, Date : {self.date}"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(30), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f"Post {self.id}"