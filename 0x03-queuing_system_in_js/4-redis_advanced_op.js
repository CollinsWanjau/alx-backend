import { createClient } from 'redis';

const client = createClient();

import redis from 'redis';

client.on('connect', () => console.log('Redis client connected to the server'));

client.on('error', err => console.error(`Redis client not connected to the server: ${err.message}`, err));

const key = 'HolbertonSchools';

const fields = ['Portland', 'Seattle', 'New York', 'Bogota', 'Cali', 'Paris']
const values = [50, 80, 20, 20, 40, 2];

fields.forEach((field, index) => {
    client.hset(key, field, values[index], redis.print)
});

// client.hset('HolbertonSchools', 'Portland', '50', redis.print);
// client.hset('HolbertonSchools', 'Seattle', '80', redis.print);
// client.hset('HolbertonSchools', 'New York', '20', redis.print);
// client.hset('HolbertonSchools', 'Bogota', '20', redis.print);
// client.hset('HolbertonSchools', 'Cali', '40', redis.print);
// client.hset('HolbertonSchools', 'Paris', '2', redis.print);

client.hgetall(key, (err, obj) => {
    if (err) {
        console.log(error)
        throw error;
    }
    console.log(obj)
})