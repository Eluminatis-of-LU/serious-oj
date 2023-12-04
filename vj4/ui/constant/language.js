import attachObjectMeta from './util/objectMeta';

export const LANG_TEXTS = {
  c: 'C99 (GCC 11.4.0)',
  cc: 'C++17 (GCC 11.4.0)',
  cs: 'C# 7 (Mono 6.8)',
  cs_bflat: 'C# 11 (Bflat .NET 7.0.2)',
  java: 'Java 8 (OpenJDK 1.8.0_392)',
  py3: 'Python 3 (Python 3.10.12)',
  js: 'JavaScript (Node.js v12.22.9)',
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
