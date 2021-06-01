#flask_sqlalchemy, Migrate

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() #init파일에서 따로 db를 임포트 해줘야 함
migrate = Migrate() #init파일에서 연결해줘야 함 (db랑 같이)


class User(db.Model): #데이터 모델을 나타내는 객체 선언  
    userid = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    pwd = db.Column(db.String(8), nullable=False)

    def __repr__(self):
        return f"User id : {self.userid}, Email : {self.email}, Password : {self.pwd}"

class Check(db.Model):
	index = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.String)
	#회차정보
	date = db.Column(db.String, nullable=False)
	comm = db.Column(db.String, nullable=False)
	#'이게뭐지' = db.relationship('Post', backref='user', lazy=True)

	def __repr__(self):
		return f"Index : {self.index}, User id : {self.userid}, Check : {self.comm}, Date : {self.date}"