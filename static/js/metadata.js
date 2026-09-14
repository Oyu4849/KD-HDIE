/*
------------------------------------------------------------
KD-HDIE Framework

Metadata Explorer

Scientific UI Controller
------------------------------------------------------------
*/

"use strict";


class MetadataExplorer {

    constructor() {

        this.attributeItems =
            document.querySelectorAll(".attribute-item");

        this.detailsPanel =
            document.getElementById("attribute-details");

        this.initialize();

    }

    initialize() {

        this.attributeItems.forEach(item => {

            item.addEventListener(
                "click",
                () => this.select(item)
            );

        });

    }

    select(item) {

        this.clearSelection();

        item.classList.add("active");

        const attribute = {

            name:
                item.dataset.attribute,

            count:
                item.dataset.count,

            domain:
                item.dataset.domain || "-",

            datatype:
                item.dataset.datatype || "-",

            unit:
                item.dataset.unit || "-",

            semantic:
                item.dataset.semantic || "Validated",

            quality:
                item.dataset.quality || "1.00",

            conflict:
                item.dataset.conflict || "No",

            fusion:
                item.dataset.fusion || "Included"

        };

        this.render(attribute);

    }

    clearSelection() {

        this.attributeItems.forEach(item => {

            item.classList.remove("active");

        });

    }

    render(attribute) {

        this.detailsPanel.innerHTML = `

<div class="table-responsive">

<table class="table table-bordered align-middle">

<tr>

<th width="35%">

Canonical Attribute

</th>

<td>

${this.pretty(attribute.name)}

</td>

</tr>

<tr>

<th>

Occurrences

</th>

<td>

${attribute.count}

</td>

</tr>

<tr>

<th>

Domain

</th>

<td>

${attribute.domain}

</td>

</tr>

<tr>

<th>

Datatype

</th>

<td>

${attribute.datatype}

</td>

</tr>

<tr>

<th>

Unit

</th>

<td>

${attribute.unit}

</td>

</tr>

<tr>

<th>

Semantic Status

</th>

<td>

<span class="badge bg-success">

${attribute.semantic}

</span>

</td>

</tr>

<tr>

<th>

Quality Score

</th>

<td>

${attribute.quality}

</td>

</tr>

<tr>

<th>

Conflict

</th>

<td>

${attribute.conflict}

</td>

</tr>

<tr>

<th>

Fusion

</th>

<td>

${attribute.fusion}

</td>

</tr>

</table>

</div>

`;

    }

    pretty(value) {

        return value

            .replaceAll("_", " ")

            .replace(/\b\w/g, c => c.toUpperCase());

    }

}


document.addEventListener(

    "DOMContentLoaded",

    () => {

        new MetadataExplorer();

    }

);