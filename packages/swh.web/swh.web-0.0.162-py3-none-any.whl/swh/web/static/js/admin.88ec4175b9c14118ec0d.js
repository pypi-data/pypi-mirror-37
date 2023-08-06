(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else if(typeof exports === 'object')
		exports["admin"] = factory();
	else
		root["swh"] = root["swh"] || {}, root["swh"]["admin"] = factory();
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/static/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/@babel/runtime-corejs2/core-js/json/stringify.js":
/*!***********************************************************************!*\
  !*** ./node_modules/@babel/runtime-corejs2/core-js/json/stringify.js ***!
  \***********************************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! core-js/library/fn/json/stringify */ "./node_modules/core-js/library/fn/json/stringify.js");

/***/ }),

/***/ "./node_modules/core-js/library/fn/json/stringify.js":
/*!***********************************************************!*\
  !*** ./node_modules/core-js/library/fn/json/stringify.js ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var core = __webpack_require__(/*! ../../modules/_core */ "./node_modules/core-js/library/modules/_core.js");
var $JSON = core.JSON || (core.JSON = { stringify: JSON.stringify });
module.exports = function stringify(it) { // eslint-disable-line no-unused-vars
  return $JSON.stringify.apply($JSON, arguments);
};


/***/ }),

/***/ "./node_modules/core-js/library/modules/_core.js":
/*!*******************************************************!*\
  !*** ./node_modules/core-js/library/modules/_core.js ***!
  \*******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

var core = module.exports = { version: '2.5.7' };
if (typeof __e == 'number') __e = core; // eslint-disable-line no-undef


/***/ }),

/***/ "./swh/web/assets/src/bundles/admin/deposit.js":
/*!*****************************************************!*\
  !*** ./swh/web/assets/src/bundles/admin/deposit.js ***!
  \*****************************************************/
/*! exports provided: initDepositAdmin */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initDepositAdmin", function() { return initDepositAdmin; });
/* harmony import */ var _babel_runtime_corejs2_core_js_json_stringify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime-corejs2/core-js/json/stringify */ "./node_modules/@babel/runtime-corejs2/core-js/json/stringify.js");
/* harmony import */ var _babel_runtime_corejs2_core_js_json_stringify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_babel_runtime_corejs2_core_js_json_stringify__WEBPACK_IMPORTED_MODULE_0__);

function initDepositAdmin() {
  var depositsTable;
  $(document).ready(function () {
    $.fn.dataTable.ext.errMode = 'none';
    depositsTable = $('#swh-admin-deposit-list').on('error.dt', function (e, settings, techNote, message) {
      $('#swh-admin-deposit-list-error').text(message);
    }).DataTable({
      serverSide: true,
      ajax: Urls.admin_deposit_list(),
      columns: [{
        data: 'id',
        name: 'id'
      }, {
        data: 'external_id',
        name: 'external_id',
        render: function render(data, type, row) {
          if (type === 'display') {
            if (data && data.startsWith('hal')) {
              return "<a href=\"https://hal.archives-ouvertes.fr/" + data + "\">" + data + "</a>";
            }
          }

          return data;
        }
      }, {
        data: 'reception_date',
        name: 'reception_date',
        render: function render(data, type, row) {
          if (type === 'display') {
            var date = new Date(data);
            return date.toLocaleString();
          }

          return data;
        }
      }, {
        data: 'status',
        name: 'status'
      }, {
        data: 'status_detail',
        name: 'status_detail',
        render: function render(data, type, row) {
          if (type === 'display' && data) {
            var text = data;

            if (typeof data === 'object') {
              text = _babel_runtime_corejs2_core_js_json_stringify__WEBPACK_IMPORTED_MODULE_0___default()(data, null, 4);
            }

            return "<div style=\"width: 200px; white-space: pre; overflow-x: auto;\">" + text + "</div>";
          }

          return data;
        },
        orderable: false
      }, {
        data: 'swh_id',
        name: 'swh_id',
        render: function render(data, type, row) {
          if (type === 'display') {
            if (data && data.startsWith('swh')) {
              var browseUrl = Urls.browse_swh_id(data);
              return "<a href=\"" + browseUrl + "\">" + data + "</a>";
            }
          }

          return data;
        }
      }],
      scrollY: '50vh',
      scrollCollapse: true,
      order: [[0, 'desc']]
    });
    depositsTable.draw();
  });
}

/***/ }),

