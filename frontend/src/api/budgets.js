import { http } from './http'

export const budgetsApi = {
  list() {
    return http.get('/budgets')
  },
  dashboard() {
    return http.get('/budgets/dashboard')
  },
  create(payload) {
    return http.post('/budgets', payload)
  },
  update(id, payload) {
    return http.put(`/budgets/${id}`, payload)
  }
}
