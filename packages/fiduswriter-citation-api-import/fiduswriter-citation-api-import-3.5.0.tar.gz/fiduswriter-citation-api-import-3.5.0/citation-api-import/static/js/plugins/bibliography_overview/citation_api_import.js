import {BibLatexApiImporter} from "../../modules/citation_api_import"

export class BibLatexApiImporterBibliographyOverview {
    constructor(bibliographyOverview) {
        this.bibliographyOverview = bibliographyOverview
    }

    init() {
        this.addButton()
    }

    addButton() {
        this.bibliographyOverview.menu.model.content.push({
            type: 'button',
            icon: 'database',
            title: gettext('Import from Database'),
            action: overview => {
                const apiImporter = new BibLatexApiImporter(
                    overview.bibDB,
                    bibEntries => overview.addBibList(bibEntries)
                )
                apiImporter.init()
            }
        })
        this.bibliographyOverview.menu.update()
    }

}
