// ==UserScript==
// @name         Github Burgr Button
// @namespace    https://burgr.sonarsource.com/
// @version      0.1
// @description  Add a "Show in Burgr" button to SonarSource Github repositories
// @author       jeanbaptiste.lievremont@sonarsource.com
// @match        https://github.com/SonarSource/*
// @grant        none
// ==/UserScript==

/*
 * This userscript is meant to be used with e.g Tampermonkey http://tampermonkey.net/
 */

(function() {
  'use strict';

  var headerNode = document.querySelector('.repohead-details-container h1');
  var projectName = /https:\/\/github\.com\/SonarSource\/([^/]+)/.exec(window.location.href)[1];
  var burgrLink = document.createElement('a');
  burgrLink.href = "https://burgr.sonarsource.com/project/SonarSource/" + projectName;
  burgrLink.target = "_blank";
  burgrLink.rel = "noopener noreferer";
  burgrLink.title = "Show in Burgr";
  burgrLink.innerHTML = "🍔";
  headerNode.insertBefore(burgrLink, headerNode.childNodes[1]);
})();