/***/ "./swh/web/assets/src/bundles/admin/index.js":
/*!***************************************************!*\
  !*** ./swh/web/assets/src/bundles/admin/index.js ***!
  \***************************************************/
/*! exports provided: initDepositAdmin, initOriginSaveAdmin, addAuthorizedOriginUrl, removeAuthorizedOriginUrl, addUnauthorizedOriginUrl, removeUnauthorizedOriginUrl, acceptOriginSaveRequest, rejectOriginSaveRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _deposit__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./deposit */ "./swh/web/assets/src/bundles/admin/deposit.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "initDepositAdmin", function() { return _deposit__WEBPACK_IMPORTED_MODULE_0__["initDepositAdmin"]; });

/* harmony import */ var _origin_save__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./origin-save */ "./swh/web/assets/src/bundles/admin/origin-save.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "initOriginSaveAdmin", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["initOriginSaveAdmin"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "addAuthorizedOriginUrl", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["addAuthorizedOriginUrl"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "removeAuthorizedOriginUrl", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["removeAuthorizedOriginUrl"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "addUnauthorizedOriginUrl", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["addUnauthorizedOriginUrl"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "removeUnauthorizedOriginUrl", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["removeUnauthorizedOriginUrl"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "acceptOriginSaveRequest", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["acceptOriginSaveRequest"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "rejectOriginSaveRequest", function() { return _origin_save__WEBPACK_IMPORTED_MODULE_1__["rejectOriginSaveRequest"]; });

/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */



/***/ }),

/***/ "./swh/web/assets/src/bundles/admin/origin-save.js":
/*!*********************************************************!*\
  !*** ./swh/web/assets/src/bundles/admin/origin-save.js ***!
  \*********************************************************/
/*! exports provided: initOriginSaveAdmin, addAuthorizedOriginUrl, removeAuthorizedOriginUrl, addUnauthorizedOriginUrl, removeUnauthorizedOriginUrl, acceptOriginSaveRequest, rejectOriginSaveRequest */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initOriginSaveAdmin", function() { return initOriginSaveAdmin; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "addAuthorizedOriginUrl", function() { return addAuthorizedOriginUrl; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "removeAuthorizedOriginUrl", function() { return removeAuthorizedOriginUrl; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "addUnauthorizedOriginUrl", function() { return addUnauthorizedOriginUrl; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "removeUnauthorizedOriginUrl", function() { return removeUnauthorizedOriginUrl; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "acceptOriginSaveRequest", function() { return acceptOriginSaveRequest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "rejectOriginSaveRequest", function() { return rejectOriginSaveRequest; });
/* harmony import */ var utils_functions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! utils/functions */ "./swh/web/assets/src/utils/functions.js");
/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */

var authorizedOriginTable;
var unauthorizedOriginTable;
var pendingSaveRequestsTable;
var acceptedSaveRequestsTable;
var rejectedSaveRequestsTable;

function enableRowSelection(tableSel) {
  $(tableSel + " tbody").on('click', 'tr', function () {
    if ($(this).hasClass('selected')) {
      $(this).removeClass('selected');
    } else {
      $(tableSel + " tr.selected").removeClass('selected');
      $(this).addClass('selected');
    }
  });
}

