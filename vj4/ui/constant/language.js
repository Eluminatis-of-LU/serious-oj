import attachObjectMeta from './util/objectMeta';

export const LANG_TEXTS = {
  c: 'C',
  cc: 'C++',
  cs: 'C# (Mono 6.8)',
  cs_bflat: 'C# (Bflat .NET 7.0.2)',
  java: 'Java',
  py3: 'Python 3',
  js: 'JavaScript',
};

export const LANG_HIGHLIGHT_ID = {
  c: 'c',
  cc: 'cpp',
  cs: 'csharp',
  cs_bflat: 'csharp',
  java: 'java',
  py3: 'python',
  js: 'javascript',
};

export const LANG_CODEMIRROR_MODES = {
  c: 'text/x-csrc',
  cc: 'text/x-c++src',
  cs: 'text/x-csharp',
  cs_bflat: 'text/x-csharp',
  java: 'text/x-java',
  py3: 'text/x-python',
  js: 'text/javascript',
};
attachObjectMeta(LANG_CODEMIRROR_MODES, 'exportToPython', false);
