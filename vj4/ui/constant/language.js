import attachObjectMeta from './util/objectMeta';

export const LANG_TEXTS = {
  c: 'C',
  cc: 'C++',
  cs: 'C#',
  java: 'Java',
  py3: 'Python 3',
  js: 'JavaScript',
};

export const LANG_HIGHLIGHT_ID = {
  c: 'c',
  cc: 'cpp',
  cs: 'csharp',
  java: 'java',
  py3: 'python',
  js: 'javascript',
};

export const LANG_CODEMIRROR_MODES = {
  c: 'text/x-csrc',
  cc: 'text/x-c++src',
  cs: 'text/x-csharp',
  java: 'text/x-java',
  py3: 'text/x-python',
  js: 'text/javascript',
};
attachObjectMeta(LANG_CODEMIRROR_MODES, 'exportToPython', false);
