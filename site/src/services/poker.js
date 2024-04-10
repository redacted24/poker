import axios from 'axios'
const baseUrl = '/api/poker'

const test = async () => {
  const response = await axios.post(`${baseUrl}/count`)
  return response.data
}

const init = async (player) => {
  const response = await axios.post(`${baseUrl}/init`, player)
  return response.data
}

const clear = async () => {
  const response = await axios.post(`${baseUrl}/clear`)
  return response.data
}

const start = async () => {
  const response = await axios.post(`${baseUrl}/start`)
  return response.data
}

const call = async (player) => {
  const response = await axios.post(`${baseUrl}/call`, player)
  return response.data
}

const check = async (player) => {
  const response = await axios.post(`${baseUrl}/check`, player)
  return response.data
}

const bet = async (player, amount) => {
  const response = await axios.post(`${baseUrl}/bet`, player)
  return response.data
}

export default { test, init, clear, start, call, check , bet }