function initOriginSaveAdmin() {
  $(document).ready(function () {
    authorizedOriginTable = $('#swh-authorized-origin-urls').DataTable({
      serverSide: true,
      ajax: Urls.admin_origin_save_authorized_urls_list(),
      columns: [{
        data: 'url',
        name: 'url'
      }],
      scrollY: '50vh',
      scrollCollapse: true,
      info: false
    });
    enableRowSelection('#swh-authorized-origin-urls');
    unauthorizedOriginTable = $('#swh-unauthorized-origin-urls').DataTable({
      serverSide: true,
      ajax: Urls.admin_origin_save_unauthorized_urls_list(),
      columns: [{
        data: 'url',
        name: 'url'
      }],
      scrollY: '50vh',
      scrollCollapse: true,
      info: false
    });
    enableRowSelection('#swh-unauthorized-origin-urls');
    var columnsData = [{
      data: 'save_request_date',
      name: 'request_date',
      render: function render(data, type, row) {
        if (type === 'display') {
          var date = new Date(data);
          return date.toLocaleString();
        }

        return data;
      }
    }, {
      data: 'origin_type',
      name: 'origin_type'
    }, {
      data: 'origin_url',
      name: 'origin_url',
      render: function render(data, type, row) {
        if (type === 'display') {
          return "<a href=\"" + data + "\">" + data + "</a>";
        }

        return data;
      }
    }];
    pendingSaveRequestsTable = $('#swh-origin-save-pending-requests').DataTable({
      serverSide: true,
      ajax: Urls.browse_origin_save_requests_list('pending'),
      columns: columnsData,
      scrollY: '50vh',
      scrollCollapse: true,
      order: [[0, 'desc']]
    });
    enableRowSelection('#swh-origin-save-pending-requests');
    rejectedSaveRequestsTable = $('#swh-origin-save-rejected-requests').DataTable({
      serverSide: true,
      ajax: Urls.browse_origin_save_requests_list('rejected'),
      columns: columnsData,
      scrollY: '50vh',
      scrollCollapse: true,
      order: [[0, 'desc']]
    });
    columnsData.push({
      data: 'save_task_status',
      name: 'save_task_status',
      render: function render(data, type, row) {
        if (data === 'succeed') {
          var browseOriginUrl = Urls.browse_origin(row.origin_url);
          return "<a href=\"" + browseOriginUrl + "\">" + data + "</a>";
        }

        return data;
      }
    });
    acceptedSaveRequestsTable = $('#swh-origin-save-accepted-requests').DataTable({
      serverSide: true,
      ajax: Urls.browse_origin_save_requests_list('accepted'),
      columns: columnsData,
      scrollY: '50vh',
      scrollCollapse: true,
      order: [[0, 'desc']]
    });
    $('#swh-origin-save-requests-nav-item').on('shown.bs.tab', function () {
      pendingSaveRequestsTable.draw();
    });
    $('#swh-origin-save-url-filters-nav-item').on('shown.bs.tab', function () {
      authorizedOriginTable.draw();
    });
    $('#swh-authorized-origins-tab').on('shown.bs.tab', function () {
      authorizedOriginTable.draw();
    });
    $('#swh-unauthorized-origins-tab').on('shown.bs.tab', function () {
      unauthorizedOriginTable.draw();
    });
    $('#swh-save-requests-pending-tab').on('shown.bs.tab', function () {
      pendingSaveRequestsTable.draw();
    });
    $('#swh-save-requests-accepted-tab').on('shown.bs.tab', function () {
      acceptedSaveRequestsTable.draw();
    });
    $('#swh-save-requests-rejected-tab').on('shown.bs.tab', function () {
      rejectedSaveRequestsTable.draw();
    });
    $('#swh-save-requests-pending-tab').click(function () {
      pendingSaveRequestsTable.ajax.reload(null, false);
    });
    $('#swh-save-requests-accepted-tab').click(function () {
      acceptedSaveRequestsTable.ajax.reload(null, false);
    });
    $('#swh-save-requests-rejected-tab').click(function () {
      rejectedSaveRequestsTable.ajax.reload(null, false);
    });
  });
}
function addAuthorizedOriginUrl() {
  var originUrl = $('#swh-authorized-url-prefix').val();
  var addOriginUrl = Urls.admin_origin_save_add_authorized_url(originUrl);
  Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(addOriginUrl).then(utils_functions__WEBPACK_IMPORTED_MODULE_0__["handleFetchError"]).then(function () {
    authorizedOriginTable.row.add({
      'url': originUrl
    }).draw();
  }).catch(function (response) {
    swh.webapp.showModalMessage('Duplicated origin url prefix', 'The provided origin url prefix is already registered in the authorized list.');
  });
}
function removeAuthorizedOriginUrl() {
  var originUrl = $('#swh-authorized-origin-urls tr.selected').text();

  if (originUrl) {
    var removeOriginUrl = Urls.admin_origin_save_remove_authorized_url(originUrl);
    Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(removeOriginUrl).then(utils_functions__WEBPACK_IMPORTED_MODULE_0__["handleFetchError"]).then(function () {
      authorizedOriginTable.row('.selected').remove().draw();
    }).catch(function () {});
  }
}
function addUnauthorizedOriginUrl() {
  var originUrl = $('#swh-unauthorized-url-prefix').val();
  var addOriginUrl = Urls.admin_origin_save_add_unauthorized_url(originUrl);
  Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(addOriginUrl).then(utils_functions__WEBPACK_IMPORTED_MODULE_0__["handleFetchError"]).then(function () {
    unauthorizedOriginTable.row.add({
      'url': originUrl
    }).draw();
  }).catch(function () {
    swh.webapp.showModalMessage('Duplicated origin url prefix', 'The provided origin url prefix is already registered in the unauthorized list.');
  });
}
function removeUnauthorizedOriginUrl() {
  var originUrl = $('#swh-unauthorized-origin-urls tr.selected').text();

  if (originUrl) {
    var removeOriginUrl = Urls.admin_origin_save_remove_unauthorized_url(originUrl);
    Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(removeOriginUrl).then(utils_functions__WEBPACK_IMPORTED_MODULE_0__["handleFetchError"]).then(function () {
      unauthorizedOriginTable.row('.selected').remove().draw();
    }).catch(function () {});
  }
}
function acceptOriginSaveRequest() {
  var selectedRow = pendingSaveRequestsTable.row('.selected');

  if (selectedRow.length) {
    var acceptOriginSaveRequestCallback = function acceptOriginSaveRequestCallback() {
      var rowData = selectedRow.data();
      var acceptSaveRequestUrl = Urls.admin_origin_save_request_accept(rowData['origin_type'], rowData['origin_url']);
      Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(acceptSaveRequestUrl).then(function () {
        pendingSaveRequestsTable.ajax.reload(null, false);
      });
    };

    swh.webapp.showModalConfirm('Accept origin save request ?', 'Are you sure to accept this origin save request ?', acceptOriginSaveRequestCallback);
  }
}
function rejectOriginSaveRequest() {
  var selectedRow = pendingSaveRequestsTable.row('.selected');

  if (selectedRow.length) {
    var rejectOriginSaveRequestCallback = function rejectOriginSaveRequestCallback() {
      var rowData = selectedRow.data();
      var rejectSaveRequestUrl = Urls.admin_origin_save_request_reject(rowData['origin_type'], rowData['origin_url']);
      Object(utils_functions__WEBPACK_IMPORTED_MODULE_0__["csrfPost"])(rejectSaveRequestUrl).then(function () {
        pendingSaveRequestsTable.ajax.reload(null, false);
      });
    };

    swh.webapp.showModalConfirm('Reject origin save request ?', 'Are you sure to reject this origin save request ?', rejectOriginSaveRequestCallback);
  }
}

