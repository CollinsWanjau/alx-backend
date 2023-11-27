import { error } from 'console';
// import { channel, unsubscribe } from 'diagnostics_channel';
import { createClient } from 'redis';

const client = createClient();

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', err => console.error(`Redis client not connected to the server: ${err.message}`, err));

client.subscribe('holberton school channel', (err, reply) => {
  if (err) {
    console.log(error);
    throw error;
  } else {
    console.log(reply);
  }
});

client.on('message', (channel, message) => {
  if (channel === 'holberton school channel') console.log(message);
  if (message === 'KILL_SERVER') {
    client.unsubscribe();
    client.quit();
  }
});
