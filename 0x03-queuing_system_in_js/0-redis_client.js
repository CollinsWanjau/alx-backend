import { createClient } from 'redis'

const client = createClient()

client.on('connection', () => console.log('Redis client connected to the server'))

client.on('error', err => console.error(`Redis client not connected to the server: ${err.message}`, err))
