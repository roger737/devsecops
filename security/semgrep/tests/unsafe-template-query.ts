import type { Request } from 'express'
import { models } from './models'

export async function unsafeLogin (req: Request) {
  // ruleid: acme.javascript.sequelize.unsafe-template-query
  return models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}'`, { plain: true })
}

export async function safeLogin (req: Request) {
  // ok: acme.javascript.sequelize.unsafe-template-query
  return models.sequelize.query('SELECT * FROM Users WHERE email = ?', {
    replacements: [req.body.email || ''],
    plain: true
  })
}

export async function safeBindLogin (req: Request) {
  // ok: acme.javascript.sequelize.unsafe-template-query
  return models.sequelize.query('SELECT * FROM Users WHERE email = $email', {
    bind: { email: req.body.email || '' },
    plain: true
  })
}
