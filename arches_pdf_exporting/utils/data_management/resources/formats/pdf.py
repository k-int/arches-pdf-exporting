import os
import logging
from functools import lru_cache
from uuid import UUID
from io import StringIO, BytesIO
import weasyprint
from pathlib import Path

from django.template import Context, Template, TemplateDoesNotExist
from django.template.loader import get_template
from arches.app.models.models import GraphModel
from arches.app.models.resource import Resource
from arches.app.models.system_settings import settings
from arches.app.utils.data_management.resources.formats.format import Writer
from arches.app.utils.data_management.resources.formats.htmlfile import HtmlWriter

logger = logging.getLogger(__name__)

class PdfWriter(HtmlWriter):
    def __init__(self, **kwargs):
        super(HtmlWriter, self).__init__(**kwargs)

    def write_resources(self, graph_id=None, resourceinstanceids=None, **kwargs):
        """
        Returns a list of dictionaries representing the generated html files with the following format:
        [
            {'name':file name, 'outputfile': a StringIO() buffer of resource instance data in the specified format},
            {'name':file name, 'outputfile': a StringIO()},
            ...
            ...
        ]
        """

        valid_graphs = HtmlWriter.get_graphids_with_export_template()
        if len(valid_graphs) == 0:
            logger.warning(
                "There are no valid graph html templates in the project - cannot generate html exports."
            )
            return []

        user = kwargs.get("user", None)
        resources_list = self.fetch_resource_objects_list(
            resourceinstanceids=resourceinstanceids,
            user=user,
            allowed_graph_ids=valid_graphs,
        )
        files = self.generate_pdf_files(resources_list)

        return files

    def generate_pdf_files(self, resource_object_list=None):
        """
        uses the provided resource object list to generate a set of html file objects required by the Arches ResourceExporter.

        """
        files = []
        for gid in resource_object_list.keys():
            template = self.load_html_template(gid)

            content = template.render({"resources": resource_object_list[gid]})

            # Rather than StringIO we use BytesIO here
            dest = BytesIO()
            # Convert the rendered HTML to a PDF
            pdf = weasyprint.HTML(string=content).write_pdf()
            dest.write(pdf)

            files.append(
                {
                    "name": f"{str(GraphModel.objects.get(pk=gid))}.pdf",
                    "outputfile": dest,
                }
            )

        return files
