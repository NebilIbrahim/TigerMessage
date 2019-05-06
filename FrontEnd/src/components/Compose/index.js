import React, { Component } from 'react';
import io from 'socket.io-client';
import './Compose.css';

const socket = io();
export default class Compose extends Component {

    constructor(props) {
      super(props);

      this.state = {
         data: 'Initial data...',
         username: '',
         chat: '',

      }
      this.handleSubmit = this.handleSubmit.bind(this);
   };
   handleSubmit(e) {
    e.preventDefault(); // prevents page reloading
    let userData = this.state.username;
    socket.emit('chat message', $('#m').val(), this.state.username, this.state.chat); // getCookie("uid")
    $('#m').val('');
    return false;
    }

  render() {
    return (
      <div className="compose">
        <input type="text" value = {this.state.data}
          onSubmit={this.handleSubmit}
          className="compose-input"
          placeholder="Type a message"
        />
        {
          this.props.rightItems
        }
      </div>
    );
  }
}