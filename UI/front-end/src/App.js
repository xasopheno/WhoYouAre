import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom'
import FileServer from './FileSystem';


class App extends Component {
  constructor(props){
    super(props)
    this.state = {

    }
  }
  render() {
    return (
      <Switch>
        <Route exact path='/train' component={FileServer}/>
        <Route exact path='/play' component={FileServer}/>
      </Switch>
    );
  }
}

export default App;
