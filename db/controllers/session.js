const sessionsRouter = require('express').Router()
const Session = require('../models/session')

sessionsRouter.get('/:id', async (request, response) => {
  const session = await Session.findById(request.params.id)
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

sessionsRouter.put('/:id', async (request, response) => {
  const session_update = { ...request.body }

  const session = await Session.findById(request.params.id)

  if (!session) response.status(404).end()

  const new_session = await Session.findByIdAndUpdate(
    request.params.id,
    session_update
  )

  response.json(new_session)
})

sessionsRouter.delete('/:id', async (request, response) => {
  const session_to_delete = await Session.findById(request.params.id)

  if (!session_to_delete) response.status(404).end()

  await Session.findByIdAndDelete(request.params.id)

  response.status(204).end()
})

module.exports = sessionsRouter