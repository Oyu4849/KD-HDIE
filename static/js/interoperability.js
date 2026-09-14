class InteroperabilityExplorer {

    constructor() {

        this.config = {

            refreshInterval: 10000,

            animationDuration: 600,

            api: {

                knowledge: "/systems/api/knowledge-graph/",

                interoperability: "/systems/api/interoperability/",

                metadata: "/systems/api/metadata/",

                generic: "/systems/execute-generic-api/"

            }

        };

        this.data = {

            summary: {},

            attributes: [],

            semantic: [],

            conflicts: [],

            quality: {},

            fusion: {},

            unified: {},

            lastExecution: null

        };

        this.dom = {};

        this.refreshTimer = null;

    }

    /*==============================================================
    Initialize
    ==============================================================*/

    initialize() {

        console.log(
            "KD-HDIE Interoperability Explorer Started"
        );

        this.cacheDom();

        this.bindEvents();

        this.load();

        this.startAutoRefresh();

    }

    /*==============================================================
    DOM
    ==============================================================*/

    cacheDom() {

        this.dom.summaryCards =
            document.querySelectorAll("[data-summary]");

        this.dom.semanticRows =
            document.querySelectorAll("[data-semantic]");

        this.dom.qualityBars =
            document.querySelectorAll("[data-quality]");

        this.dom.fusionProgress =
            document.getElementById("fusionProgress");

        this.dom.modelStatus =
            document.getElementById("modelStatus");

        this.dom.genericForm =
            document.getElementById("genericApiForm");

        this.dom.genericResult =
            document.getElementById("genericApiResult");

        this.dom.genericButton =
            document.getElementById("genericApiExecute");

        this.dom.genericUrl =
            document.getElementById("genericApiUrl");

        this.dom.genericMethod =
            document.getElementById("genericApiMethod");

        this.dom.genericParams =
            document.getElementById("genericApiParams");

        this.dom.genericHeaders =
            document.getElementById("genericApiHeaders");

        this.dom.genericJson =
            document.getElementById("genericApiJson");

    }

    /*==============================================================
    Events
    ==============================================================*/

    bindEvents() {

        window.addEventListener(
            "resize",
            () => {
                console.log("Layout updated.");
            }
        );

        if (this.dom.genericForm) {

            this.dom.genericForm.addEventListener(
                "submit",
                (event) => {

                    event.preventDefault();

                    this.executeGenericAPI();

                }
            );

        }

        if (this.dom.genericButton) {

            this.dom.genericButton.addEventListener(
                "click",
                (event) => {

                    if (
                        this.dom.genericForm
                        && this.dom.genericForm.tagName === "FORM"
                    ) {
                        return;
                    }

                    event.preventDefault();

                    this.executeGenericAPI();

                }
            );

        }

    }

    /*==============================================================
    Load
    ==============================================================*/

    async load() {

        await this.loadKnowledgeGraph();

        this.updateSummary();

        this.updateSemantic();

        this.updateConflicts();

        this.updateQuality();

        this.updateFusion();

        this.updateUnifiedModel();

    }

    /*==============================================================
    Knowledge Graph
    ==============================================================*/

    async loadKnowledgeGraph() {

        try {

            const response = await fetch(
                this.config.api.knowledge,
                {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    }
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Knowledge Graph HTTP ${response.status}`
                );
            }

            const result = await response.json();

            if (result.success) {

                this.data.summary =
                    result.data || {};

            }

        }
        catch (error) {

            this.handleError(error);

        }

    }

    /*==============================================================
    Summary
    ==============================================================*/

    updateSummary() {

        const cards =
            document.querySelectorAll("[data-summary]");

        if (!cards.length) {
            return;
        }

        const summary = this.data.summary || {};

        const sources =
            summary.source_systems
            ?? summary.sources
            ?? summary.source_count
            ?? "-";

        const canonical =
            summary.canonical_attributes
            ?? summary.unique_attributes
            ?? "-";

        const semantic =
            this.toPercent(
                summary.semantic_coverage
                ?? summary.resolution_rate
            );

        const interoperability =
            summary.success === false
                ? "Error"
                : "Ready";

        const values = [
            sources,
            canonical,
            semantic,
            interoperability
        ];

        cards.forEach((card, index) => {

            if (values[index] !== undefined) {

                card.textContent = values[index];

            }

        });

    }

    /*==============================================================
    Semantic Mapping
    ==============================================================*/

    updateSemantic() {

        const summary =
            this.data.summary || {};

        const value =
            this.toPercent(
                summary.semantic_coverage
                ?? summary.resolution_rate
            );

        document
            .querySelectorAll("[data-semantic]")
            .forEach((bar) => {

                if (value !== null) {

                    bar.style.width = `${value}%`;

                    bar.textContent = `${value}%`;

                    bar.setAttribute(
                        "aria-valuenow",
                        value
                    );

                }

            });

    }

    /*==============================================================
    Conflict
    ==============================================================*/

    updateConflicts() {

        const summary =
            this.data.summary || {};

        const conflicts =
            Number(
                summary.conflicts
                ?? summary.total_conflicts
                ?? 0
            );

        document
            .querySelectorAll("[data-conflicts]")
            .forEach((element) => {

                element.textContent =
                    conflicts;

            });

        document
            .querySelectorAll(".badge")
            .forEach((item) => {

                const text =
                    item.textContent.trim();

                if (
                    text.includes("Resolved")
                    || text.includes("No Conflict")
                ) {

                    item.classList.remove(
                        "bg-danger"
                    );

                    item.classList.add(
                        "bg-success"
                    );

                }

            });

    }

    /*==============================================================
    Quality
    ==============================================================*/

    updateQuality() {

        const summary =
            this.data.summary || {};

        const value =
            this.toPercent(
                summary.quality_score
                ?? summary.quality
            );

        document
            .querySelectorAll("[data-quality]")
            .forEach((bar) => {

                if (value !== null) {

                    bar.style.width =
                        `${value}%`;

                    bar.textContent =
                        `${value}%`;

                    bar.setAttribute(
                        "aria-valuenow",
                        value
                    );

                }

            });

    }

    /*==============================================================
    Fusion
    ==============================================================*/

    updateFusion() {

        const progress =
            document.getElementById(
                "fusionProgress"
            );

        if (!progress) {
            return;
        }

        const summary =
            this.data.summary || {};

        const input =
            Number(
                summary.input_records ?? 0
            );

        const fused =
            Number(
                summary.fused_records ?? 0
            );

        let value = 0;

        if (input > 0) {

            value =
                Math.round(
                    (fused / input) * 100
                );

        }
        else if (
            summary.success === true
        ) {

            value = 100;

        }

        value =
            Math.max(
                0,
                Math.min(100, value)
            );

        progress.style.width =
            `${value}%`;

        progress.textContent =
            `${value}%`;

    }

    /*==============================================================
    Unified Information Model
    ==============================================================*/

    updateUnifiedModel() {

        const status =
            document.getElementById(
                "modelStatus"
            );

        if (!status) {
            return;
        }

        const summary =
            this.data.summary || {};

        if (summary.success === false) {

            status.textContent =
                "Error";

            return;

        }

        const finalRecords =
            Number(
                summary.final_records ?? 0
            );

        if (finalRecords > 0) {

            status.textContent =
                "Operational";

        }
        else if (
            summary.success === true
        ) {

            status.textContent =
                "Completed";

        }
        else {

            status.textContent =
                "Ready";

        }

    }

    /*==============================================================
    Generic API
    ==============================================================*/

    async executeGenericAPI() {

        const url =
            this.dom.genericUrl?.value.trim();

        const method =
            (
                this.dom.genericMethod?.value
                || "GET"
            ).toUpperCase();

        if (!url) {

            this.showGenericResult(
                false,
                "API URL is required."
            );

            return;

        }

        let params = {};
        let headers = {};
        let json = null;

        try {

            if (
                this.dom.genericParams
                && this.dom.genericParams.value.trim()
            ) {

                params =
                    JSON.parse(
                        this.dom.genericParams.value
                    );

            }

            if (
                this.dom.genericHeaders
                && this.dom.genericHeaders.value.trim()
            ) {

                headers =
                    JSON.parse(
                        this.dom.genericHeaders.value
                    );

            }

            if (
                this.dom.genericJson
                && this.dom.genericJson.value.trim()
            ) {

                json =
                    JSON.parse(
                        this.dom.genericJson.value
                    );

            }

        }
        catch (error) {

            this.showGenericResult(
                false,
                "Parameters, headers or JSON body must contain valid JSON."
            );

            return;

        }

        const payload = {

            url: url,

            method: method,

            params: params,

            headers: headers,

            json: json

        };

        this.setGenericLoading(true);

        try {

            const response =
                await fetch(
                    this.config.api.generic,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Accept":
                                "application/json"
                        },

                        body:
                            JSON.stringify(payload)
                    }
                );

            const result =
                await response.json();

            this.data.lastExecution =
                result;

            this.applyExecutionResult(
                result
            );

            this.showGenericResult(
                result.success,
                this.formatExecutionResult(
                    result
                )
            );

        }
        catch (error) {

            this.showGenericResult(
                false,
                error.message
            );

            this.handleError(error);

        }
        finally {

            this.setGenericLoading(false);

        }

    }

    /*==============================================================
    Apply Real Execution Result
    ==============================================================*/

    applyExecutionResult(result) {

        if (!result) {
            return;
        }

        if (result.statistics) {

            this.data.summary =
                result.statistics;

        }

        this.updateSummary();

        this.updateSemantic();

        this.updateConflicts();

        this.updateQuality();

        this.updateFusion();

        this.updateUnifiedModel();

    }

    /*==============================================================
    Format Result
    ==============================================================*/

    formatExecutionResult(result) {

        if (!result) {
            return "No response received.";
        }

        const statistics =
            result.statistics || {};

        const metadata =
            result.metadata || {};

        const lines = [

            `Status: ${
                result.success
                    ? "SUCCESS"
                    : "FAILED"
            }`,

            `Records: ${
                statistics.records
                ?? result.records_processed
                ?? 0
            }`,

            `Resolved attributes: ${
                statistics.resolved_attributes
                ?? 0
            }`,

            `Semantic coverage: ${
                this.toPercent(
                    statistics.semantic_coverage
                )
                ?? 0
            }%`,

            `Mapped attributes: ${
                statistics.mapped_attributes
                ?? 0
            }`,

            `Quality score: ${
                this.toPercent(
                    statistics.quality_score
                )
                ?? 0
            }%`,

            `Conflicts: ${
                statistics.conflicts
                ?? 0
            }`,

            `Reliability mean: ${
                statistics.reliability_mean
                ?? 0
            }`,

            `Final records: ${
                statistics.final_records
                ?? 0
            }`,

            `Normalizer: ${
                metadata.normalizer
                ?? "GenericJSONResponseNormalizer"
            }`

        ];

        if (
            result.message
            && result.message !==
                "Execution completed successfully."
        ) {

            lines.push(
                `Message: ${result.message}`
            );

        }

        if (
            result.errors
            && result.errors.length
        ) {

            lines.push(
                `Errors: ${result.errors.join("; ")}`
            );

        }

        return lines.join("\n");

    }

    /*==============================================================
    Generic Result UI
    ==============================================================*/

    showGenericResult(
        success,
        message
    ) {

        if (!this.dom.genericResult) {

            console.log(message);

            return;

        }

        this.dom.genericResult.textContent =
            message;

        this.dom.genericResult.classList.remove(
            "text-danger",
            "text-success"
        );

        this.dom.genericResult.classList.add(
            success
                ? "text-success"
                : "text-danger"
        );

    }

    setGenericLoading(isLoading) {

        if (!this.dom.genericButton) {
            return;
        }

        this.dom.genericButton.disabled =
            isLoading;

        this.dom.genericButton.textContent =
            isLoading
                ? "Ishlanmoqda..."
                : "API ni ishga tushirish";

    }

    /*==============================================================
    Auto Refresh
    ==============================================================*/

    startAutoRefresh() {

        if (this.refreshTimer) {
            clearInterval(
                this.refreshTimer
            );
        }

        this.refreshTimer =
            setInterval(
                () => {

                    this.load();

                },
                this.config.refreshInterval
            );

    }

    /*==============================================================
    Helpers
    ==============================================================*/

    toPercent(value) {

        if (
            value === null
            || value === undefined
            || value === ""
        ) {

            return null;

        }

        const number =
            Number(value);

        if (!Number.isFinite(number)) {

            return null;

        }

        if (
            number >= 0
            && number <= 1
        ) {

            return Math.round(
                number * 100
            );

        }

        return Math.round(
            Math.max(
                0,
                Math.min(
                    100,
                    number
                )
            )
        );

    }

    handleError(error) {

        console.error(
            "KD-HDIE:",
            error
        );

    }

}


/*=====================================================================
Start KD-HDIE Framework
======================================================================*/

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const explorer =
            new InteroperabilityExplorer();

        explorer.initialize();

        window.kdhdieExplorer =
            explorer;

    }
);
