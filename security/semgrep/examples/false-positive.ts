import { models } from './models'

const reportingRegion = 'eu-west-1'

export async function regionalReport () {
  // nosemgrep: acme.javascript.sequelize.unsafe-template-query -- SEC-1042; fixed deployment constant; owner @REPOSITORY_OWNER; expires 2026-12-31
  return models.sequelize.query(`SELECT * FROM RegionalTotals WHERE region = '${reportingRegion}'`, { plain: true })
}
