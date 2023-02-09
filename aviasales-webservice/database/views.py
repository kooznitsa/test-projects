from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from database.database import Database


FILES = ['database/files/RS_ViaOW.xml', 'database/files/RS_Via-3.xml',]


def populate_database(request: HttpRequest) -> HttpResponse:
    for file in FILES:
        data = Database(file).parse_xml()
    
    context = {'data': data}
    return render(request, 'database/database.html', context)