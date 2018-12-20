from app import db
from sqlalchemy import Column, String, Integer, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import backref, relationship

class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    date_created = Column(DateTime, default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp())
    status = Column(Integer, default=0)

class Address(Base):
    __tablename__ = "address"

    line1 = Column(String(256))
    line2 = Column(String(256))
    line3 = Column(String(256))
    county = Column(String(256))
    postcode = Column(String(256))

class EventRole(Base):
    __tablename__ = "event_role"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))
    status = Column(Integer, nullable=False, default=0)

class User(Base):
    __tablename__ = "user"

    username = Column(String(64), nullable=False, unique=True)
    forename = Column(String(128))
    surname = Column(String(128))
    dob = Column(Date)
    email_address = Column(String(512))

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", backref=backref("user_address", uselist=False))

    default_event_role_id = Column(Integer, ForeignKey("event_role.id"))
    default_event_role = relationship("EventRole")    

class ChargeType(Base):
    __tablename__ = "charge_type"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class WeatherCondition(Base):
    __tablename__ = "weather_condition"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class EventType(Base):
    __tablename__ = "event_type"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

    default_charge_type_id = Column(Integer, ForeignKey("charge_type.id"))
    default_charge_type = relationship("ChargeType")

class EventLocation(Base):
    __tablename__ = "event_location"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))
    contact_name = Column(String(512))
    contact_email_address = Column(String(512))
    contact_telephone1 = Column(String(64))
    contact_telephone2 = Column(String(64))

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address")

class Partnership(Base):
    __tablename__ = "partnership"

    name = Column(String(256), nullable=False, unique=True) 
    description = Column(String(512))

class Event(Base):
    __tablename__ = "event"

    description = Column(String(512))
    notes = Column(String(2048))
    start = Column(DateTime)
    duration_minutes = Column(Integer)

    location_id = Column(Integer, ForeignKey("event_location.id"))
    location = relationship("EventLocation")
    event_type_id = Column(Integer, ForeignKey("event_type.id"))
    event_type = relationship("EventType")
    charge_type_id = Column(Integer, ForeignKey("charge_type.id"))
    charge_type = relationship("ChargeType")

class Participation(Base):
    __tablename__ = "participation"

    notes = Column(String(2048))
    duration_minutes = Column(Integer, default=0)

    event_role_id = Column(Integer, ForeignKey("event_role.id"))
    event_role = relationship("EventRole")

    partnership_id = Column(Integer, ForeignKey("partnership.id"))
    partnership = relationship("Partnership")

    event_id = Column(Integer, ForeignKey("event.id"))
    event = relationship("Event")

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", backref=backref("participants"))

def generate_controller(class_type, item_type_name, controller_method_name, controller_url, output_filepath):
    template = None
    with open("controller_template.txt", "r") as fs:
        template = fs.read()

    template = template.replace("$CLASSNAME$", class_type.__name__)
    template = template.replace("$ITEMTYPENAME$", item_type_name)
    template = template.replace("$CONTROLLERMETHODNAME$", controller_method_name)
    template = template.replace("$CONTROLLERURL$", controller_url)

    with open(output_filepath, "w+") as fs:
        fs.write(template)