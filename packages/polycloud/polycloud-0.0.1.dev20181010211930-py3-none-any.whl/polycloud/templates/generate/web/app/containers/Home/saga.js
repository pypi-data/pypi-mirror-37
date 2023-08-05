// import { take, call, put, select } from 'redux-saga/effects';
import { put, takeLatest } from 'redux-saga/effects';
// Import Keycloak for auth
import { keycloak } from '../../keycloak-config';

import {
  LOGIN_SUCCEEDED,
  LOGIN,
  LOAD_PRODUCTS,
  LOAD_PRODUCTS_SUCCEEDED,
  CHECK_LOGIN,
} from './constants';

function* handleLogin() {
  // check in state if the user is authenticated and not expired otherwise redirect, get code (own saga handler?) -> get token -> update state
  yield keycloak.init({ onLoad: 'login-required' });
  yield put({ type: LOGIN_SUCCEEDED, payload: keycloak });
}

function* handleLoadProducts() {
  const mock = [
    {
      name: 'Product Info',
      type: 'services',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'Identity Access Management',
      type: 'platform',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'API Runtime',
      type: 'platform',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'API Management',
      type: 'platform',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'AI Development',
      type: 'platform',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'Risk Asessment',
      type: 'services',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'Adress Check',
      type: 'services',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
    {
      name: 'Investment',
      type: 'services',
      description: 'babba bla bla bla',
      links: {
        landing: 'http://api.d10l.de',
        production: '',
        sandbox: '',
        documentation: '',
      },
    },
  ];

  yield put({ type: LOAD_PRODUCTS_SUCCEEDED, products: mock });
}

function* handleCheckLogin() {
  yield keycloak.init({ onLoad: 'check-sso' });
  yield put({ type: LOGIN_SUCCEEDED, payload: keycloak });
}

/**
 * Root saga manages watcher lifecycle
 */
export default function* watchHome() {
  // Watches for LOAD_REPOS actions and calls getRepos when one comes in.
  // By using `takeLatest` only the result of the latest API call is applied.
  // It returns task descriptor (just like fork) so we can continue execution
  // It will be cancelled automatically on component unmount
  yield takeLatest(LOGIN, handleLogin);
  yield takeLatest(LOAD_PRODUCTS, handleLoadProducts);
  yield takeLatest(CHECK_LOGIN, handleCheckLogin);
}
