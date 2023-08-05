/**
 *
 * NavBar
 *
 */

import React from 'react';
import { Menu, Layout, Button, Row, Col } from 'antd';
import './NavBar.css';

const { Header } = Layout;

function NavBar(props) {
  return (
    <Header className="header-light">
      <Row type="flex" justify="space-between">
        <Col span={15}>
          {props.logo ? (
            <img className="logo" src={props.logo} alt="logo" />
          ) : (
            ''
          )}
        </Col>
        <Col span={4} offset={4}>
          <Menu
            theme="light"
            mode="horizontal"
            defaultSelectedKeys={props.defaultSelected}
            style={{ lineHeight: '64px' }}
            id="nav"
            key="nav"
          >
            {props.nav.map(element => (
              <Menu.Item key={element}>{element}</Menu.Item>
            ))}
          </Menu>
        </Col>
        <Col span={1}>
          <Button
            type={props.authenticated ? 'primary' : 'default'}
            shape="circle"
            icon={props.authenticated ? 'logout' : 'login'}
          />
        </Col>
      </Row>
    </Header>
  );
}

export default NavBar;
