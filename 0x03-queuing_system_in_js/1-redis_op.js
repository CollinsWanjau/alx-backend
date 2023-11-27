// import { redis } from 'kue'
import { createClient } from 'redis';

const client = createClient();

const redis = require('redis');

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', err => console.error(`Redis client not connected to the server: ${err.message}`, err));

function setNewSchool (schoolName, value) {
  // Use the client set method to set a value for a key and use a callback
  client.set(schoolName, value, redis.print);
}

function displaySchoolValue (schoolName) {
  client.get(schoolName, (err, reply) => {
    if (err) {
      console.error(err);
    } else {
      console.log(reply);
    }
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
