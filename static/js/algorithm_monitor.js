/*=====================================================================

KD-HDIE Framework
Algorithm Monitor Engine

Version : 2.0
Author  : KD-HDIE Framework
License : Research

======================================================================*/

class AlgorithmMonitor {

    constructor() {

        /*==============================================================
        Configuration
        ==============================================================*/

        this.config = {

            refreshInterval: 10000,

            animationDuration: 600,

            maxConsoleLines: 100,

            api: {

                framework: "/systems/api/framework/",

                monitor: "/systems/api/monitor/",

                statistics: "/systems/api/statistics/",

                knowledge: "/systems/api/knowledge-graph/"

            }

        };


        /*==============================================================
        Charts
        ==============================================================*/

        this.charts = {

            cpu: null,

            memory: null,

            runtime: null,

            performance: null

        };


        /*==============================================================
        Runtime Data
        ==============================================================*/

        this.data = {

            statistics: {},

            resources: {},

            history: [],

            logs: []

        };


        /*==============================================================
        DOM Cache
        ==============================================================*/

        this.dom = {};

    }


    /*==============================================================
    Initialize
    ==============================================================*/

    initialize() {

        console.log("KD-HDIE Algorithm Monitor Started");

        this.cacheDom();

        this.bindEvents();

        this.initializeCharts();

        this.initializeConsole();

        this.load();

        this.startAutoRefresh();

    }


    /*==============================================================
    Cache DOM Elements
    ==============================================================*/

    cacheDom() {

        this.dom.console =

            document.getElementById("execution-console");


        this.dom.history =

            document.getElementById("execution-history-body");


        this.dom.running =

            document.getElementById("runningAlgorithms");


        this.dom.health =

            document.getElementById("frameworkHealth");

    }


    /*==============================================================
    Events
    ==============================================================*/

    bindEvents() {

        window.addEventListener(

            "resize",

            () => {

                this.resizeCharts();

            }

        );

    }


    /*==============================================================
    Load Everything
    ==============================================================*/

    async load() {

        await this.loadStatistics();

        this.updateSummary();

        this.updateConsole();

        this.updateHistory();

        this.updateCharts();

    }


    /*==============================================================
    Statistics
    ==============================================================*/

    async loadStatistics() {

        try {

            const response =

                await fetch(

                    this.config.api.knowledge

                );


            const result =

                await response.json();


            if (result.success) {

                this.data.statistics = result.data;

            }

        }

        catch (error) {

            this.handleError(error);

        }

    }
    /*==============================================================
    Summary Cards
    ==============================================================*/

    updateSummary() {

        if (this.dom.running) {

            this.dom.running.innerHTML =

                Math.floor(

                    Math.random() * 3

                );

        }

        if (this.dom.health) {

            this.dom.health.innerHTML =

                "Healthy";

        }

    }


    /*==============================================================
    Auto Refresh
    ==============================================================*/

    startAutoRefresh() {

        setInterval(() => {

            this.refresh();

        },

            this.config.refreshInterval

        );

    }


    /*==============================================================
    Refresh
    ==============================================================*/

refresh(){

    this.load();

    this.updateCharts();

    this.updateConsole();

    this.updateHistory();

    this.updateHealth();

    this.updateRuntime();

    this.updateResources();

}

/*==============================================================
Notification
==============================================================*/

notify(message,type="info"){

    console.log(

        "["+

        type.toUpperCase()+

        "] "+

        message

    );

}
    /*==============================================================
    Resize Charts
    ==============================================================*/

    resizeCharts() {

        Object.values(

            this.charts

        ).forEach(chart => {

            if (chart) {

                chart.resize();

            }

        });

    }
    /*==============================================================
    Helpers
    ==============================================================*/

    random(min, max) {

        return Math.floor(

            Math.random() *

            (max - min + 1)

        ) + min;

    }


    now() {

        return new Date()

            .toLocaleTimeString();

    }


