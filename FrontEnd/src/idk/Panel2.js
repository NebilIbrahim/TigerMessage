class Panel extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: false, // <~ set loading to false
      searchFilter: '',
      messages: []
    }
  }

  componentDidMount() {this.updateData();}
  componentWillReceiveProps(nextProps) {
    // Check to see if the requestRefresh prop has changed
    if (nextProps.requestRefresh === true) {
      this.setState({loading: true}, this.updateData);
    }
  }

  onComponentRefresh() {this.setState({loading: false});}

  handleSearch(val) {
    // handle search here
  }

  render() {
    const {loading} = this.state;

    return (
      <div>
        <Header
          onSearch={this.handleSearch.bind(this)}
          title="Github activity" />
        <Content
          requestRefresh={loading}
          onComponentRefresh={this.onComponentRefresh.bind(this)}
          fetchData={this.updateData.bind(this)} />
      </div>
    )
  }
}