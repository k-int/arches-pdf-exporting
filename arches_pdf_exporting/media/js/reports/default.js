define([
    'jquery',
    'knockout',
    'arches',
    'viewmodels/report',
    'templates/views/report-templates/default.htm'
], function($, ko, arches, ReportViewModel, defaultReportTemplate) {
    return ko.components.register('default-report', {
        viewModel: function(params) {
            params.configKeys = [];

            ReportViewModel.apply(this, [params]);


            // this.getExportData = function(){
            //     var payload = ko.unwrap(this.query);
            //     self.downloadPending(true);
            //     payload.format = this.format();
            //     payload.reportlink = this.reportlink();
            //     payload.precision = this.precision();
            //     payload.total = this.total();
            //     payload.email = this.emailInput();
            //     payload.exportName = this.exportName() || "Arches Export";
            //     payload.exportsystemvalues = this.exportSystemValues();
            //     $.ajax({
            //         type: "GET",
            //         url: arches.urls.export_results,
            //         data: payload
            //     }).done(function(response) {
            //         self.downloadPending(false);
            //         self.downloadStarted(true);
            //         window.setTimeout(function(){
            //             self.downloadStarted(false);
            //         }, 9000);
            //         self.result(response.message);
            //     });
            // };

            var resourceId = params.resourceid || params.resourceinstanceid ||
                (this.resourceid && ko.unwrap(this.resourceid)) ||
                (this.resourceinstanceid && ko.unwrap(this.resourceinstanceid)) ||
                (this.report && this.report.resourceinstanceid);

            this.exportSinglePdf = function() {

                var id = ko.unwrap(resourceId);
                if (!id) {
                    return;
                }

                var exportUrl = arches.urls.export_results + '?' + $.param({
                    resourceinstanceids: [id],
                    format: 'pdf',
                    reportlink: false,
                    total: 1,
                    precision: 6,
                    exportresperpdf: true,
                    exportsystemvalues: false,
                });

                window.open(exportUrl, '_blank');
            };
        },
        template: defaultReportTemplate
    });
});
