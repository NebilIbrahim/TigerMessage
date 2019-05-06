import React, {Component} from 'react';

import {Header} from './components/Header'
import {ChatItem} from './components/ChatItem'
import {Form} from './components/Form'

import logo from './chat.png';
import './App.css';

import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom'

class App extends React.Component {
  render() {
    return (
      <div className="App">
          <Header />
          <ChatItem />
          <Form />
      </div>
    )
  }
}

export default App;
