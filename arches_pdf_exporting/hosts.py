import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(
        re.sub(r"_", r"-", r"arches_pdf_exporting"),
        "arches_pdf_exporting.urls",
        name="arches_pdf_exporting",
    ),
)
