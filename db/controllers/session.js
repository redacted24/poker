const sessionsRouter = require('express').Router()
const Session = require('../models/session')

sessionsRouter.get('/', async (request, response) => {
  const { session_key } = request.body
  const session = await Session.findOne({ session_key })
  response.json(session)
})

sessionsRouter.post('/', async (request, response) => {
  const content = request.body
  
  if (!content) response.status(401)
    .json({ error: 'no content was provided' })

  const session = new Session({
    ...content
  })
  
  const result = await session.save()
  response.status(201).json(result)
})

sessionsRouter.put('/', async (request, response) => {
  const content = request.body

  Session.findByIdAndUpdate(content.id)

})

module.exports = sessionsRouter