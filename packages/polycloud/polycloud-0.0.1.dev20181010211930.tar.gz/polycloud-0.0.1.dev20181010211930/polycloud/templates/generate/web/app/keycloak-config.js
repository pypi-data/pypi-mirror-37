import Keycloak from 'keycloak-js';
import ksconfig from './keycloak.json';

export const keycloak = Keycloak(ksconfig);
