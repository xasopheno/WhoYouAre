import io from 'socket.io-client';


export default function connect_to_socket() {
  let address = window.location.host === 'localhost:3000' ?
    '127.0.0.1:2345' : '127.0.0.1:2345';

  let socket = io(`${address}`, {
    transports: ['websocket'],
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax : 5000,
    reconnectionAttempts: Infinity,
  });

  return socket;
};
