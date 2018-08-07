// ==UserScript==
// @name         Github Burgr Button
// @namespace    https://burgr.sonarsource.com/
// @version      0.2
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

  const projectExp = /https:\/\/github\.com\/SonarSource\/([^/]+)/;
  const branchExp = /\/tree\/([\w\/]+)/;
  const prExp = /\/pull\/(\d+)/;

  const location = window.location.href;
  const projectName = projectExp.exec(location)[1];
  const branchName = branchExp.test(location) ? branchExp.exec(location)[1] : null;
  const prNumber = prExp.test(location) ? prExp.exec(location)[1] : null;

  const headerNode = document.querySelector('.repohead-details-container h1');
  const burgrLink = document.createElement('a');
  burgrLink.href = 'https://burgr.sonarsource.com/projects/SonarSource/' + projectName;
  if (branchName) {
    burgrLink.href += ('/branches/' + branchName);
  } else if (prNumber) {
    burgrLink.href += ('/pullrequests/' + prNumber);
  }
  burgrLink.target = '_blank';
  burgrLink.rel = 'noopener noreferer';
  burgrLink.title = 'Show in Burgr';
  burgrLink.innerHTML = '🍔';
  headerNode.insertBefore(burgrLink, headerNode.childNodes[1]);
})();
