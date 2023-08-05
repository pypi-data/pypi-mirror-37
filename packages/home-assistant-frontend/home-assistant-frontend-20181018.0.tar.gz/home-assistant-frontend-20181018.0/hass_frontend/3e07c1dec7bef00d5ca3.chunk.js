(window.webpackJsonp=window.webpackJsonp||[]).push([[67],{237:function(module,__webpack_exports__,__webpack_require__){"use strict";var _Mathmax=Math.max,_polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(3),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(1),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_1__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_3__.a`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var parentNode=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(this).parentNode,ownerRoot=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(this).getOwnerRoot(),target;if(this.for){target=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(ownerRoot).querySelector("#"+this.for)}else{target=parentNode.nodeType==Node.DOCUMENT_FRAGMENT_NODE?ownerRoot.host:parentNode}return target},attached:function(){this._findTarget()},detached:function(){if(!this.manualMode)this._removeListeners()},playAnimation:function(type){if("entry"===type){this.show()}else if("exit"===type){this.hide()}},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(this._showing)return;if(""===Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(this).textContent.trim()){for(var allChildrenEmpty=!0,effectiveChildren=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(this).getEffectiveChildNodes(),i=0;i<effectiveChildren.length;i++){if(""!==effectiveChildren[i].textContent.trim()){allChildrenEmpty=!1;break}}if(allChildrenEmpty){return}}this._showing=!0;this.$.tooltip.classList.remove("hidden");this.$.tooltip.classList.remove("cancel-animation");this.$.tooltip.classList.remove(this._getAnimationType("exit"));this.updatePosition();this._animationPlaying=!0;this.$.tooltip.classList.add(this._getAnimationType("entry"))},hide:function(){if(!this._showing){return}if(this._animationPlaying){this._showing=!1;this._cancelAnimation();return}else{this._onAnimationFinish()}this._showing=!1;this._animationPlaying=!0},updatePosition:function(){if(!this._target||!this.offsetParent)return;var offset=this.offset;if(14!=this.marginTop&&14==this.offset)offset=this.marginTop;var parentRect=this.offsetParent.getBoundingClientRect(),targetRect=this._target.getBoundingClientRect(),thisRect=this.getBoundingClientRect(),horizontalCenterOffset=(targetRect.width-thisRect.width)/2,verticalCenterOffset=(targetRect.height-thisRect.height)/2,targetLeft=targetRect.left-parentRect.left,targetTop=targetRect.top-parentRect.top,tooltipLeft,tooltipTop;switch(this.position){case"top":tooltipLeft=targetLeft+horizontalCenterOffset;tooltipTop=targetTop-thisRect.height-offset;break;case"bottom":tooltipLeft=targetLeft+horizontalCenterOffset;tooltipTop=targetTop+targetRect.height+offset;break;case"left":tooltipLeft=targetLeft-thisRect.width-offset;tooltipTop=targetTop+verticalCenterOffset;break;case"right":tooltipLeft=targetLeft+targetRect.width+offset;tooltipTop=targetTop+verticalCenterOffset;break;}if(this.fitToVisibleBounds){if(parentRect.left+tooltipLeft+thisRect.width>window.innerWidth){this.style.right="0px";this.style.left="auto"}else{this.style.left=_Mathmax(0,tooltipLeft)+"px";this.style.right="auto"}if(parentRect.top+tooltipTop+thisRect.height>window.innerHeight){this.style.bottom=parentRect.height-targetTop+offset+"px";this.style.top="auto"}else{this.style.top=_Mathmax(-parentRect.top,tooltipTop)+"px";this.style.bottom="auto"}}else{this.style.left=tooltipLeft+"px";this.style.top=tooltipTop+"px"}},_addListeners:function(){if(this._target){this.listen(this._target,"mouseenter","show");this.listen(this._target,"focus","show");this.listen(this._target,"mouseleave","hide");this.listen(this._target,"blur","hide");this.listen(this._target,"tap","hide")}this.listen(this.$.tooltip,"animationend","_onAnimationEnd");this.listen(this,"mouseenter","hide")},_findTarget:function(){if(!this.manualMode)this._removeListeners();this._target=this.target;if(!this.manualMode)this._addListeners()},_delayChange:function(newValue){if(500!==newValue){this.updateStyles({"--paper-tooltip-delay-in":newValue+"ms"})}},_manualModeChanged:function(){if(this.manualMode)this._removeListeners();else this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry"));this.$.tooltip.classList.remove(this._getAnimationType("exit"));this.$.tooltip.classList.remove("cancel-animation");this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){if(this._showing){this.$.tooltip.classList.remove(this._getAnimationType("entry"));this.$.tooltip.classList.remove("cancel-animation");this.$.tooltip.classList.add(this._getAnimationType("exit"))}},_onAnimationEnd:function(){this._animationPlaying=!1;if(!this._showing){this.$.tooltip.classList.remove(this._getAnimationType("exit"));this.$.tooltip.classList.add("hidden")}},_getAnimationType:function(type){if("entry"===type&&""!==this.animationEntry){return this.animationEntry}if("exit"===type&&""!==this.animationExit){return this.animationExit}if(this.animationConfig[type]&&"string"===typeof this.animationConfig[type][0].name){if(this.animationConfig[type][0].timing&&this.animationConfig[type][0].timing.delay&&0!==this.animationConfig[type][0].timing.delay){var timingDelay=this.animationConfig[type][0].timing.delay;if("entry"===type){this.updateStyles({"--paper-tooltip-delay-in":timingDelay+"ms"})}else if("exit"===type){this.updateStyles({"--paper-tooltip-delay-out":timingDelay+"ms"})}}return this.animationConfig[type][0].name}},_removeListeners:function(){if(this._target){this.unlisten(this._target,"mouseenter","show");this.unlisten(this._target,"focus","show");this.unlisten(this._target,"mouseleave","hide");this.unlisten(this._target,"blur","hide");this.unlisten(this._target,"tap","hide")}this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd");this.unlisten(this,"mouseenter","hide")}})},346:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return classMap});var _lit_html_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(215);/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */if(window.navigator.userAgent.match("Trident")){DOMTokenList.prototype.toggle=function(token,force){if(force===void 0||force){this.add(token)}else{this.remove(token)}return force===void 0?!0:force}}const classMapCache=new WeakMap,classMapStatics=new WeakMap,classMap=classInfo=>Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.f)(part=>{if(!(part instanceof _lit_html_js__WEBPACK_IMPORTED_MODULE_0__.a)||part instanceof _lit_html_js__WEBPACK_IMPORTED_MODULE_0__.c||"class"!==part.committer.name||1<part.committer.parts.length){throw new Error("The `classMap` directive must be used in the `class` attribute "+"and must be the only part in the attribute.")}if(!classMapStatics.has(part)){part.committer.element.className=part.committer.strings.join(" ");classMapStatics.set(part,!0)}const oldInfo=classMapCache.get(part);for(const name in oldInfo){if(!(name in classInfo)){part.committer.element.classList.remove(name)}}for(const name in classInfo){if(!oldInfo||oldInfo[name]!==classInfo[name]){part.committer.element.classList.toggle(name,!!classInfo[name])}}classMapCache.set(part,classInfo)})},454:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return styleMap});var _lit_html_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(215);/**
 * @license
 * Copyright (c) 2018 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const styleMapCache=new WeakMap,styleMapStatics=new WeakMap,styleMap=styleInfo=>Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.f)(part=>{if(!(part instanceof _lit_html_js__WEBPACK_IMPORTED_MODULE_0__.a)||part instanceof _lit_html_js__WEBPACK_IMPORTED_MODULE_0__.c||"style"!==part.committer.name||1<part.committer.parts.length){throw new Error("The `styleMap` directive must be used in the style attribute "+"and must be the only part in the attribute.")}if(!styleMapStatics.has(part)){part.committer.element.style.cssText=part.committer.strings.join(" ");styleMapStatics.set(part,!0)}const oldInfo=styleMapCache.get(part);for(const name in oldInfo){if(!(name in styleInfo)){part.committer.element.style[name]=null}}Object.assign(part.committer.element.style,styleInfo);styleMapCache.set(part,styleInfo)})},455:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return repeat});var _lit_html_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(215);/**
 * @license
 * Copyright (c) 2017 The Polymer Project Authors. All rights reserved.
 * This code may only be used under the BSD style license found at
 * http://polymer.github.io/LICENSE.txt
 * The complete set of authors may be found at
 * http://polymer.github.io/AUTHORS.txt
 * The complete set of contributors may be found at
 * http://polymer.github.io/CONTRIBUTORS.txt
 * Code distributed by Google as part of the polymer project is also
 * subject to an additional IP rights grant found at
 * http://polymer.github.io/PATENTS.txt
 */const createAndInsertPart=(containerPart,beforePart)=>{const container=containerPart.startNode.parentNode,beforeNode=beforePart===void 0?containerPart.endNode:beforePart.startNode,startNode=container.insertBefore(Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.e)(),beforeNode);container.insertBefore(Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.e)(),beforeNode);const newPart=new _lit_html_js__WEBPACK_IMPORTED_MODULE_0__.b(containerPart.options);newPart.insertAfterNode(startNode);return newPart},updatePart=(part,value)=>{part.setValue(value);part.commit();return part},insertPartBefore=(containerPart,part,ref)=>{const container=containerPart.startNode.parentNode,beforeNode=ref?ref.startNode:containerPart.endNode,endNode=part.endNode.nextSibling;if(endNode!==beforeNode){Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.j)(container,part.startNode,endNode,beforeNode)}},removePart=part=>{Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.i)(part.startNode.parentNode,part.startNode,part.endNode.nextSibling)},generateMap=(list,start,end)=>{const map=new Map;for(let i=start;i<=end;i++){map.set(list[i],i)}return map},partListCache=new WeakMap,keyListCache=new WeakMap;function repeat(items,keyFnOrTemplate,template){let keyFn;if(2===arguments.length){template=keyFnOrTemplate}else if(3===arguments.length){keyFn=keyFnOrTemplate}return Object(_lit_html_js__WEBPACK_IMPORTED_MODULE_0__.f)(containerPart=>{const oldParts=partListCache.get(containerPart)||[],oldKeys=keyListCache.get(containerPart)||[],newParts=[],newValues=[],newKeys=[];let index=0;for(const item of items){newKeys[index]=keyFn?keyFn(item,index):index;newValues[index]=template(item,index);index++}let newKeyToIndexMap,oldKeyToIndexMap,oldHead=0,oldTail=oldParts.length-1,newHead=0,newTail=newValues.length-1;while(oldHead<=oldTail&&newHead<=newTail){if(null===oldParts[oldHead]){oldHead++}else if(null===oldParts[oldTail]){oldTail--}else if(oldKeys[oldHead]===newKeys[newHead]){newParts[newHead]=updatePart(oldParts[oldHead],newValues[newHead]);oldHead++;newHead++}else if(oldKeys[oldTail]===newKeys[newTail]){newParts[newTail]=updatePart(oldParts[oldTail],newValues[newTail]);oldTail--;newTail--}else if(oldKeys[oldHead]===newKeys[newTail]){newParts[newTail]=updatePart(oldParts[oldHead],newValues[newTail]);insertPartBefore(containerPart,oldParts[oldHead],newParts[newTail+1]);oldHead++;newTail--}else if(oldKeys[oldTail]===newKeys[newHead]){newParts[newHead]=updatePart(oldParts[oldTail],newValues[newHead]);insertPartBefore(containerPart,oldParts[oldTail],oldParts[oldHead]);oldTail--;newHead++}else{if(newKeyToIndexMap===void 0){newKeyToIndexMap=generateMap(newKeys,newHead,newTail);oldKeyToIndexMap=generateMap(oldKeys,oldHead,oldTail)}if(!newKeyToIndexMap.has(oldKeys[oldHead])){removePart(oldParts[oldHead]);oldHead++}else if(!newKeyToIndexMap.has(oldKeys[oldTail])){removePart(oldParts[oldTail]);oldTail--}else{const oldIndex=oldKeyToIndexMap.get(newKeys[newHead]),oldPart=oldIndex!==void 0?oldParts[oldIndex]:null;if(null===oldPart){const newPart=createAndInsertPart(containerPart,oldParts[oldHead]);updatePart(newPart,newValues[newHead]);newParts[newHead]=newPart}else{newParts[newHead]=updatePart(oldPart,newValues[newHead]);insertPartBefore(containerPart,oldPart,oldParts[oldHead]);oldParts[oldIndex]=null}newHead++}}}while(newHead<=newTail){const newPart=createAndInsertPart(containerPart,newParts[newTail+1]);updatePart(newPart,newValues[newHead]);newParts[newHead++]=newPart}while(oldHead<=oldTail){const oldPart=oldParts[oldHead++];if(null!==oldPart){removePart(oldPart)}}partListCache.set(containerPart,newParts);keyListCache.set(containerPart,newKeys)})}},637:function(module,__webpack_exports__,__webpack_require__){"use strict";var lit_element=__webpack_require__(229),classMap=__webpack_require__(346),lit_html=__webpack_require__(215);/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */class MDCFoundation{static get cssClasses(){return{}}static get strings(){return{}}static get numbers(){return{}}static get defaultAdapter(){return{}}constructor(adapter={}){this.adapter_=adapter}init(){}destroy(){}}/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *//**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */const cssClasses={ROOT:"mdc-ripple-upgraded",UNBOUNDED:"mdc-ripple-upgraded--unbounded",BG_FOCUSED:"mdc-ripple-upgraded--background-focused",FG_ACTIVATION:"mdc-ripple-upgraded--foreground-activation",FG_DEACTIVATION:"mdc-ripple-upgraded--foreground-deactivation"},strings={VAR_LEFT:"--mdc-ripple-left",VAR_TOP:"--mdc-ripple-top",VAR_FG_SIZE:"--mdc-ripple-fg-size",VAR_FG_SCALE:"--mdc-ripple-fg-scale",VAR_FG_TRANSLATE_START:"--mdc-ripple-fg-translate-start",VAR_FG_TRANSLATE_END:"--mdc-ripple-fg-translate-end"},numbers={PADDING:10,INITIAL_ORIGIN_SCALE:.6,DEACTIVATION_TIMEOUT_MS:225,FG_DEACTIVATION_MS:150,TAP_DELAY_MS:300};/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */let supportsCssVariables_,supportsPassive_;function detectEdgePseudoVarBug(windowObj){const document=windowObj.document,node=document.createElement("div");node.className="mdc-ripple-surface--test-edge-var-bug";document.body.appendChild(node);const computedStyle=windowObj.getComputedStyle(node),hasPseudoVarBug=null!==computedStyle&&"solid"===computedStyle.borderTopStyle;node.remove();return hasPseudoVarBug}function supportsCssVariables(windowObj,forceRefresh=!1){let supportsCssVariables=supportsCssVariables_;if("boolean"===typeof supportsCssVariables_&&!forceRefresh){return supportsCssVariables}const supportsFunctionPresent=windowObj.CSS&&"function"===typeof windowObj.CSS.supports;if(!supportsFunctionPresent){return}const explicitlySupportsCssVars=windowObj.CSS.supports("--css-vars","yes"),weAreFeatureDetectingSafari10plus=windowObj.CSS.supports("(--css-vars: yes)")&&windowObj.CSS.supports("color","#00000000");if(explicitlySupportsCssVars||weAreFeatureDetectingSafari10plus){supportsCssVariables=!detectEdgePseudoVarBug(windowObj)}else{supportsCssVariables=!1}if(!forceRefresh){supportsCssVariables_=supportsCssVariables}return supportsCssVariables}function applyPassive(globalObj=window,forceRefresh=!1){if(supportsPassive_===void 0||forceRefresh){let isSupported=!1;try{globalObj.document.addEventListener("test",null,{get passive(){isSupported=!0;return isSupported}})}catch(e){}supportsPassive_=isSupported}return supportsPassive_?{passive:!0}:!1}function getMatchesProperty(HTMLElementPrototype){const matchesMethods=["matches","webkitMatchesSelector","msMatchesSelector"];let method="matches";for(let i=0;i<matchesMethods.length;i++){const matchesMethod=matchesMethods[i];if(matchesMethod in HTMLElementPrototype){method=matchesMethod;break}}return method}function getNormalizedEventCoords(ev,pageOffset,clientRect){const{x,y}=pageOffset,documentX=x+clientRect.left,documentY=y+clientRect.top;let normalizedX,normalizedY;if("touchstart"===ev.type){ev=ev;normalizedX=ev.changedTouches[0].pageX-documentX;normalizedY=ev.changedTouches[0].pageY-documentY}else{ev=ev;normalizedX=ev.pageX-documentX;normalizedY=ev.pageY-documentY}return{x:normalizedX,y:normalizedY}}/**
 * @license
 * Copyright 2016 Google Inc.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */const ACTIVATION_EVENT_TYPES=["touchstart","pointerdown","mousedown","keydown"],POINTER_DEACTIVATION_EVENT_TYPES=["touchend","pointerup","mouseup"];let activatedTargets=[];class foundation_MDCRippleFoundation extends MDCFoundation{static get cssClasses(){return cssClasses}static get strings(){return strings}static get numbers(){return numbers}static get defaultAdapter(){return{browserSupportsCssVars:()=>{},isUnbounded:()=>{},isSurfaceActive:()=>{},isSurfaceDisabled:()=>{},addClass:()=>{},removeClass:()=>{},containsEventTarget:()=>{},registerInteractionHandler:()=>{},deregisterInteractionHandler:()=>{},registerDocumentInteractionHandler:()=>{},deregisterDocumentInteractionHandler:()=>{},registerResizeHandler:()=>{},deregisterResizeHandler:()=>{},updateCssVariable:()=>{},computeBoundingRect:()=>{},getWindowPageOffset:()=>{}}}constructor(adapter){super(Object.assign(foundation_MDCRippleFoundation.defaultAdapter,adapter));this.layoutFrame_=0;this.frame_={width:0,height:0};this.activationState_=this.defaultActivationState_();this.initialSize_=0;this.maxRadius_=0;this.activateHandler_=e=>this.activate_(e);this.deactivateHandler_=()=>this.deactivate_();this.focusHandler_=()=>this.handleFocus();this.blurHandler_=()=>this.handleBlur();this.resizeHandler_=()=>this.layout();this.unboundedCoords_={left:0,top:0};this.fgScale_=0;this.activationTimer_=0;this.fgDeactivationRemovalTimer_=0;this.activationAnimationHasEnded_=!1;this.activationTimerCallback_=()=>{this.activationAnimationHasEnded_=!0;this.runDeactivationUXLogicIfReady_()};this.previousActivationEvent_}supportsPressRipple_(){return this.adapter_.browserSupportsCssVars()}defaultActivationState_(){return{isActivated:!1,hasDeactivationUXRun:!1,wasActivatedByPointer:!1,wasElementMadeActive:!1,activationEvent:void 0,isProgrammatic:!1}}init(){const supportsPressRipple=this.supportsPressRipple_();this.registerRootHandlers_(supportsPressRipple);if(supportsPressRipple){const{ROOT,UNBOUNDED}=foundation_MDCRippleFoundation.cssClasses;requestAnimationFrame(()=>{this.adapter_.addClass(ROOT);if(this.adapter_.isUnbounded()){this.adapter_.addClass(UNBOUNDED);this.layoutInternal_()}})}}destroy(){if(this.supportsPressRipple_()){if(this.activationTimer_){clearTimeout(this.activationTimer_);this.activationTimer_=0;this.adapter_.removeClass(foundation_MDCRippleFoundation.cssClasses.FG_ACTIVATION)}if(this.fgDeactivationRemovalTimer_){clearTimeout(this.fgDeactivationRemovalTimer_);this.fgDeactivationRemovalTimer_=0;this.adapter_.removeClass(foundation_MDCRippleFoundation.cssClasses.FG_DEACTIVATION)}const{ROOT,UNBOUNDED}=foundation_MDCRippleFoundation.cssClasses;requestAnimationFrame(()=>{this.adapter_.removeClass(ROOT);this.adapter_.removeClass(UNBOUNDED);this.removeCssVars_()})}this.deregisterRootHandlers_();this.deregisterDeactivationHandlers_()}registerRootHandlers_(supportsPressRipple){if(supportsPressRipple){ACTIVATION_EVENT_TYPES.forEach(type=>{this.adapter_.registerInteractionHandler(type,this.activateHandler_)});if(this.adapter_.isUnbounded()){this.adapter_.registerResizeHandler(this.resizeHandler_)}}this.adapter_.registerInteractionHandler("focus",this.focusHandler_);this.adapter_.registerInteractionHandler("blur",this.blurHandler_)}registerDeactivationHandlers_(e){if("keydown"===e.type){this.adapter_.registerInteractionHandler("keyup",this.deactivateHandler_)}else{POINTER_DEACTIVATION_EVENT_TYPES.forEach(type=>{this.adapter_.registerDocumentInteractionHandler(type,this.deactivateHandler_)})}}deregisterRootHandlers_(){ACTIVATION_EVENT_TYPES.forEach(type=>{this.adapter_.deregisterInteractionHandler(type,this.activateHandler_)});this.adapter_.deregisterInteractionHandler("focus",this.focusHandler_);this.adapter_.deregisterInteractionHandler("blur",this.blurHandler_);if(this.adapter_.isUnbounded()){this.adapter_.deregisterResizeHandler(this.resizeHandler_)}}deregisterDeactivationHandlers_(){this.adapter_.deregisterInteractionHandler("keyup",this.deactivateHandler_);POINTER_DEACTIVATION_EVENT_TYPES.forEach(type=>{this.adapter_.deregisterDocumentInteractionHandler(type,this.deactivateHandler_)})}removeCssVars_(){const{strings}=foundation_MDCRippleFoundation;Object.keys(strings).forEach(k=>{if(0===k.indexOf("VAR_")){this.adapter_.updateCssVariable(strings[k],null)}})}activate_(e){if(this.adapter_.isSurfaceDisabled()){return}const activationState=this.activationState_;if(activationState.isActivated){return}const previousActivationEvent=this.previousActivationEvent_,isSameInteraction=previousActivationEvent&&e!==void 0&&previousActivationEvent.type!==e.type;if(isSameInteraction){return}activationState.isActivated=!0;activationState.isProgrammatic=e===void 0;activationState.activationEvent=e;activationState.wasActivatedByPointer=activationState.isProgrammatic?!1:e!==void 0&&("mousedown"===e.type||"touchstart"===e.type||"pointerdown"===e.type);const hasActivatedChild=e!==void 0&&0<activatedTargets.length&&activatedTargets.some(target=>this.adapter_.containsEventTarget(target));if(hasActivatedChild){this.resetActivationState_();return}if(e!==void 0){activatedTargets.push(e.target);this.registerDeactivationHandlers_(e)}activationState.wasElementMadeActive=this.checkElementMadeActive_(e);if(activationState.wasElementMadeActive){this.animateActivation_()}requestAnimationFrame(()=>{activatedTargets=[];if(!activationState.wasElementMadeActive&&e!==void 0&&(" "===e.key||32===e.keyCode)){activationState.wasElementMadeActive=this.checkElementMadeActive_(e);if(activationState.wasElementMadeActive){this.animateActivation_()}}if(!activationState.wasElementMadeActive){this.activationState_=this.defaultActivationState_()}})}checkElementMadeActive_(e){return e!==void 0&&"keydown"===e.type?this.adapter_.isSurfaceActive():!0}activate(event){this.activate_(event)}animateActivation_(){const{VAR_FG_TRANSLATE_START,VAR_FG_TRANSLATE_END}=foundation_MDCRippleFoundation.strings,{FG_DEACTIVATION,FG_ACTIVATION}=foundation_MDCRippleFoundation.cssClasses,{DEACTIVATION_TIMEOUT_MS}=foundation_MDCRippleFoundation.numbers;this.layoutInternal_();let translateStart="",translateEnd="";if(!this.adapter_.isUnbounded()){const{startPoint,endPoint}=this.getFgTranslationCoordinates_();translateStart=`${startPoint.x}px, ${startPoint.y}px`;translateEnd=`${endPoint.x}px, ${endPoint.y}px`}this.adapter_.updateCssVariable(VAR_FG_TRANSLATE_START,translateStart);this.adapter_.updateCssVariable(VAR_FG_TRANSLATE_END,translateEnd);clearTimeout(this.activationTimer_);clearTimeout(this.fgDeactivationRemovalTimer_);this.rmBoundedActivationClasses_();this.adapter_.removeClass(FG_DEACTIVATION);this.adapter_.computeBoundingRect();this.adapter_.addClass(FG_ACTIVATION);this.activationTimer_=setTimeout(()=>this.activationTimerCallback_(),DEACTIVATION_TIMEOUT_MS)}getFgTranslationCoordinates_(){const{activationEvent,wasActivatedByPointer}=this.activationState_;let startPoint;if(wasActivatedByPointer){startPoint=getNormalizedEventCoords(activationEvent,this.adapter_.getWindowPageOffset(),this.adapter_.computeBoundingRect())}else{startPoint={x:this.frame_.width/2,y:this.frame_.height/2}}startPoint={x:startPoint.x-this.initialSize_/2,y:startPoint.y-this.initialSize_/2};const endPoint={x:this.frame_.width/2-this.initialSize_/2,y:this.frame_.height/2-this.initialSize_/2};return{startPoint,endPoint}}runDeactivationUXLogicIfReady_(){const{FG_DEACTIVATION}=foundation_MDCRippleFoundation.cssClasses,{hasDeactivationUXRun,isActivated}=this.activationState_;if((hasDeactivationUXRun||!isActivated)&&this.activationAnimationHasEnded_){this.rmBoundedActivationClasses_();this.adapter_.addClass(FG_DEACTIVATION);this.fgDeactivationRemovalTimer_=setTimeout(()=>{this.adapter_.removeClass(FG_DEACTIVATION)},numbers.FG_DEACTIVATION_MS)}}rmBoundedActivationClasses_(){const{FG_ACTIVATION}=foundation_MDCRippleFoundation.cssClasses;this.adapter_.removeClass(FG_ACTIVATION);this.activationAnimationHasEnded_=!1;this.adapter_.computeBoundingRect()}resetActivationState_(){this.previousActivationEvent_=this.activationState_.activationEvent;this.activationState_=this.defaultActivationState_();setTimeout(()=>this.previousActivationEvent_=void 0,foundation_MDCRippleFoundation.numbers.TAP_DELAY_MS)}deactivate_(){const activationState=this.activationState_;if(!activationState.isActivated){return}const state=Object.assign({},activationState);if(activationState.isProgrammatic){requestAnimationFrame(()=>this.animateDeactivation_(state));this.resetActivationState_()}else{this.deregisterDeactivationHandlers_();requestAnimationFrame(()=>{this.activationState_.hasDeactivationUXRun=!0;this.animateDeactivation_(state);this.resetActivationState_()})}}deactivate(){this.deactivate_()}animateDeactivation_({wasActivatedByPointer,wasElementMadeActive}){if(wasActivatedByPointer||wasElementMadeActive){this.runDeactivationUXLogicIfReady_()}}layout(){if(this.layoutFrame_){cancelAnimationFrame(this.layoutFrame_)}this.layoutFrame_=requestAnimationFrame(()=>{this.layoutInternal_();this.layoutFrame_=0})}layoutInternal_(){this.frame_=this.adapter_.computeBoundingRect();const maxDim=Math.max(this.frame_.height,this.frame_.width);this.maxRadius_=this.adapter_.isUnbounded()?maxDim:(()=>{var _Mathpow=Math.pow;const hypotenuse=Math.sqrt(_Mathpow(this.frame_.width,2)+_Mathpow(this.frame_.height,2));return hypotenuse+foundation_MDCRippleFoundation.numbers.PADDING})();this.initialSize_=Math.floor(maxDim*foundation_MDCRippleFoundation.numbers.INITIAL_ORIGIN_SCALE);this.fgScale_=this.maxRadius_/this.initialSize_;this.updateLayoutCssVars_()}updateLayoutCssVars_(){var _Mathround=Math.round;const{VAR_FG_SIZE,VAR_LEFT,VAR_TOP,VAR_FG_SCALE}=foundation_MDCRippleFoundation.strings;this.adapter_.updateCssVariable(VAR_FG_SIZE,`${this.initialSize_}px`);this.adapter_.updateCssVariable(VAR_FG_SCALE,this.fgScale_);if(this.adapter_.isUnbounded()){this.unboundedCoords_={left:_Mathround(this.frame_.width/2-this.initialSize_/2),top:_Mathround(this.frame_.height/2-this.initialSize_/2)};this.adapter_.updateCssVariable(VAR_LEFT,`${this.unboundedCoords_.left}px`);this.adapter_.updateCssVariable(VAR_TOP,`${this.unboundedCoords_.top}px`)}}setUnbounded(unbounded){const{UNBOUNDED}=foundation_MDCRippleFoundation.cssClasses;if(unbounded){this.adapter_.addClass(UNBOUNDED)}else{this.adapter_.removeClass(UNBOUNDED)}}handleFocus(){requestAnimationFrame(()=>this.adapter_.addClass(foundation_MDCRippleFoundation.cssClasses.BG_FOCUSED))}handleBlur(){requestAnimationFrame(()=>this.adapter_.removeClass(foundation_MDCRippleFoundation.cssClasses.BG_FOCUSED))}}/**
@license
Copyright 2018 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/const style=lit_element.c`<style>@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}</style>`,MATCHES=getMatchesProperty(HTMLElement.prototype),ripple_directive_supportsCssVariables=supportsCssVariables(window),isSafari=navigator.userAgent.match(/Safari/);/**
@license
Copyright 2018 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/let didApplyRippleStyle=!1;const applyRippleStyle=()=>{didApplyRippleStyle=!0;const part=new lit_html.b({templateFactory:lit_html.l});part.appendInto(document.head);part.setValue(style);part.commit()},rippleNode=options=>{if(isSafari&&!didApplyRippleStyle){applyRippleStyle()}const surfaceNode=options.surfaceNode,interactionNode=options.interactionNode||surfaceNode;if(interactionNode.getRootNode()!==surfaceNode.getRootNode()){if(""===interactionNode.style.position){interactionNode.style.position="relative"}}const rippleFoundation=new foundation_MDCRippleFoundation({browserSupportsCssVars:()=>ripple_directive_supportsCssVariables,isUnbounded:()=>options.unbounded===void 0?!0:options.unbounded,isSurfaceActive:()=>interactionNode[MATCHES](":active"),isSurfaceDisabled:()=>!!options.disabled,addClass:className=>surfaceNode.classList.add(className),removeClass:className=>surfaceNode.classList.remove(className),containsEventTarget:target=>interactionNode.contains(target),registerInteractionHandler:(type,handler)=>interactionNode.addEventListener(type,handler,applyPassive()),deregisterInteractionHandler:(type,handler)=>interactionNode.removeEventListener(type,handler,applyPassive()),registerDocumentInteractionHandler:(evtType,handler)=>document.documentElement.addEventListener(evtType,handler,applyPassive()),deregisterDocumentInteractionHandler:(evtType,handler)=>document.documentElement.removeEventListener(evtType,handler,applyPassive()),registerResizeHandler:handler=>window.addEventListener("resize",handler),deregisterResizeHandler:handler=>window.removeEventListener("resize",handler),updateCssVariable:(varName,value)=>surfaceNode.style.setProperty(varName,value),computeBoundingRect:()=>interactionNode.getBoundingClientRect(),getWindowPageOffset:()=>({x:window.pageXOffset,y:window.pageYOffset})});rippleFoundation.init();return rippleFoundation},rippleInteractionNodes=new WeakMap,ripple=(options={})=>Object(lit_html.f)(part=>{const surfaceNode=part.committer.element,interactionNode=options.interactionNode||surfaceNode;let rippleFoundation=part.value;const existingInteractionNode=rippleInteractionNodes.get(rippleFoundation);if(existingInteractionNode!==void 0&&existingInteractionNode!==interactionNode){rippleFoundation.destroy();rippleFoundation=lit_html.h}if(rippleFoundation===lit_html.h){rippleFoundation=rippleNode(Object.assign({},options,{surfaceNode}));rippleInteractionNodes.set(rippleFoundation,interactionNode);part.setValue(rippleFoundation)}else{if(options.unbounded!==void 0){rippleFoundation.setUnbounded(options.unbounded)}if(options.disabled!==void 0){rippleFoundation.setUnbounded(options.disabled)}}if(!0===options.active){rippleFoundation.activate()}else if(!1===options.active){rippleFoundation.deactivate()}}),mwc_ripple_css_style=lit_element.c`<style>@keyframes mdc-ripple-fg-radius-in{from{animation-timing-function:cubic-bezier(0.4, 0, 0.2, 1);transform:translate(var(--mdc-ripple-fg-translate-start, 0)) scale(1)}to{transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}}@keyframes mdc-ripple-fg-opacity-in{from{animation-timing-function:linear;opacity:0}to{opacity:var(--mdc-ripple-fg-opacity, 0)}}@keyframes mdc-ripple-fg-opacity-out{from{animation-timing-function:linear;opacity:var(--mdc-ripple-fg-opacity, 0)}to{opacity:0}}.mdc-ripple-surface--test-edge-var-bug{--mdc-ripple-surface-test-edge-var: 1px solid #000;visibility:hidden}.mdc-ripple-surface--test-edge-var-bug::before{border:var(--mdc-ripple-surface-test-edge-var)}.mdc-ripple-surface{--mdc-ripple-fg-size: 0;--mdc-ripple-left: 0;--mdc-ripple-top: 0;--mdc-ripple-fg-scale: 1;--mdc-ripple-fg-translate-end: 0;--mdc-ripple-fg-translate-start: 0;-webkit-tap-highlight-color:rgba(0,0,0,0);will-change:transform,opacity;position:relative;outline:none;overflow:hidden}.mdc-ripple-surface::before,.mdc-ripple-surface::after{position:absolute;border-radius:50%;opacity:0;pointer-events:none;content:""}.mdc-ripple-surface::before{transition:opacity 15ms linear;z-index:1}.mdc-ripple-surface.mdc-ripple-upgraded::before{transform:scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface.mdc-ripple-upgraded::after{top:0;left:0;transform:scale(0);transform-origin:center center}.mdc-ripple-surface.mdc-ripple-upgraded--unbounded::after{top:var(--mdc-ripple-top, 0);left:var(--mdc-ripple-left, 0)}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-activation::after{animation:225ms mdc-ripple-fg-radius-in forwards,75ms mdc-ripple-fg-opacity-in forwards}.mdc-ripple-surface.mdc-ripple-upgraded--foreground-deactivation::after{animation:150ms mdc-ripple-fg-opacity-out;transform:translate(var(--mdc-ripple-fg-translate-end, 0)) scale(var(--mdc-ripple-fg-scale, 1))}.mdc-ripple-surface::before,.mdc-ripple-surface::after{background-color:#000}.mdc-ripple-surface:hover::before{opacity:.04}.mdc-ripple-surface:not(.mdc-ripple-upgraded):focus::before,.mdc-ripple-surface.mdc-ripple-upgraded--background-focused::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.16}.mdc-ripple-surface.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.16}.mdc-ripple-surface::before,.mdc-ripple-surface::after{top:calc(50% - 100%);left:calc(50% - 100%);width:200%;height:200%}.mdc-ripple-surface.mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded]{overflow:visible}.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded]::after{top:calc(50% - 50%);left:calc(50% - 50%);width:100%;height:100%}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::before,.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after{top:var(--mdc-ripple-top, calc(50% - 50%));left:var(--mdc-ripple-left, calc(50% - 50%));width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface[data-mdc-ripple-is-unbounded].mdc-ripple-upgraded::after{width:var(--mdc-ripple-fg-size, 100%);height:var(--mdc-ripple-fg-size, 100%)}.mdc-ripple-surface--primary::before,.mdc-ripple-surface--primary::after{background-color:#6200ee}@supports not (-ms-ime-align: auto){.mdc-ripple-surface--primary::before,.mdc-ripple-surface--primary::after{background-color:var(--mdc-theme-primary, #6200ee)}}.mdc-ripple-surface--primary:hover::before{opacity:.04}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):focus::before,.mdc-ripple-surface--primary.mdc-ripple-upgraded--background-focused::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--primary:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.16}.mdc-ripple-surface--primary.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.16}.mdc-ripple-surface--accent::before,.mdc-ripple-surface--accent::after{background-color:#018786}@supports not (-ms-ime-align: auto){.mdc-ripple-surface--accent::before,.mdc-ripple-surface--accent::after{background-color:var(--mdc-theme-secondary, #018786)}}.mdc-ripple-surface--accent:hover::before{opacity:.04}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):focus::before,.mdc-ripple-surface--accent.mdc-ripple-upgraded--background-focused::before{transition-duration:75ms;opacity:.12}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded)::after{transition:opacity 150ms linear}.mdc-ripple-surface--accent:not(.mdc-ripple-upgraded):active::after{transition-duration:75ms;opacity:.16}.mdc-ripple-surface--accent.mdc-ripple-upgraded{--mdc-ripple-fg-opacity: 0.16}.mdc-ripple-surface{pointer-events:none;position:absolute;top:0;right:0;bottom:0;left:0}</style>`;/**
@license
Copyright 2018 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/var __decorate=void 0||function(decorators,target,key,desc){var c=arguments.length,r=3>c?target:null===desc?desc=Object.getOwnPropertyDescriptor(target,key):desc,d;if("object"===typeof Reflect&&"function"===typeof Reflect.decorate)r=Reflect.decorate(decorators,target,key,desc);else for(var i=decorators.length-1;0<=i;i--)if(d=decorators[i])r=(3>c?d(r):3<c?d(target,key,r):d(target,key))||r;return 3<c&&r&&Object.defineProperty(target,key,r),r};/**
@license
Copyright 2018 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/let mwc_ripple_Ripple=class extends lit_element.a{constructor(){super(...arguments);this.primary=!1;this.accent=!1;this.unbounded=!1;this.disabled=!1;this.interactionNode=this}renderStyle(){return mwc_ripple_css_style}connectedCallback(){this.interactionNode=this.parentNode}render(){const classes={"mdc-ripple-surface--primary":this.primary,"mdc-ripple-surface--accent":this.accent},{disabled,unbounded,active,interactionNode}=this,rippleOptions={disabled,unbounded,interactionNode};if(active!==void 0){rippleOptions.active=active}return lit_element.c`
      ${this.renderStyle()}
      <div .ripple="${ripple(rippleOptions)}"
          class="mdc-ripple-surface ${Object(classMap.a)(classes)}"></div>`}};__decorate([Object(lit_element.d)({type:Boolean})],mwc_ripple_Ripple.prototype,"primary",void 0);__decorate([Object(lit_element.d)({type:Boolean})],mwc_ripple_Ripple.prototype,"active",void 0);__decorate([Object(lit_element.d)({type:Boolean})],mwc_ripple_Ripple.prototype,"accent",void 0);__decorate([Object(lit_element.d)({type:Boolean})],mwc_ripple_Ripple.prototype,"unbounded",void 0);__decorate([Object(lit_element.d)({type:Boolean})],mwc_ripple_Ripple.prototype,"disabled",void 0);__decorate([Object(lit_element.d)()],mwc_ripple_Ripple.prototype,"interactionNode",void 0);mwc_ripple_Ripple=__decorate([Object(lit_element.b)("mwc-ripple")],mwc_ripple_Ripple)}}]);
//# sourceMappingURL=3e07c1dec7bef00d5ca3.chunk.js.map