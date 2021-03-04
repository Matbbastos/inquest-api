from api import db


class Person(db.Model):
    """This class represents a person"""

    __tablename__ = "people"

    cpf = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    companies = db.relationship('Company')
    assets = db.relationship('Asset')

    def __init__(self, cpf, name):
        """This is the constructor of the class

        Args:
            cpf (string): CPF number of the person (unique, 11 digits)
            name (string): full name of the person
        """
        self.cpf = cpf
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Person.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Person: {self.name} (CPF: {self.cpf})>"


class Company(db.Model):
    """This class represents a comapny"""

    __tablename__ = "companies"

    cnpj = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_cnpj = db.Column(db.String(30), db.ForeignKey('companies.cnpj'))
    parent_cpf = db.Column(db.String(20), db.ForeignKey('people.cpf'))

    assets = db.relationship('Asset')
    children_company = db.relationship('Company',
                                       remote_side='Company.cnpj',
                                       backref=db.backref('children_company'),
                                       single_parent=True)

    def __init__(self, cnpj, name):
        """This is the constructor of the class

        Args:
            cnpj (string): CNPJ number of the company (unique, 14 digits)
            name (string): full name of the company
        """
        self.cnpj = cnpj
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Company.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Company: {self.name} (CNPJ: {self.cnpj})>"


class Asset(db.Model):
    """This class represents any type of asset"""

    __tablename__ = "assets"

    id_ = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    date_acquisition = db.Column(db.DateTime)
    value = db.Column(db.Numeric)

    parent_cnpj = db.Column(db.String(30), db.ForeignKey('companies.cnpj'))
    parent_cpf = db.Column(db.String(20), db.ForeignKey('people.cpf'))

    def __init__(self, id_, description, date_acquisition=None, value=None):
        """This is the constructor of the class

        Args:
            id_ (integer): Identification number of the asset
            description (string): general description of the asset
            date_acquisition (datetime): date at which it was obtained
            value (numeric): estimated or market value
        """
        self.id_ = id_
        self.description = description
        self.date_acquisition = date_acquisition
        self.value = value

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Asset.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Asset: ({self.id_}) {self.description}>"
