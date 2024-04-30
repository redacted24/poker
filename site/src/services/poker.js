import axios from 'axios'
const baseUrl = '/api/poker'

const test = async () => {
  const response = await axios.post(`${baseUrl}/count`)
  return response.data
}

const init = async (req) => {
  const response = await axios.post(`${baseUrl}/init`, req)
  return response.data
}

const quickStart = async (req) => {
  const response = await axios.post(`${baseUrl}/quick_start`, req)
  return response.data
}

const join = async (req) => {
  const response = await axios.post(`${baseUrl}/join`, req)
  
  return response.data
}

const clear = async (req) => {
  const response = await axios.post(`${baseUrl}/clear`, req)
  return response.data
}

const start = async (req) => {
  const response = await axios.post(`${baseUrl}/start`, req)
  return response.data
}

const getTable = async (req) => {
  const response = await axios.post(`${baseUrl}/get-table`, req)
  return response.data
}

const call = async (req) => {
  const response = await axios.post(`${baseUrl}/call`, req)
  return response.data
}

const check = async (req) => {
  const response = await axios.post(`${baseUrl}/check`, req)
  return response.data
}

const fold = async (req) => {
  const response = await axios.post(`${baseUrl}/fold`, req)
  return response.data
}

const bet = async (req) => {
  const response = await axios.post(`${baseUrl}/bet`, req)
  return response.data
}

const next = async (req) => {
  const response = await axios.post(`${baseUrl}/go_next`, req)
  return response.data
}

export default { test, init, quickStart, join, clear, start, getTable, call, check, fold, bet, next }