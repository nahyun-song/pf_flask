#flask_sqlalchemy, Migrate

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() #init파일에서 따로 db를 임포트 해줘야 함
migrate = Migrate() #init파일에서 연결해줘야 함 (db랑 같이)


class Check(db.Model): #__tablename__으로 이름을 지정하지 않아도 클래스 이름의 소문자로 테이블 이름을 자동지정해줌
	userid = db.Column(db.String, primary_key=True)
	done = db.Column(db.String, nullable=False)
	date = db.Column(db.Integer, nullable=False)
	#'이게뭐지' = db.relationship('Post', backref='user', lazy=True)

	def __repr__(self):
		return f"User id : {self.id}, Check : {self.done}, Date : {self.date}"


class User(db.Model): #데이터 모델을 나타내는 객체 선언  
    userid = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(32), nullable=False)
    pwd = db.Column(db.String(8), nullable=False)

    def __init__(self, email, pwd):
        self.email = email
        self.set_password(pwd)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
 
    def check_password(self, password):
        return check_password_hash(self.password, password)