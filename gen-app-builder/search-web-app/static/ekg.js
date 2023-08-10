/**
 * Copyright 2023 Google LLC
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

hljs.highlightAll();

mdc.autoInit();

const MDCRipple = mdc.ripple.MDCRipple;
const MDCTextField = mdc.textField.MDCTextField;
const MDCSelect = mdc.select.MDCSelect;
const MDCTabBar = mdc.tabBar.MDCTabBar;
const MDCChipSet = mdc.chips.MDCChipSet;
const MDCChip = mdc.chips.MDCChip;

MDCRipple.attachTo(document.querySelector(".search-button"));

const queryTextField = new MDCTextField(document.querySelector(".query-field"));
const typesTextField = new MDCTextField(document.querySelector(".mdc-text-field.types-field"));

const select = new MDCSelect(document.querySelector(".mdc-select"));
const tabBar = new MDCTabBar(document.querySelector(".mdc-tab-bar"));

const chipset = new MDCChipSet(document.querySelector(".mdc-chip-set"));
const chip = new MDCChipSet(document.querySelector(".mdc-chip"));

const jsonTabSelector = document.querySelector("#json-tab-selector");
const entitiesTabSelector = document.querySelector("#entities-tab-selector");

const tabContent = document.querySelector(".tab-content");
const jsonTab = document.querySelector("#json-tab");
const entitiesTab = document.querySelector("#entities-tab");

jsonTabSelector.onclick = () => {
  jsonTab.classList.replace("tab-hidden", "tab-visible");
  entitiesTab.classList.replace("tab-visible", "tab-hidden");
  entitiesTab.replaceWith(jsonTab);
};

entitiesTabSelector.onclick = () => {
  entitiesTab.classList.replace("tab-hidden", "tab-visible");
  jsonTab.classList.replace("tab-visible", "tab-hidden");
  jsonTab.replaceWith(entitiesTab);
};

/*
function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

// Start file download.
document.getElementById("dwn-btn").addEventListener("click", function () {
    // Generate download of hello.txt file with some content
    var text = document.getElementById("text-val").value;
    var filename = "hello.txt";

    download(filename, text);
}, false);
*/
