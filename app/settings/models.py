from ..extensions import db


class Settings(db.Model):
    """ Settings Model for storing settings related details """
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    driver_seat_tilt = db.Column(db.Integer, nullable=False)
    passenger_seat_tilt = db.Column(db.Integer, nullable=False)
    driver_mirror_tilt_X = db.Column(db.Integer, nullable=False)
    driver_mirror_tilt_Y = db.Column(db.Integer, nullable=False)
    passenger_mirror_tilt_X = db.Column(db.Integer, nullable=False)
    passenger_mirror_tilt_Y = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, driver_seat_tilt=100, passenger_seat_tilt=100, driver_mirror_tilt_X=180,
                 driver_mirror_tilt_Y=180, passenger_mirror_tilt_X=180, passenger_mirror_tilt_Y=180):
        self.user_id = user_id
        self.driver_seat_tilt = driver_seat_tilt
        self.passenger_seat_tilt = passenger_seat_tilt
        self.driver_mirror_tilt_X = driver_mirror_tilt_X
        self.driver_mirror_tilt_Y = driver_mirror_tilt_Y
        self.passenger_mirror_tilt_X = passenger_mirror_tilt_X
        self.passenger_mirror_tilt_Y = passenger_mirror_tilt_Y
