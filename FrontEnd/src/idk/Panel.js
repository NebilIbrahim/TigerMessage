class Panel extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: false, // <~ set loading to false
      messages: data,
      filtered: data,
    }
  }

  componentDidMount() {this.updateData();}
  componentWillReceiveProps(nextProps) {
    // Check to see if the requestRefresh prop has changed
    if (nextProps.requestRefresh === true) {
      this.setState({loading: true}, this.updateData);
    }
  }

  handleSearch = txt => {
    if (txt === '') {
      this.setState({
        filtered: this.state.messages
      })
    } else {
      const { messages } = this.state
      const filtered = messages.filter(a => a.actor && a.actor.login.match(txt))
      this.setState({
        filtered
      })
    }
  }

  // Call out to github and refresh directory
  updateData() {
    this.setState({
      loading: false,
      messages: data
    }, this.props.onComponentRefresh);
  }

  render() {
    const {loading, filtered} = this.state;

    return (
      <div>
        <Header
          onSubmit={this.handleSearch}
          title="emma" />
        <div className="content">
          <div className="line"></div>
          {/* Show loading message if loading */}
          {loading && <div>Loading</div>}
          {/* Chat item */}
          {filtered.map((message) => (
            <MessageItem
              key={message.id}
              message={message} />
          ))}

        </div>
      </div>
    )
  }
}