import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
})

export const apiRequest = async (method, endpoint, data = null) => {
  const baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000'
  
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  }

  if (data && method !== 'GET') {
    config.body = JSON.stringify(data)
  }

  const response = await fetch(`${baseURL}${endpoint}`, config)
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
  }
  
  return response.json()
}