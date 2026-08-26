define([
    'knockout',
    'arches',
    'knockout-mapping', 
    'underscore', 
    'moment', 
    'bindings/let', 
    'views/components/simple-switch'
], function (ko, arches, koMapping, _, moment) {
    var ReportViewModel = function(params) {
        var self = this;

        this.report = params.report || null;
        this.summary = params.summary || false;
        this.reportDate = moment().format('MMMM D, YYYY');
        this.configForm = params.configForm || false;
        this.configType = params.configType || 'header';
        this.editorContext = params.editorContext || false;

        this.configState = params.report.configState || ko.observable({});
        this.configJSON = params.report.configJSON || ko.observable({});
        this.configObservables = params.configObservables || {};
        this.configKeys = params.configKeys || [];

        this.hasProvisionalData = ko.pureComputed(function() {
            return _.some(self.tiles(), function(tile){
                return _.keys(ko.unwrap(tile.provisionaledits)).length > 0;
            });
        });
        
        this.hideEmptyNodes = ko.observable(params.report.hideEmptyNodes);

        this.configJSON = ko.computed(function(){
            self.configKeys.forEach(function(config) {
                self[config] = self.configState[config];
            });
            self.report.configJSON(koMapping.toJS(self.report.configState));
            return self.report.configJSON;
        }).extend({deferred: true});

        var getCardTiles = function(card, tiles) {
            var cardTiles = ko.unwrap(card.tiles);
            cardTiles.forEach(function(tile) {
                tiles.push(tile);
                tile.cards.forEach(function(card) {
                    getCardTiles(card, tiles);
                });
            });
        };

        this.tiles = ko.computed(function() {
            var tiles = [];
            if (self.report) {
                ko.unwrap(self.report.cards).forEach(function(card) {
                    getCardTiles(card, tiles);
                });
            }
            return tiles;
        });

        // Copied from core Arches so we can extend with this function
        this.exportSinglePdf = function () {
            const resourceId = self.report.report_json.resourceinstanceid

            this.url = function() {
                let url = arches.urls.export_results;
                let urlparams = {
                    format: "pdf",
                    reportlink: false,
                    precision: 6,
                    total: 1,
                    exportsystemvalues: false,
                    exportresperpdf: true,
                    "term-filter": JSON.stringify([{
                        "inverted": false, 
                        "type": "string", 
                        "context": "", 
                        "context_label": "", 
                        "id": resourceId, 
                        "text": `Contains Term: ${resourceId}`, 
                        "value": resourceId, 
                        "selected": true 
                    }])
                }
                url = url + '?' + $.param(urlparams);
                return url;
            };

            window.open(this.url());
        };
    };
    return ReportViewModel;
});
