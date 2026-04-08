from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from io import StringIO

from arches.app.utils.data_management.resources.formats.htmlfile import HtmlWriter
from arches.app.utils.data_management.resources.exporter import ResourceExporter

class PrintReportView(View):

    def get(self, request, resourceid=None):

        # Call HTML exporter - pass in our single resource id
        html_exporter = ResourceExporter(format="html")
        resource = html_exporter.export(resourceinstanceids=[resourceid])

        # exporter returns file object, with file + content as stringIO, so we convert it back to html
        html_content = resource[0]["outputfile"].getvalue()

        return HttpResponse(html_content)