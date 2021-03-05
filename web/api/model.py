from api import db


class Person(db.Model):
    """This class represents a person.

    Args:
        cpf (string): CPF number of the person (unique, 11 digits)
        name (string): full name of the person
    """

    __tablename__ = "people"

    cpf = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    companies = db.relationship('Company')
    assets = db.relationship('Asset')

    def __init__(self, cpf, name):
        self.cpf = cpf
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Person.query.all()

    @staticmethod
    def get(cpf):
        return Person.query.get(cpf)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Person: {self.name} (CPF: {self.cpf})>"


class Company(db.Model):
    """This class represents a comapny.

    Args:
        cnpj (string): CNPJ number of the company (unique, 14 digits)
        name (string): full name of the company
        parent (string): CNPJ or CPF number of the parent (person or company)
    """

    __tablename__ = "companies"
    __table_args__ = (
        (db.CheckConstraint('num_nonnulls(parent_cnpj, parent_cpf) = 1', name='single_parent')),
    )

    cnpj = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_cnpj = db.Column(db.String(30), db.ForeignKey('companies.cnpj'), name='parent_cnpj', nullable=True)
    parent_cpf = db.Column(db.String(20), db.ForeignKey('people.cpf'), name='parent_cpf', nullable=True)

    assets = db.relationship('Asset')
    children_company = db.relationship(
        'Company',
        remote_side='Company.cnpj',
        backref=db.backref('children_company'),
        single_parent=True)

    def __init__(self, cnpj, name, parent):
        self.cnpj = cnpj
        self.name = name

        if len(parent) == 14:
            self.parent_cpf = parent
        elif len(parent) == 18:
            self.parent_cnpj = parent

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Company.query.all()

    @staticmethod
    def get(cnpj):
        return Company.query.get(cnpj)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Company: {self.name} (CNPJ: {self.cnpj})>"


class Asset(db.Model):
    """This class represents any type of asset.

    Args:
        id_ (integer): Identification number of the asset
        value (numeric): estimated or market value
        description (string): general description of the asset
        date_acquisition (datetime): date at which it was obtained [OPTIONAL]
        parent (string): CNPJ or CPF number of the parent (person or company)
    """

    __tablename__ = "assets"
    __table_args__ = (
        (db.CheckConstraint('num_nonnulls(parent_cnpj, parent_cpf) = 1', name='single_parent')),
    )

    id_ = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date_acquisition = db.Column(db.DateTime)

    parent_cnpj = db.Column(db.String(30), db.ForeignKey('companies.cnpj'), name='parent_cnpj', nullable=True)
    parent_cpf = db.Column(db.String(20), db.ForeignKey('people.cpf'), name='parent_cpf', nullable=True)

    def __init__(self, id_, value, description, parent, date_acquisition=None):
        self.id_ = id_
        self.value = value
        self.description = description
        self.date_acquisition = date_acquisition

        if len(parent) == 14:
            self.parent_cpf = parent
        elif len(parent) == 18:
            self.parent_cnpj = parent

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Asset.query.all()

    @staticmethod
    def get(id_):
        return Asset.query.get(id_)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Asset: ({self.id_}) R${self.value} - {self.description}>"
