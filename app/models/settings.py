from app.models.base import db, BaseModel


class Settings(BaseModel, db.Model):
	__tablename__ = 'settings'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	company_name = db.Column(db.String(255), nullable=False)
	base_rate = db.Column(db.Float, nullable=False)
	distance_rate = db.Column(db.Float, nullable=False)
	time_rate = db.Column(db.Float, nullable=False)
	peak_start_time = db.Column(db.String(4))
	peak_end_time = db.Column(db.String(4))
	peak_surcharge = db.Column(db.Float, nullable=False)

	def __init__(self, company_name, base_rate, distance_dict, time_dict, peak_surcharge):
		self.company_name = company_name
		self.base_rate = base_rate
		self.distance_rate = distance_dict['price']
		self.time_rate = time_dict['price']
		self.peak_surcharge = peak_surcharge

	def __repr__(self):
		return "<App Settings Object>"

	@staticmethod
	def get_rates():
		settings = Settings.query.filter_by(id=1).first()
		return {
			"base_rate": settings.base_rate,
			"distance_rate": settings.distance_rate,
			"time_rate": settings.time_rate,
			"peak_surcharge": settings.peak_surcharge
		}

	@staticmethod
	def is_peak_chargeable():
		return False
