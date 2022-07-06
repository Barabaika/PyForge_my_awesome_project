from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String
import requests

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


Base = declarative_base()


class Compound(Base):
    __tablename__ = "compounds"

    compound = Column(String(), unique=True, nullable=False, primary_key=True)
    formula = Column(String(), unique=True, nullable=False)
    inchi = Column(String())
    inchi_key = Column(String())
    smiles = Column(String())
    cross_links_count = Column(String())

    def __init__(
        self, compound, name, formula, inchi, inchi_key, smiles, cross_links_count
    ):
        self.compound = compound
        self.name = name
        self.formula = formula
        self.inchi = inchi
        self.inchi_key = inchi_key
        self.smiles = smiles
        self.cross_links_count = cross_links_count

    @staticmethod
    def from_json(json_dct, compound_name):
        json_compound = Compound(
            compound_name,
            json_dct["name"],
            json_dct["formula"],
            json_dct["inchi"],
            json_dct["inchi_key"],
            json_dct["smiles"],
            len(json_dct["cross_links"]),
        )
        return json_compound


def get_data_from_https(url):
    response = requests.request("GET", url)
    response_dict = response.json()
    assert len(response_dict) == 1, f"Wrong format of data taken from {url}"

    return response_dict
