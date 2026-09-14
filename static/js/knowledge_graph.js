/*
==============================================================

KD-HDIE Framework

Knowledge Graph Engine

Author:
Oybek Xolmuminov

==============================================================
*/

"use strict";

class KnowledgeGraph {

    constructor() {

        this.apiUrl = "/systems/api/knowledge-graph/";

        this.network = null;

        this.nodes = [];

        this.edges = [];

        this.container =
            document.getElementById(
                "knowledge-network"
            );

        this.initialize();

    }

    /*
    ==========================================================
    Initialization
    ==========================================================
    */

    async initialize() {

        this.registerEvents();

        await this.loadGraph();

    }

    /*
    ==========================================================
    Load Graph
    ==========================================================
    */

    async loadGraph() {

        try {

            this.showLoading();

            const response =
                await fetch(
                    this.apiUrl
                );

            if (!response.ok) {

                throw new Error(
                    "Unable to load graph."
                );

            }

            const result =
                await response.json();

            this.nodes =
                result.data.nodes || [];

            this.edges =
                result.data.edges || [];

            this.render();

            this.updateStatistics();

        }

        catch (error) {

            console.error(error);

            this.showError();

        }

    }

    /*
    ==========================================================
    Render Network
    ==========================================================
    */

    render() {

        const data = {

            nodes:
                new vis.DataSet(
                    this.nodes
                ),

            edges:
                new vis.DataSet(
                    this.edges
                )

        };

        const options = {

            autoResize: true,

            interaction: {

                hover: true,

                navigationButtons: true,

                keyboard: true,

            },

            physics: {

                stabilization: true,

                barnesHut: {

                    springLength: 180,

                    damping: 0.5,

                }

            },

            layout: {

                improvedLayout: true,

            },

            edges: {

                smooth: true,

                arrows: {

                    to: {

                        enabled: true,

                        scaleFactor: 0.6,

                    }

                }

            },

            nodes: {

                shape: "dot",

                size: 20,

                font: {

                    size: 14,

                }

            }

        };

        this.network =
            new vis.Network(

                this.container,

                data,

                options,

            );

        this.registerNetworkEvents();

    }
    /*
    ==========================================================
    Network Events
    ==========================================================
    */

    registerNetworkEvents() {

        this.network.on("click", (params) => {

            if (params.nodes.length === 0) {

                return;

            }

            const nodeId = params.nodes[0];

            this.showNodeDetails(nodeId);

        });

    }


    /*
    ==========================================================
    Node Details
    ==========================================================
    */

    showNodeDetails(nodeId) {

        const node = this.nodes.find(
            item => item.id === nodeId
        );

        if (!node) {

            return;

        }

        const panel =
            document.getElementById(
                "node-details"
            );

        if (!panel) {

            return;

        }

        panel.innerHTML = `

<div class="card border-0">

<div class="card-body">

<h5 class="fw-bold mb-3">

${node.label}

</h5>

<table class="table table-sm">

<tr>

<th>ID</th>

<td>${node.id}</td>

</tr>

<tr>

<th>Domain</th>

<td>${node.group}</td>

</tr>

<tr>

<th>Connections</th>

<td>

${this.getConnectionCount(node.id)}

</td>

</tr>

</table>

</div>

</div>

`;

    }


    /*
    ==========================================================
    Connection Counter
    ==========================================================
    */

    getConnectionCount(nodeId) {

        return this.edges.filter(edge =>

            edge.from === nodeId ||

            edge.to === nodeId

        ).length;

    }


    /*
    ==========================================================
    Statistics
    ==========================================================
    */

    updateStatistics() {

        const nodeCounter =
            document.getElementById(
                "graph-node-count"
            );

        const edgeCounter =
            document.getElementById(
                "graph-edge-count"
            );

        if (nodeCounter) {

            nodeCounter.innerText =
                this.nodes.length;

        }

        if (edgeCounter) {

            edgeCounter.innerText =
                this.edges.length;

        }

    }


    /*
    ==========================================================
    Refresh
    ==========================================================
    */

    async refresh() {

        await this.loadGraph();

    }


    /*
    ==========================================================
    Loading
    ==========================================================
    */

    showLoading() {

        this.container.innerHTML = `

<div class="d-flex
justify-content-center
align-items-center
h-100">

<div class="text-center">

<div class="spinner-border
text-primary
mb-3">

</div>

<h5>

Loading Knowledge Graph...

</h5>

</div>

</div>

`;

    }


    /*
    ==========================================================
    Error
    ==========================================================
    */

    showError() {

        this.container.innerHTML = `

<div class="d-flex
justify-content-center
align-items-center
h-100">

<div class="text-center">

<i class="bi bi-exclamation-circle
display-4
text-danger">

</i>

<h5 class="mt-3">

Unable to load graph

</h5>

</div>

</div>

`;

    }
    /*
    ==========================================================
    Search
    ==========================================================
    */

    search(keyword) {

        keyword = keyword.toLowerCase();

        const matched = this.nodes
            .filter(node =>

                node.label
                    .toLowerCase()
                    .includes(keyword)

            )
            .map(node => node.id);

        this.network.selectNodes(matched);

        if (matched.length > 0) {

            this.network.focus(

                matched[0],

                {

                    scale: 1.3,

                    animation: true,

                }

            );

        }

    }


    /*
    ==========================================================
    Domain Filter
    ==========================================================
    */

    filter(domain) {

        if (domain === "all") {

            this.network.setData({

                nodes: new vis.DataSet(this.nodes),

                edges: new vis.DataSet(this.edges)

            });

            return;

        }

        const nodes = this.nodes.filter(

            node => node.group === domain

        );

        const ids = nodes.map(

            node => node.id

        );

        const edges = this.edges.filter(

            edge =>

                ids.includes(edge.from) ||

                ids.includes(edge.to)

        );

        this.network.setData({

            nodes: new vis.DataSet(nodes),

            edges: new vis.DataSet(edges),

        });

    }


    /*
    ==========================================================
    Layout
    ==========================================================
    */

    changeLayout(layout) {

        if (layout === "hierarchical") {

            this.network.setOptions({

                physics: false,

                layout: {

                    hierarchical: {

                        enabled: true,

                        direction: "UD",

                        sortMethod: "directed",

                    }

                }

            });

        }

        else {

            this.network.setOptions({

                physics: true,

                layout: {

                    hierarchical: false,

                }

            });

        }

    }


    /*
    ==========================================================
    UI Events
    ==========================================================
    */

    registerEvents() {

        const refreshButton =
            document.getElementById(
                "refresh-graph"
            );

        if (refreshButton) {

            refreshButton.addEventListener(

                "click",

                () => this.refresh()

            );

        }

        const searchBox =
            document.getElementById(
                "graph-search"
            );

        if (searchBox) {

            searchBox.addEventListener(

                "keyup",

                event =>

                    this.search(
                        event.target.value
                    )

            );

        }

        const domain =
            document.getElementById(
                "graph-domain"
            );

        if (domain) {

            domain.addEventListener(

                "change",

                event =>

                    this.filter(
                        event.target.value
                    )

            );

        }

        const layout =
            document.getElementById(
                "graph-layout"
            );

        if (layout) {

            layout.addEventListener(

                "change",

                event =>

                    this.changeLayout(
                        event.target.value
                    )

            );

        }

    }

}


/*
==============================================================
Start Application
==============================================================
*/

document.addEventListener(

    "DOMContentLoaded",

    () => {

        new KnowledgeGraph();

    }

);