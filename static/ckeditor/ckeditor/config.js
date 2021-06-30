/**
 * @license Copyright (c) 2003-2021, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.height = '450px';
	config.toolbar_customer =
    [
        ['Styles','Format','Bold','Italic','Underline','Strike','SpellChecker','Undo','Redo'],
		['Link','Unlink'],
		['Image','Table','HorizontalRule'],
		['TextColor','BGColor'],
		['Smiley','SpecialChar'], 
		['Source'],
		['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
		['NumberedList','BulletedList'],
		['Indent','Outdent'],
		['Maximize'],
    ];
    config.toolbar = 'customer';
};
