import {setCheckableLabel} from "../../modules/common"
import {BibLatexApiImporter} from "../../modules/citation_api_import"

export class BibLatexApiImporterCitationDialog {
    constructor(citationDialog) {
        this.citationDialog = citationDialog
    }

    init() {
        this.addButton()
    }

    addButton() {
        this.citationDialog.buttons.unshift({
            text: gettext('Import from database'),
            click: () => {
                this.initImporter()
            },
            class: 'fw-button fw-light fw-add-button'
        })
    }

    initImporter() {
        //import via web api
        const apiImporter = new BibLatexApiImporter(
            this.citationDialog.editor.mod.db.bibDB,
            bibEntries => {
                this.citationDialog.addToCitableItems(bibEntries)
            }
        )

        apiImporter.init()
    }
}
