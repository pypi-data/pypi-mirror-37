(window.webpackJsonp=window.webpackJsonp||[]).push([[59],{202:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"b",function(){return PaperDialogBehaviorImpl});__webpack_require__.d(__webpack_exports__,"a",function(){return PaperDialogBehavior});var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(53),_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(1);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const PaperDialogBehaviorImpl={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.__readied=!0},_modalChanged:function(modal,readied){if(!readied){return}if(modal){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick;this.__prevNoCancelOnEscKey=this.noCancelOnEscKey;this.__prevWithBackdrop=this.withBackdrop;this.noCancelOnOutsideClick=!0;this.noCancelOnEscKey=!0;this.withBackdrop=!0}else{this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick;this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey;this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop}},_updateClosingReasonConfirmed:function(confirmed){this.closingReason=this.closingReason||{};this.closingReason.confirmed=confirmed},_onDialogClick:function(event){for(var path=Object(_polymer_polymer_lib_legacy_polymer_dom_js__WEBPACK_IMPORTED_MODULE_2__.b)(event).path,i=0,l=path.indexOf(this),target;i<l;i++){target=path[i];if(target.hasAttribute&&(target.hasAttribute("dialog-dismiss")||target.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(target.hasAttribute("dialog-confirm"));this.close();event.stopPropagation();break}}}},PaperDialogBehavior=[_polymer_iron_overlay_behavior_iron_overlay_behavior_js__WEBPACK_IMPORTED_MODULE_1__.a,PaperDialogBehaviorImpl]},204:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_iron_flex_layout_iron_flex_layout_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(26),_polymer_paper_styles_default_theme_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(29),_polymer_paper_styles_typography_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(42),_polymer_paper_styles_shadow_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(63);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/const $_documentContainer=document.createElement("template");$_documentContainer.setAttribute("style","display: none;");$_documentContainer.innerHTML=`<dom-module id="paper-dialog-shared-styles">
  <template>
    <style>
      :host {
        display: block;
        margin: 24px 40px;

        background: var(--paper-dialog-background-color, var(--primary-background-color));
        color: var(--paper-dialog-color, var(--primary-text-color));

        @apply --paper-font-body1;
        @apply --shadow-elevation-16dp;
        @apply --paper-dialog;
      }

      :host > ::slotted(*) {
        margin-top: 20px;
        padding: 0 24px;
      }

      :host > ::slotted(.no-padding) {
        padding: 0;
      }

      
      :host > ::slotted(*:first-child) {
        margin-top: 24px;
      }

      :host > ::slotted(*:last-child) {
        margin-bottom: 24px;
      }

      /* In 1.x, this selector was \`:host > ::content h2\`. In 2.x <slot> allows
      to select direct children only, which increases the weight of this
      selector, so we have to re-define first-child/last-child margins below. */
      :host > ::slotted(h2) {
        position: relative;
        margin: 0;

        @apply --paper-font-title;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-top. */
      :host > ::slotted(h2:first-child) {
        margin-top: 24px;
        @apply --paper-dialog-title;
      }

      /* Apply mixin again, in case it sets margin-bottom. */
      :host > ::slotted(h2:last-child) {
        margin-bottom: 24px;
        @apply --paper-dialog-title;
      }

      :host > ::slotted(.paper-dialog-buttons),
      :host > ::slotted(.buttons) {
        position: relative;
        padding: 8px 8px 8px 24px;
        margin: 0;

        color: var(--paper-dialog-button-color, var(--primary-color));

        @apply --layout-horizontal;
        @apply --layout-end-justified;
      }
    </style>
  </template>
</dom-module>`;document.head.appendChild($_documentContainer.content)},207:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_paper_dialog_behavior_paper_dialog_shared_styles_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(204),_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(95),_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(202),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(3),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_4__.a)({_template:_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_5__.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[_polymer_paper_dialog_behavior_paper_dialog_behavior_js__WEBPACK_IMPORTED_MODULE_3__.a,_polymer_neon_animation_neon_animation_runner_behavior_js__WEBPACK_IMPORTED_MODULE_2__.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation();this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation();this.playAnimation("exit")},_onNeonAnimationFinish:function(){if(this.opened){this._finishRenderOpened()}else{this._finishRenderClosed()}}})},210:function(module,__webpack_exports__,__webpack_require__){"use strict";var polymer_legacy=__webpack_require__(2),iron_flex_layout=__webpack_require__(26),iron_control_state=__webpack_require__(12),iron_validatable_behavior=__webpack_require__(37),polymer_fn=__webpack_require__(3),polymer_dom=__webpack_require__(1),html_tag=__webpack_require__(0);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(polymer_fn.a)({_template:html_tag.a`
    <style>
      :host {
        display: inline-block;
        position: relative;
        width: 400px;
        border: 1px solid;
        padding: 2px;
        -moz-appearance: textarea;
        -webkit-appearance: textarea;
        overflow: hidden;
      }

      .mirror-text {
        visibility: hidden;
        word-wrap: break-word;
        @apply --iron-autogrow-textarea;
      }

      .fit {
        @apply --layout-fit;
      }

      textarea {
        position: relative;
        outline: none;
        border: none;
        resize: none;
        background: inherit;
        color: inherit;
        /* see comments in template */
        width: 100%;
        height: 100%;
        font-size: inherit;
        font-family: inherit;
        line-height: inherit;
        text-align: inherit;
        @apply --iron-autogrow-textarea;
      }

      textarea::-webkit-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea::-moz-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }

      textarea:-ms-input-placeholder {
        @apply --iron-autogrow-textarea-placeholder;
      }
    </style>

    <!-- the mirror sizes the input/textarea so it grows with typing -->
    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->
    <div id="mirror" class="mirror-text" aria-hidden="true">&nbsp;</div>

    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->
    <div class="textarea-container fit">
      <textarea id="textarea" name\$="[[name]]" aria-label\$="[[label]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" disabled\$="[[disabled]]" rows\$="[[rows]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]"></textarea>
    </div>
`,is:"iron-autogrow-textarea",behaviors:[iron_validatable_behavior.a,iron_control_state.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(value){this.$.textarea.selectionStart=value},set selectionEnd(value){this.$.textarea.selectionEnd=value},attached:function(){var IS_IOS=navigator.userAgent.match(/iP(?:[oa]d|hone)/);if(IS_IOS){this.$.textarea.style.marginLeft="-3px"}},validate:function(){var valid=this.$.textarea.validity.valid;if(valid){if(this.required&&""===this.value){valid=!1}else if(this.hasValidator()){valid=iron_validatable_behavior.a.validate.call(this,this.value)}}this.invalid=!valid;this.fire("iron-input-validate");return valid},_bindValueChanged:function(bindValue){this.value=bindValue},_valueChanged:function(value){var textarea=this.textarea;if(!textarea){return}if(textarea.value!==value){textarea.value=!(value||0===value)?"":value}this.bindValue=value;this.$.mirror.innerHTML=this._valueForMirror();this.fire("bind-value-changed",{value:this.bindValue})},_onInput:function(event){var eventPath=Object(polymer_dom.b)(event).path;this.value=eventPath?eventPath[0].value:event.target.value},_constrain:function(tokens){var _tokens;tokens=tokens||[""];if(0<this.maxRows&&tokens.length>this.maxRows){_tokens=tokens.slice(0,this.maxRows)}else{_tokens=tokens.slice(0)}while(0<this.rows&&_tokens.length<this.rows){_tokens.push("")}return _tokens.join("<br/>")+"&#160;"},_valueForMirror:function(){var input=this.textarea;if(!input){return}this.tokens=input&&input.value?input.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""];return this._constrain(this.tokens)},_updateCached:function(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});var paper_input_char_counter=__webpack_require__(91),paper_input_container=__webpack_require__(92),paper_input_error=__webpack_require__(93),iron_form_element_behavior=__webpack_require__(34),paper_input_behavior=__webpack_require__(68);/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(polymer_fn.a)({_template:html_tag.a`
    <style>
      :host {
        display: block;
      }

      :host([hidden]) {
        display: none !important;
      }

      label {
        pointer-events: none;
      }
    </style>

    <paper-input-container no-label-float\$="[[noLabelFloat]]" always-float-label="[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]" auto-validate\$="[[autoValidate]]" disabled\$="[[disabled]]" invalid="[[invalid]]">

      <label hidden\$="[[!label]]" aria-hidden="true" for\$="[[_inputId]]" slot="label">[[label]]</label>

      <iron-autogrow-textarea class="paper-input-input" slot="input" id\$="[[_inputId]]" aria-labelledby\$="[[_ariaLabelledBy]]" aria-describedby\$="[[_ariaDescribedBy]]" bind-value="{{value}}" invalid="{{invalid}}" validator\$="[[validator]]" disabled\$="[[disabled]]" autocomplete\$="[[autocomplete]]" autofocus\$="[[autofocus]]" inputmode\$="[[inputmode]]" name\$="[[name]]" placeholder\$="[[placeholder]]" readonly\$="[[readonly]]" required\$="[[required]]" minlength\$="[[minlength]]" maxlength\$="[[maxlength]]" autocapitalize\$="[[autocapitalize]]" rows\$="[[rows]]" max-rows\$="[[maxRows]]" on-change="_onChange"></iron-autogrow-textarea>

      <template is="dom-if" if="[[errorMessage]]">
        <paper-input-error aria-live="assertive" slot="add-on">[[errorMessage]]</paper-input-error>
      </template>

      <template is="dom-if" if="[[charCounter]]">
        <paper-input-char-counter slot="add-on"></paper-input-char-counter>
      </template>

    </paper-input-container>
`,is:"paper-textarea",behaviors:[paper_input_behavior.a,iron_form_element_behavior.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(start){this.$.input.textarea.selectionStart=start},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(end){this.$.input.textarea.selectionEnd=end},_ariaLabelledByChanged:function(ariaLabelledBy){this._focusableElement.setAttribute("aria-labelledby",ariaLabelledBy)},_ariaDescribedByChanged:function(ariaDescribedBy){this._focusableElement.setAttribute("aria-describedby",ariaDescribedBy)},get _focusableElement(){return this.inputElement.textarea}})},676:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element=__webpack_require__(198),fire_event=__webpack_require__(76),paper_button=__webpack_require__(54),paper_textarea=__webpack_require__(210),paper_dialog=__webpack_require__(207);const getCardConfig=(hass,cardId)=>hass.callWS({type:"lovelace/config/card/get",card_id:cardId}),updateCardConfig=(hass,cardId,config)=>hass.callWS({type:"lovelace/config/card/update",card_id:cardId,card_config:config});__webpack_require__.d(__webpack_exports__,"HuiEditCardModal",function(){return ha_dialog_edit_card_HuiEditCardModal});class ha_dialog_edit_card_HuiEditCardModal extends lit_element.a{static get properties(){return{hass:{},cardId:{type:Number},_cardConfig:{},_dialogClosedCallback:{}}}async showDialog({hass,cardId,reloadLovelace}){this.hass=hass;this._cardId=cardId;this._reloadLovelace=reloadLovelace;this._loadConfig();await this.updateComplete;this._dialog.open()}get _dialog(){return this.shadowRoot.querySelector("paper-dialog")}render(){return lit_element.c`
      <style>
        paper-dialog {
          width: 650px;
        }
      </style>
      <paper-dialog with-backdrop>
        <h2>Card Configuration</h2>
        <paper-textarea
          value="${this._cardConfig}"
        ></paper-textarea>
        <div class="paper-dialog-buttons">
          <paper-button @click="${this._closeDialog}">Cancel</paper-button>
          <paper-button @click="${this._updateConfig}">Save</paper-button>
        </div>
      </paper-dialog>
    `}_closeDialog(){this._dialog.close()}async _loadConfig(){this._cardConfig=await getCardConfig(this.hass,this._cardId);await this.updateComplete;Object(fire_event.a)(this._dialog,"iron-resize")}async _updateConfig(){const newCardConfig=this.shadowRoot.querySelector("paper-textarea").value;if(this._cardConfig===newCardConfig){this._dialog.close();return}try{await updateCardConfig(this.hass,this._cardId,newCardConfig);this._dialog.close();this._reloadLovelace()}catch(err){alert(`Saving failed: ${err.reason}`)}}}customElements.define("ha-dialog-edit-card",ha_dialog_edit_card_HuiEditCardModal)}}]);
//# sourceMappingURL=dc30f14eae0b712dd5b7.chunk.js.map