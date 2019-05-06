import React, { Component } from 'react';
import './ChatSearch.css';

export default class ChatSearch extends Component {
  render() {
    return (
      <div className="chat-search">
        <input
          type="search"
          className="chat-search-input"
          placeholder="Search Messages"
        />
      </div>
    );
  }
}