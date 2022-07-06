from flask.cli import FlaskGroup
from project import app, Compound, get_data_from_https
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import click
import pandas as pd

cli = FlaskGroup(app)

db_log_file_name = 'db.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG
db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)
db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

LIST_COMPOUNDS = ["ADP", "ATP", "STI", "ZID", "DPM", "XP9", "18W", "29P"]
database_url = os.getenv("DATABASE_URL", "sqlite://")
engine = create_engine(database_url, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


@cli.command("clear_db")
def clear_db():
    session.query(Compound).delete()
    session.commit()


@cli.command("add")
@click.option("--compound_name")
def add_compound(compound_name=None):

    assert (
        compound_name in LIST_COMPOUNDS
    ), f"Wrong or missing compound name: \n passed - {compound_name} \n available compounds {LIST_COMPOUNDS}"

    session.query(Compound).filter(Compound.compound.in_([compound_name])).delete()
    url_base = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/"
    url = url_base + compound_name
    response_dict = get_data_from_https(url)
    json_dct = response_dict[compound_name][0]
    comp = Compound.from_json(json_dct, compound_name)
    session.add(comp)
    session.commit()


@cli.command("print_info")
def print_info():
    print("check")
    pd.set_option("display.max_colwidth", 14)
    df = pd.read_sql(session.query(Compound).statement, session.bind)
    print(df)


if __name__ == "__main__":
    cli()
