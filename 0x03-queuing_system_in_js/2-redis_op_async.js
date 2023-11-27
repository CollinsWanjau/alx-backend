import { createClient } from 'redis';
import { promisify } from 'util';

const client = createClient();

const redis = require('redis');

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', err => console.error(`Redis client not connected to the server: ${err.message}`, err));

// use the promisify function to convert the client.get method into a promise-based function
const getAsync = promisify(client.get).bind(client);

function setNewSchool (schoolName, value) {
  // Use the client set method to set a value for a key and use a callback
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue (schoolName) {
  console.log(await getAsync(schoolName));
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
