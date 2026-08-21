# Arches PDF Exporting

An Arches application to extend Arches search exports with an option for PDF exporting. 
The PDF export option uses the HTML templating and export back-end functionality, but converts the resulting HTML file into a PDF as the final step. Resources can be exported in the standard format, where N resources are included in one file, or each of N resources can be exported into their own file. 

In addition to offering a new search export, this application adds a button to the Arches report for exporting individual resources to PDF. This offers as an alternative to the "print" feature. 

Note that the export option and report button will only become visible if HTML templates are present within a project or application.

## Project Configuration

1. If you don't already have an Arches project, you'll need to create one by following the instructions in the Arches [documentation](http://archesproject.org/documentation/).

2. When your project is ready, add "arches_pdf_exporting" to INSTALLED_APPS **below** the name of your project:
    ```
    INSTALLED_APPS = (
        ...
        "my_project_name",
        "arches_pdf_exporting",
    )
    ```

3. Add the following formatter to your project's settings.py file
    ```
    # Add PDF writer to FORMATTERS
    RESOURCE_FORMATTERS["pdf"] = "arches_pdf_exporting.utils.data_management.resources.formats.pdf.PdfWriter"
    ```

4. Update urls.py to include the arches-pdf-exporting urls
    ```
    urlpatterns = [
        path("", include("arches_pdf_exporting.urls")),
    ]
    ```

5. This application requires the pip package [weasyprint](https://pypi.org/project/weasyprint/). Run `pip install weasyprint` to install the package. There are also some additional installation steps which can be found on the weasyprint [documentation site](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation), e.g. for Ubuntu you also need to run `sudo apt install libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-subset0`

6. Start your project
    ```
    python manage.py runserver
    ```

7. Install and build front-end dependencies:
    ```
    npm install
    npm run build_development (or npm run start)
    ```

## Core Arches modification

Since this Arches extension adds functionality that cannot be directly added by natively extending core Arches, certain files have been copied from core Arches (7.6.x). These files, and their reasonings, are:

- media/js/views/components/search/search-export.js
- templates/views/components/search/search-export.htm
- search/search_export.py
- views/search.py
To implement the PDF search export option, and the routing logic when the PDF option is selected.

- urls.py
- templates/arches_urls.htm
Our overwritten search export URL is defined here, both for the backend endpoint and the referenced arches.url used in the report.js function.

- tasks.py
Overwrites the `export_search_results` celery task to incorporate the PDF exporting task logic.

- media/js/viewmodels/report.js
Overwrites and extends the default report javascript to include our footer button function.

- templates/views/components/report-templates.htm
Not necessarily a file overwritten, but this extends the footer of all default report templates to include the export PDF button. Note: this does not appear for Arches for HERs reports.  