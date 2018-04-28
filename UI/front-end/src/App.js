import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom'
import FileServer from './Components/Train/FileSystem';
import Play from './Components/Predict/Play';


class App extends Component {
  constructor(props){
    super(props)
    this.state = {

    }
  }
  render() {
    return (
      <Switch>
        <Route exact path='/' component={FileServer}/>
        <Route exact path='/train' component={FileServer}/>
        <Route exact path='/play' component={Play}/>
      </Switch>
    );
  }
}

export default App;
