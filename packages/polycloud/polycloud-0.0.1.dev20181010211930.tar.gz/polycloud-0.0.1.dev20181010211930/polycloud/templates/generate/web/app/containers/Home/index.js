/**
 *
 * Home
 *
 */

import React from 'react';
import { connect } from 'react-redux';
import { Helmet } from 'react-helmet';
import { FormattedMessage } from 'react-intl';
import { createStructuredSelector } from 'reselect';
import { compose } from 'redux';
import { Menu, Layout, Button, Row, Col, List, Icon } from 'antd';

import injectSaga from 'utils/injectSaga';
import injectReducer from 'utils/injectReducer';
import { login, loadProducts, checkLogin } from './actions';
import {
  makeSelectPlatform,
  makeSelectServices,
  makeSelectKeycloak,
} from './selectors';
import reducer from './reducer';
import saga from './saga';
import messages from './messages';
import logo from '../../images/logo.svg';
import './index.css';

const { Header, Content, Footer } = Layout;

/* eslint-disable react/prefer-stateless-function */
export class Home extends React.Component {
  componentDidMount() {
    this.props.checkLogin();
    this.props.loadProducts();
  }

  render() {
    const defaultSelected = ['Products'];
    return (
      <div>
        <Helmet>
          <title>
            An integrated suite of cloud products, services and solutions |
            zealous Cloud
          </title>
          <meta name="description" content="Description of Home" />
        </Helmet>
        <Layout className="layout">
          <Header className="header-light">
            <Row type="flex" justify="space-between">
              <Col span={15}>
                <img className="logo" src={logo} alt="logo" />
              </Col>
              <Col span={4} offset={4}>
                <Menu
                  theme="light"
                  mode="horizontal"
                  defaultSelectedKeys={defaultSelected}
                  style={{ lineHeight: '64px' }}
                  id="nav"
                  key="nav"
                >
                  <Menu.Item key="products">
                    <FormattedMessage {...messages.headerNavEntryProducts} />
                  </Menu.Item>
                  <Menu.Item key="documentation">
                    <FormattedMessage
                      {...messages.headerNavEntryDocumentation}
                    />
                  </Menu.Item>
                </Menu>
              </Col>
              <Col span={1}>
                <Button
                  onClick={() => this.props.onLoginClick()}
                  type={
                    this.props.keycloak.authenticated ? 'primary' : 'default'
                  }
                  shape="circle"
                  icon={this.props.keycloak.authenticated ? 'logout' : 'login'}
                />
              </Col>
            </Row>
          </Header>
          <Content>
            <Row>
              <div
                className="banner"
                style={{ background: '#fff', padding: 100, minHeight: 280 }}
              >
                <h1 style={{ textAlign: 'center' }}>
                  <FormattedMessage {...messages.contentKeyMessage} />
                </h1>
                <div
                  className="urgent-call-to-action"
                  style={{ textAlign: 'center', padding: '45px' }}
                >
                  <Button type="primary" icon="double-right" size="large" ghost>
                    <FormattedMessage {...messages.contentActionButton} />
                  </Button>
                </div>
              </div>
            </Row>
            <Row gutter={16} style={{ padding: '0 30px' }}>
              <h1 style={{ padding: '45px' }}>
                <FormattedMessage {...messages.contentPoductsHeading} />
              </h1>
              <Col span={12}>
                <List
                  header={
                    <div>
                      <h2>
                        <Icon type="api" />{' '}
                        <FormattedMessage
                          {...messages.poductsSubHeadingServices}
                        />
                      </h2>
                    </div>
                  }
                  bordered
                  dataSource={this.props.services}
                  renderItem={item => <List.Item>{item.name}</List.Item>}
                  style={{ background: '#fff' }}
                />
              </Col>
              <Col span={12}>
                <List
                  header={
                    <div>
                      <h2>
                        <Icon type="block" />{' '}
                        <FormattedMessage
                          {...messages.poductsSubHeadingPlatform}
                        />
                      </h2>
                    </div>
                  }
                  bordered
                  dataSource={this.props.platform}
                  renderItem={item => <List.Item>{item.name}</List.Item>}
                  style={{ background: '#fff' }}
                />
              </Col>
            </Row>
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            <FormattedMessage {...messages.footer} />
          </Footer>
        </Layout>
      </div>
    );
  }
}

const mapStateToProps = createStructuredSelector({
  services: makeSelectServices(),
  platform: makeSelectPlatform(),
  keycloak: makeSelectKeycloak(),
});

function mapDispatchToProps(dispatch) {
  return {
    loadProducts: () => {
      dispatch(loadProducts());
    },
    onLoginClick: () => {
      dispatch(login());
    },
    checkLogin: () => {
      dispatch(checkLogin());
    },
  };
}

const withConnect = connect(
  mapStateToProps,
  mapDispatchToProps,
);

const withReducer = injectReducer({ key: 'home', reducer });
const withSaga = injectSaga({ key: 'home', saga });

export default compose(
  withReducer,
  withSaga,
  withConnect,
)(Home);
