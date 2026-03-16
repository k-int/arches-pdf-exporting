import logging

from django.urls import get_script_prefix, resolve, reverse
from django.utils.translation import gettext as _

from arches.app.models import models
from arches.app.models.system_settings import settings
from arches.app.utils.betterJSONSerializer import JSONDeserializer
from arches.app.utils.data_management.resources.exporter import ResourceExporter

logger = logging.getLogger(__name__)

from arches.app.search.search_export import SearchResultsExporter as ArchesSearchResultsExporter


class AppSearchResultsExporter(ArchesSearchResultsExporter):
    def __init__(self, search_request=None):
        super().__init__(search_request)
    
    def pdf_export(self, format, report_link):
        super().export(format, report_link)

        ret = []
        search_results_path = reverse("search_results")
        if search_results_path.startswith(get_script_prefix()):
            search_results_path = search_results_path.replace(get_script_prefix(), "/")
        func, args, kwargs = resolve(search_results_path)
        kwargs["request"] = self.search_request
        search_res_json = func(*args, **kwargs)
        if search_res_json.status_code == 500:
            return ret
        results = JSONDeserializer().deserialize(search_res_json.content)
        instances = results["results"]["hits"]["hits"]
        output = {}

        for resource_instance in instances:
            use_fieldname = self.format in ("shp",)
            resource_obj = self.flatten_tiles(
                resource_instance["_source"]["tiles"],
                self.datatype_factory,
                compact=self.compact,
                use_fieldname=use_fieldname,
            )
            has_geom = resource_obj.pop("has_geometry")
            skip_resource = self.format in ("shp",) and has_geom is False
            if skip_resource is False:
                try:
                    output[resource_instance["_source"]["graph_id"]]["output"].append(
                        resource_obj
                    )
                except KeyError:
                    output[resource_instance["_source"]["graph_id"]] = {"output": []}
                    output[resource_instance["_source"]["graph_id"]]["output"].append(
                        resource_obj
                    )

        for graph_id, resources in output.items():
            graph = models.GraphModel.objects.get(pk=graph_id)

            if (report_link == "true") and (format != "tilexl"):
                for resource in resources["output"]:
                    report_url = reverse(
                        "resource_report", kwargs={"resourceid": resource["resourceid"]}
                    )
                    export_namespace = settings.ARCHES_NAMESPACE_FOR_DATA_EXPORT.rstrip(
                        "/"
                    )
                    resource["Link"] = f"{export_namespace}{report_url}"

            if format == "pdf":
                ret += self.to_html(
                    resources["output"], name=graph.name, graph_id=str(graph.pk)
                )

        full_path = self.search_request.get_full_path()
        search_request_path = (
            self.search_request.path if full_path is None else full_path
        )
        search_export_info = models.SearchExportHistory(
            user=self.search_request.user,
            numberofinstances=len(instances),
            url=search_request_path,
        )
        search_export_info.save()

        return ret, search_export_info

    # copied from the core Arches class, but modified for format=pdf rather than html 
    def to_html(self, instances, name, graph_id):
        resourceinstanceids = [
            instance["resourceid"] for instance in instances if "resourceid" in instance
        ]
        html_exporter = ResourceExporter(format="pdf")
        dest = html_exporter.export(resourceinstanceids=resourceinstanceids)
        return dest
