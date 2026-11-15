import express from 'express'
import cors from 'cors'

const app = express()

// ruleid: acme.javascript.express.permissive-cors
app.use(cors())

// ruleid: acme.javascript.express.permissive-cors
app.options('*', cors())

// ruleid: acme.javascript.express.permissive-cors
app.use(cors({ origin: true, credentials: true }))

// ok: acme.javascript.express.permissive-cors
app.use(cors({ origin: ['https://customer.acme.example'], credentials: true }))
