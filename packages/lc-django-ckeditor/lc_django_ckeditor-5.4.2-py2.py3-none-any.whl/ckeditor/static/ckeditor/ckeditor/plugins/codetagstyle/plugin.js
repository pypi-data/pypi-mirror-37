CKEDITOR.plugins.add('codetagstyle', {
  icons: 'code',
  init(editor) {
    var style = new CKEDITOR.style({ element: 'code' }),
      forms = ['code'];

    // Put the style as the most important form.
    forms.unshift(style);

    // Listen to contextual style activation.
    editor.attachStyleStateChange(style, function (state) {
      !editor.readOnly && editor.getCommand('wrapCode').setState(state);
    });

    // Create the command that can be used to apply the style.
    editor.addCommand('wrapCode', new CKEDITOR.styleCommand(style, {
      contentForms: forms,
    }));

    // Register the button, if the button plugin is loaded.
    if (editor.ui.addButton) {
      editor.ui.addButton('Code', {
        label: 'Code',
        command: 'wrapCode',
        toolbar: 'insert',
      });
    }

    editor.setKeystroke([
      [CKEDITOR.CTRL + 75, 'wrapCode'],
    ]);
  },
});
