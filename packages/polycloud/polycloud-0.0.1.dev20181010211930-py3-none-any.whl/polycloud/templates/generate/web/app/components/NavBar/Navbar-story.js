import React from 'react';
import { storiesOf } from '@storybook/react';
import NavBar from './index';
import logo from '../../images/logo.svg';

storiesOf('NavBar', module)
  .add('authenticated new', () => {
    const elements = ['Products', 'Documentation'];
    const defaultSelected = ['Products'];
    return (
      <NavBar
        logo={logo}
        nav={elements}
        defaultSelected={defaultSelected}
        authenticated
      />
    );
  })
  .add('unauthenticated new', () => {
    const elements = ['Products', 'Documentation'];
    const defaultSelected = ['Products'];
    return (
      <NavBar
        logo={logo}
        nav={elements}
        defaultSelected={defaultSelected}
        authenticated={false}
      />
    );
  })
  .add('no logo new', () => {
    const elements = ['Products', 'Documentation'];
    const defaultSelected = ['Products'];
    return (
      <NavBar
        nav={elements}
        defaultSelected={defaultSelected}
        authenticated={false}
      />
    );
  });
