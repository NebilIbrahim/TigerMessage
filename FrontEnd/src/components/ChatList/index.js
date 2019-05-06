import React, { Component } from 'react';
import ChatSearch from '../ChatSearch';
import ChatListItem from '../ChatListItem';
import Toolbar from '../Toolbar';
import ToolbarButton from '../ToolbarButton';
import axios from 'axios';

import './ChatList.css';

export default class ChatList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chats: []
    };
  }

  componentDidMount() {
    this.getChats();
  }

  getChats = () => {
  {/* figure out hpps part */}
    axios.get('https://randomuser.me/api/?results=20').then(response => {
      this.setState(prevState => {
        let chats = response.data.results.map(result => {
          return {
            photo: result.picture.large,
            name: `${result.name.first} ${result.name.last}`,
            text: 'Hello world! This is a long message that needs to be truncated.'
          };
        });

        return { ...prevState, chats };
      });
    });
  }

  render() {
    return (
      <div className="chat-list">
        <Toolbar
          title="Messenger"
          leftItems={[
            <ToolbarButton key="cog" icon="ion-ios-cog" />
          ]}
          rightItems={[
            <ToolbarButton key="add" icon="ion-ios-add-circle-outline" />
          ]}
        />
        <ChatSearch />
        {
          this.state.chats.map(chat =>
            <ChatListItem
              key={chat.name}
              data={chat}
            />
          )
        }
      </div>
    );
  }
}