/***/ }),

/***/ "./swh/web/assets/src/utils/functions.js":
/*!***********************************************!*\
  !*** ./swh/web/assets/src/utils/functions.js ***!
  \***********************************************/
/*! exports provided: handleFetchError, handleFetchErrors, staticAsset, csrfPost, isGitRepoUrl */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "handleFetchError", function() { return handleFetchError; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "handleFetchErrors", function() { return handleFetchErrors; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "staticAsset", function() { return staticAsset; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "csrfPost", function() { return csrfPost; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isGitRepoUrl", function() { return isGitRepoUrl; });
/**
 * Copyright (C) 2018  The Software Heritage developers
 * See the AUTHORS file at the top-level directory of this distribution
 * License: GNU Affero General Public License version 3, or any later version
 * See top-level LICENSE file for more information
 */
// utility functions
function handleFetchError(response) {
  if (!response.ok) {
    throw response;
  }

  return response;
}
function handleFetchErrors(responses) {
  for (var i = 0; i < responses.length; ++i) {
    if (!responses[i].ok) {
      throw responses[i];
    }
  }

  return responses;
}
function staticAsset(asset) {
  return "" + "/static/" + asset;
}
function csrfPost(url, headers, body) {
  if (headers === void 0) {
    headers = {};
  }

  if (body === void 0) {
    body = null;
  }

  headers['X-CSRFToken'] = Cookies.get('csrftoken');
  return fetch(url, {
    credentials: 'include',
    headers: headers,
    method: 'POST',
    body: body
  });
}
function isGitRepoUrl(url, domain) {
  var endOfPattern = '\\/[\\w\\.-]+\\/?(?!=.git)(?:\\.git(?:\\/?|\\#[\\w\\.\\-_]+)?)?$';
  var pattern = "(?:git|https?|git@)(?:\\:\\/\\/)?" + domain + "[/|:][A-Za-z0-9-]+?" + endOfPattern;
  var re = new RegExp(pattern);
  return re.test(url);
}
;

/***/ }),

/***/ 0:
/*!************************************!*\
  !*** multi bundles/admin/index.js ***!
  \************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! bundles/admin/index.js */"./swh/web/assets/src/bundles/admin/index.js");


/***/ })

/******/ });
});
//# admin.88ec4175b9c14118ec0d.js.map