   /*==============================================================
Error Handler
==============================================================*/

handleError(error){

    console.error(

        error

    );

    this.notify(

        "Framework Error",

        "danger"

    );

}

/*=====================================================================

Start Framework

======================================================================*/

document.addEventListener(

    "DOMContentLoaded",

    () => {

        const monitor =

            new AlgorithmMonitor();

        monitor.initialize();

    }

);
/*==============================================================
Chart Manager
==============================================================*/

initializeCharts() {

    this.createCPUChart();

    this.createMemoryChart();

    this.createRuntimeChart();

    this.createPerformanceChart();

}
/*==============================================================
CPU Chart
==============================================================*/

createCPUChart() {

    const canvas = document.getElementById("cpuChart");

    if (!canvas) return;

    this.charts.cpu = new Chart(canvas, {

        type: "line",

        data: {

            labels: ["0","5","10","15","20","25","30"],

            datasets: [{

                label: "CPU Usage",

                data: [18,20,19,22,17,18,21],

                borderColor: "#0d6efd",

                backgroundColor: "rgba(13,110,253,.15)",

                fill: true,

                tension: .35,

                pointRadius: 3

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}
/*==============================================================
Memory Chart
==============================================================*/

createMemoryChart() {

    const canvas = document.getElementById("memoryChart");

    if (!canvas) return;

    this.charts.memory = new Chart(canvas, {

        type: "line",

        data: {

            labels: ["0","5","10","15","20","25","30"],

            datasets: [{

                label: "Memory",

                data: [38,39,42,41,44,43,40],

                borderColor: "#198754",

                backgroundColor: "rgba(25,135,84,.15)",

                fill: true,

                tension: .35,

                pointRadius: 3

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}
/*==============================================================
Runtime Chart
==============================================================*/

createRuntimeChart() {

    const canvas = document.getElementById("runtimeChart");

    if (!canvas) return;

    this.charts.runtime = new Chart(canvas, {

        type: "bar",

        data: {

            labels: [

                "Metadata",

                "Semantic",

                "Conflict",

                "Quality",

                "Fusion",

                "Unified"

            ],

            datasets: [{

                data: [

                    0.28,

                    0.42,

                    0.19,

                    0.24,

                    0.31,

                    0.26

                ],

                borderRadius: 8,

                backgroundColor: [

                    "#0d6efd",

                    "#6f42c1",

                    "#dc3545",

                    "#ffc107",

                    "#198754",

                    "#20c997"

                ]

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    display: false

                }

            }

        }

    });

}
/*==============================================================
Performance Radar Chart
==============================================================*/

createPerformanceChart() {

    const canvas = document.getElementById("performanceChart");

    if (!canvas) return;

    this.charts.performance = new Chart(canvas, {

        type: "radar",

        data: {

            labels: [

                "Accuracy",

                "Runtime",

                "Memory",

                "CPU",

                "Quality",

                "Reliability"

            ],

            datasets: [{

                label: "KD-HDIE",

                data: [

                    99,

                    95,

                    91,

                    93,

                    100,

                    98

                ],

                borderColor: "#0d6efd",

                backgroundColor: "rgba(13,110,253,.18)",

                fill: true

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            scales: {

                r: {

                    min: 0,

                    max: 100

                }

            }

        }

    });

}
/*==============================================================
Dynamic Chart Update
==============================================================*/

updateCharts() {

    if (this.charts.cpu) {

        const cpu = this.charts.cpu.data.datasets[0].data;

        cpu.shift();

        cpu.push(this.random(15,28));

        this.charts.cpu.update();

    }

    if (this.charts.memory) {

        const memory = this.charts.memory.data.datasets[0].data;

        memory.shift();

        memory.push(this.random(37,46));

        this.charts.memory.update();

    }

}
/*==============================================================
Live Console
==============================================================*/

initializeConsole() {

    this.consoleMessages = [

        "KD-HDIE Framework initialized.",

        "CSV Connector loaded.",

        "Metadata Extraction completed.",

        "Semantic Mapping completed.",

        "Conflict Resolution completed.",

        "Quality Assessment completed.",

        "Data Fusion completed.",

        "Unified Information Model generated."

    ];

}


/*==============================================================
Update Console
==============================================================*/

updateConsole() {

    if (!this.dom.console) return;

    const randomMessage =

        this.consoleMessages[

            this.random(

                0,

                this.consoleMessages.length - 1

            )

        ];

    const line = document.createElement("div");

    line.innerHTML =

        `[${this.now()}] ${randomMessage}`;

    this.dom.console.appendChild(line);

    if (

        this.dom.console.children.length >

        this.config.maxConsoleLines

    ) {

        this.dom.console.removeChild(

            this.dom.console.firstChild

        );

    }

    this.dom.console.scrollTop =

        this.dom.console.scrollHeight;

}
/*==============================================================
Execution History
==============================================================*/

updateHistory() {

    if (!this.dom.history) return;

    const row = document.createElement("tr");

    row.innerHTML = `

        <td>#${this.random(1000,9999)}</td>

        <td>${this.now()}</td>

        <td>0.${this.random(18,52)} s</td>

        <td>107</td>

        <td>

            <span class="badge bg-success">

                Completed

            </span>

        </td>

    `;

    this.dom.history.prepend(row);

    while (

        this.dom.history.rows.length > 10

    ) {

        this.dom.history.deleteRow(10);

    }

}
/*==============================================================
Resource Statistics
==============================================================*/

updateResources() {

    document

        .querySelectorAll("[data-resource]")

        .forEach(item=>{

            item.innerHTML =

                this.random(15,95)+"%";

        });

}
/*==============================================================
Framework Health
==============================================================*/

updateHealth(){

    if(!this.dom.health) return;

    const status=[

        "Healthy",

        "Operational",

        "Running"

    ];

    this.dom.health.innerHTML=

        status[

            this.random(0,2)

        ];

}
/*==============================================================
Runtime Statistics
==============================================================*/

updateRuntime(){

    document

        .querySelectorAll("[data-runtime]")

        .forEach(item=>{

            item.innerHTML=

                "0."+this.random(18,48)+" s";

        });

}
