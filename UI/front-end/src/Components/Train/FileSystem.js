import React, { Component } from 'react';
import ListContainer from './ListContainer'
import HTML5Backend from 'react-dnd-html5-backend';
import { DragDropContext } from 'react-dnd';
import ItemsDragLayer from './ItemsDragLayer';
import axios from 'axios';

class FileSystem extends Component {
  constructor(props){
    super(props);
    this.state = { leftItems: [], rightItems: [] };
  }
  componentWillMount() {
    let domain = window.location.protocol + '//' +  
      (window.location.host === 'localhost:3000' ? '127.0.0.1:2345' : '127.0.0.1:2345');
    this.apiRequest = axios.create({
      baseURL: `${domain}/api/v1/`,
      timeout: 25000,
      headers: {
        'content-type': 'application/json',
      },
      error: '',
    });
    this.getFileNames();
    this.addItemsToCart = this.addItemsToCart.bind(this);
  }

  async getFileNames() {
    try {
      let file_names = await this.apiRequest.get('files');
      this.setState({
        ...this.state,
        leftItems: file_names.data.file_names
      });
    } catch (e) {
      console.log(e)
    }
  }


  addItemsToCart(items, source, dropResult) {
    const leftItems = source === 'left' ? this.state.leftItems.filter(x => items.findIndex(y => x === y) < 0) :
      this.state.leftItems.concat(items);
    const rightItems = source === 'left' ? this.state.rightItems.concat(items) :
      this.state.rightItems.filter(x => items.findIndex(y => x === y) < 0);
    this.setState({ leftItems, rightItems });
  }

  async postFiles() {
    try {
      let response = await this.apiRequest.post('files', JSON.stringify(this.state.leftItems));
      console.log(response)
    } catch (e) {
      console.log(e)
    }
  }

  createDataset() {
    let response = this.postFiles()
    console.log(response)
  }

  render() {
    console.log(this.state)
    return (
      <div style={styles.main}>
        <h2>Select files to use for training</h2>
        <h4>Use Shift or Cmd key to multi-select</h4>
        <button style={styles.file_system__button} onClick={() => this.createDataset()}>
          <h2>Create Dataset</h2>
        </button>

        <ItemsDragLayer />

        <div style={styles.content}>
          <div>
            <p style={styles.file_system__title_text}>Selected</p>
            <ListContainer id='left' fields={this.state.leftItems} addItemsToCart={this.addItemsToCart} />
          </div>
          <div style={styles.file_system__list_container}>
          <p style={styles.file_system__title_text}>Unselected</p>
            <ListContainer id='right' fields={this.state.rightItems} addItemsToCart={this.addItemsToCart} />
          </div>
        </div>
      </div>
    );
  }
}

const styles = {
  file_system__list_container: {
    marginLeft: '2em',
  },
  file_system__button: {
    margin: '1em',
  },
  file_system__title_text: {
    fontSize: '1.5em',
    margin: '1.25em'
  },
  main: {
    width: '50%',
    margin: '0 auto',
    textAlign: 'center',
  },
  content: {
    display: 'flex',
    flexFlow: 'row',
    justifyContent: 'left',
    alignItems: 'stretch',
    alignContent: 'stretch',
  },
};

const dragDropContext = DragDropContext;
export default dragDropContext(HTML5Backend)(FileSystem);
