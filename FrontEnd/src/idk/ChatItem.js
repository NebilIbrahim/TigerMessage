import React, {Component} from 'react';
import PropTypes from 'prop-types'

export class ChatItem extends Component {
  render() {
    const {messages} = this.props; // ES6 destructuring

    return (
      <div className="chatitem">
        <div className="line"></div>

        {/* Chat item */}
        {messages.map((message) => (
           <MessageItem
             message = {message} />
         ))}

      </div>
    )
  }
}
