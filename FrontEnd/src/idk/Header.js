import React, {Component} from 'react';

export class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      searchVisible: false
    }
  }
   // toggle visibility when run on the state
  showSearch() {
    this.setState({
      searchVisible: !this.state.searchVisible
    })
  }
  render() {
    let searchInputClasses = ["searchInput"];

      // Update the class array if the state is visible
      if (this.state.searchVisible) {
        searchInputClasses.push("active");
      }
      const wrapperStyle = {
      backgroundColor: 'rgba(94, 15, 173, 1)'
       }

      const titleStyle = {
         color: '#111111'
       }

      const menuColor = {
        backgroundColor: '#111111'
        }

    return (
      <div style={wrapperStyle} className="header">

        <div className="more">

          <div className="newIcon">
            <div className="dashTop"></div>
          </div>

        <span style={titleStyle} className="title">
          {this.props.title}
        </span>

        {/* Search things */}
        <SearchForm
          searchVisible={this.state.searchVisible}
          onSubmit={this.props.onSubmit} />

        {/* Adding an onClick handler to call the showSearch button */}
        <div
          style={titleStyle}
          onClick={this.showSearch.bind(this)}

        <div className="search - searchIcon"></div>

      </div>
    )
  }
}
Header.propTypes = {
  onSearch: PropTypes.func
  }


export default Header