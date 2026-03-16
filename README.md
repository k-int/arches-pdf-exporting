# Arches PDF Exporting

An Arches application to extend Arches search exports with an option for PDF exporting. 
The PDF export option uses the HTML templating and export back-end functionality, but converts the resulting HTML file into a PDF as the final step. Resources can be exported in the standard format, where N resources are included in one file, or each of N resources can be exported into their own file. 

In addition to offering a new search export, this application adds a button to the Arches report for exporting individual resources to PDF. This offers as an alternative to the "print" feature. 

Note that the export option and report button will only become visible if HTML templates are present within a project or application.

## Project Configuration

1. If you don't already have an Arches project, you'll need to create one by following the instructions in the Arches [documentation](http://archesproject.org/documentation/).

2. When your project is ready, add "arches_templating", "arches_for_science", and "pgtrigger" to INSTALLED_APPS **below** the name of your project:
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
        re_path(r"^search/export_results$", search.export_results, name="export_results"),
    ]
    ```

5. Start your project
    ```
    python manage.py runserver
    ```

6. Install and build front-end dependencies:
    ```
    npm install
    npm run build_development (or npm run start)
    ```