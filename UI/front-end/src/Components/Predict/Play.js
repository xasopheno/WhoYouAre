import React, { Component } from 'react';
import connectToSocket from '../Shared/connectToSocket';

class Play extends Component {
  constructor(props){
    super(props);
    this.state = {
      input: {
        note: [0],
        length: [0],
      },
      output: {
        note: [0],
        length: [0],
      }
    };
    this.socket = connectToSocket();

    this.socket.on('reconnect_attempt', () => {
      this.socket.io.opts.transports = ['polling', 'websocket'];
    });
  }

  componentWillMount() {
    this.socket.emit('client_connect', {data: 'I\'m connected!'});
    this.socket.on('connected_to_server', function() {console.log('Connected')});
    this.socket.on('disconnect', function() {console.log('disconnected')});
    this.socket.on('model_input', this.onModelInput.bind(this));
    this.socket.on('model_output', this.onModelOutput.bind(this));
  }

  ringBuffer(array, value) {
    let clone = array.slice(0);
    if (clone.length >= 30) {
      clone.pop();
      clone.unshift(value);
    } else {
      clone.unshift(value);
    }
    return clone;
  }

  onModelInput(data) {
    this.setState({
      ...this.state,
      input: {
        note: data.data.note,
        length: data.data.length,
      }
    })
  }

  onModelOutput(data) {
    let note = this.ringBuffer(this.state.output.note, data.data.note);
    let length = this.ringBuffer(this.state.output.length, data.data.length);
    this.setState({
      ...this.state,
      output: {
        note: note,
        length: length,
      }
    })
  }

  renderInputArray(array) {
    let clone = array.slice(0);
    clone.reverse();
    return clone.map((value, index) => {
      if (index === 0) {
        return <p style={{
          margin: '.1em',
          color: 'black',
          backgroundColor: '#00FA9A',
          fontSize: '1.2em',
          padding: '0.5em',
        }} key={index}>{value}</p>
      } else {
        return <p
          style={{
            margin: '.1em',
            color: 'grey',
            fontSize: '.8em',
          }}
          key={index}>{value}</p>
      }
    })
  }

  renderOutputArray(array) {
    return array.map((value, index) => {
      if (index === 0) {
        return <p style={{
          margin: '.1em',
          color: 'black',
          backgroundColor: '#00CED1',
          fontSize: '1.2em',
          padding: '0.5em',
        }} key={index}>{value}</p>
      } else {
        return <p
          style={{
            margin: '.1em',
            color: 'grey',
            fontSize: '.8em',
          }}
          key={index}>{value}</p>
      }
    })
  }

  render() {
    return (
      <div>
        <p>Play</p>
        <div style={{
          display: 'flex',
          flexDirection: 'row',
        }}>
          <p>Input</p>
          <div style={{
            margin: '1em',
            marginTop: '0',
            display: 'flex',
            flexDirection: 'column',
          }}>
            <p>note</p>
            {this.renderInputArray(this.state.input.note)}
          </div>
          <div style={{
            margin: '1em',
            marginTop: '0',
            display: 'flex',
            flexDirection: 'column',
          }}>
            <p>length</p>
            {this.renderInputArray(this.state.input.length)}
          </div>



          <div style={{
            display: 'flex',
            flexDirection: 'row',
          }}>
            <p>Output</p>
            <div style={{
              margin: '1em',
              marginTop: '0',
              display: 'flex',
              flexDirection: 'column',
            }}>
              <p>note</p>
              {this.renderOutputArray(this.state.output.note)}
            </div>
            <div style={{
              margin: '1em',
              marginTop: '0',
              display: 'flex',
              flexDirection: 'column',
            }}>
              <p>length</p>
              {this.renderOutputArray(this.state.output.length)}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Play;
