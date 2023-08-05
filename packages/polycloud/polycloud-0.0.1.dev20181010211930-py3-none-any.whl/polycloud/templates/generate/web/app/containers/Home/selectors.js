import { createSelector } from 'reselect';
import { initialState } from './reducer';

/**
 * Direct selector to the home state domain
 */

/**
 * Other specific selectors
 */
const selectProducts = state => state.getIn(['home', 'products'], initialState);
const selectKeycloak = state => state.getIn(['home', 'keycloak'], initialState);
/**
 * Default selector used by Home
 */
const makeSelectServices = () =>
  createSelector(selectProducts, products =>
    products.filter(product => product.type === 'services'),
  );

const makeSelectPlatform = () =>
  createSelector(selectProducts, products =>
    products.filter(product => product.type === 'platform'),
  );

const makeSelectKeycloak = () =>
  createSelector(selectKeycloak, keycloakObject => keycloakObject);

export {
  makeSelectPlatform,
  makeSelectServices,
  selectProducts,
  makeSelectKeycloak,
};
