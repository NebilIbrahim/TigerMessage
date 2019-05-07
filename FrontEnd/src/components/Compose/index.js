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
         id: '',

      }
      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleChange = this.handleChange.bind(this);
   };
   handleSubmit(e) {
    e.preventDefault(); // prevents page reloading
    let userData = this.state.username;
    socket.emit('chat message', this.state.data, this.state.username, this.state.chat); // getCookie("uid")
    this.state.data = '';
    return false;
    }

    handleChange(e) {
    this.setState({data: e.target.value});
    }

  render() {
    return (
    <div className="compose">
          <input type="text" data={this.state.data} onChange={this.handleChange}
           className="compose-input"
          onSubmit={this.handleSubmit}
          placeholder="Type a message, @name"
        />

        {
          this.props.rightItems
        }
        </div>

    );
  }
}


