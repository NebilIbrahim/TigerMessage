class Content extends React.Component {
  render() {
    const {messages} = this.props; // ES6 destructuring

    return (
      <div className="content">
        <div className="line"></div>

        {/* Message item */}
        {messages.map((message) => (
          <MessageItem
            messages={message} />
        ))}

      </div>
    )
  }
}