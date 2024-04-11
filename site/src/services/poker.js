import axios from 'axios'
const baseUrl = '/api/poker'

const test = async () => {
  const response = await axios.get(`${baseUrl}/hi`)
  return response
}

export default { test }