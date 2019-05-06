
import React, { Component } from 'react';
import './Toolbar.css';

export default class Toolbar extends Component {
 constructor(props) {
    super(props);
        this.state = {
        input: '';
        username: '';
        socket = io();
        token = -1;
         chat = '';
        },

    this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleSubmit(this) {
    this.preventDefault(); // prevents page reloading
    let userData = this.state.netid;
    socket.emit('chat message', $('#m').val(), username, chat); // getCookie("uid")
    $('#m').val('');
    return false;
    }

  render() {
    const { title, leftItems, rightItems } = this.props;
    return (
      <div className="toolbar">
        <div className="left-items">{ leftItems }</div>
        <h1 className="toolbar-title">{ title }</h1>
        <div className="right-items">{ rightItems }</div>
      </div>
    );
  }
