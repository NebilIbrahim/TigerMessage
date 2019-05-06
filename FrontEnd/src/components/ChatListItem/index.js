import React, { Component } from 'react';
import shave from 'shave';

import './ChatListItem.css';

export default class ChatListItem extends Component {
  componentDidMount() {
    shave('.chat-snippet', 20);
  }

  render() {
    const {name, text } = this.props.data;

    return (
      <div className="chat-list-item">
        <div className="chat-info">
          <h1 className="chat-title">{ name }</h1>
          <p className="chat-snippet">{ text }</p>
        </div>
      </div>
    );
  }
}