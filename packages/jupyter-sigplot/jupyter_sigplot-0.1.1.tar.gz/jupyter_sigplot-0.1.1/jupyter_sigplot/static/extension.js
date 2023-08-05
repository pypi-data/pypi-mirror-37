define(function() { return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

	// This file contains the javascript that is run when the notebook is loaded.
	// It contains some requirejs configuration and the `load_ipython_extension`
	// which is required for any notebook extension.
	//
	// Some static assets may be required by the custom widget javascript. The base
	// url for the notebook is not known at build time and is therefore computed
	// dynamically.
	__webpack_require__.p = document.querySelector('body').getAttribute('data-base-url') + 'nbextensions/jupyter_sigplot';


	// Configure requirejs
	if (window.require) {
	    window.require.config({
	        map: {
	            "*" : {
	                "jupyter_sigplot": "nbextensions/jupyter_sigplot/index",
	                "jupyter-js-widgets": "nbextensions/jupyter-js-widgets/extension",

	            }
	        }
	    });
	}

	// Export the required load_ipython_extension
	module.exports = {
	    load_ipython_extension: function() {}
	};


/***/ })
/******/ ])});;