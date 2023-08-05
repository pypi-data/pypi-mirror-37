import { configure } from '@storybook/react';

// automatically import all files ending in *.stories.js
function loadStories() {
  // https://www.npmjs.com/package/require-context
  const req = require.context('../app', true, /\-story\.js$/);
  req.keys().forEach(filename => req(filename));
}

configure(loadStories, module);