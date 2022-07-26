from reportlab.lib import colors
from reportlab.lib.colors import blue
from reportlab.lib.pagesizes import LETTER, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, SimpleDocTemplate, TableStyle

from application.models import Dimension
import json


def create_pdf(username):
    doc = SimpleDocTemplate('dimension_' + username + ".pdf", pagesize=letter)
    # container for the 'Flowable' objects
    elements = []
    data = [['Name of dimension', 'Dimension']]
    a = Dimension.query.filter_by(name=username)
    size = 1
    for dimens in a:
        size += 1
        data.append([dimens.dimension_name, dimens.dimension])
    t = Table(data, 2 * [2 * inch], size * [0.4 * inch])
    t.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    elements.append(t)
    doc.build(elements)

def create_json(username):
    data=[]
    a = Dimension.query.filter_by(name=username)
    for dimens in a:
        temp={"Name of dimension":dimens.dimension_name,'Dimension':dimens.dimension}
        data.append(temp)
    with open('dimension_' + username + ".json", 'w') as f:
        json.dump(data, f)