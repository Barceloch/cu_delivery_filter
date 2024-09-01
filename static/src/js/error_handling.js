odoo.define('cu_delivery_filter.error_handling', [], function (require) {
    'use strict';

    console.log("(BarSoft) - error_handling.js cargado correctamente");

    // Manejo global de promesas no gestionadas
    window.addEventListener('unhandledrejection', function (event) {
        //event.preventDefault();
        console.error('(BarSoft) - Uncaught Promise Rejection:', event.reason);
    });


});
