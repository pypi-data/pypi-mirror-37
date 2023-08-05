/*
 *
 * Home actions
 *
 */

import {
  DEFAULT_ACTION,
  LOGIN,
  LOGOUT,
  CHECK_LOGIN,
  LOAD_PRODUCTS,
} from './constants';

export function defaultAction() {
  return {
    type: DEFAULT_ACTION,
  };
}

export function login() {
  return { type: LOGIN };
}

export function logout() {
  return { type: LOGOUT };
}

export function checkLogin() {
  return { type: CHECK_LOGIN };
}

export function loadProducts() {
  return {
    type: LOAD_PRODUCTS,
  };
}
