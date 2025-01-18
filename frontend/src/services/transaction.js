import api from './api';

export const transactionsApi = {
  // Create a new transaction request
  create: async (transactionData) => {
    try {
      const response = await api.post('/api/transactions/', transactionData);
      return response.data;
    } catch (error) {
      console.error('Error creating transaction:', error);
      throw error;
    }
  },

  // Get all transactions for the current user
  getAll: async () => {
    try {
      const response = await api.get('/api/transactions/');
      // Ensure each transaction has a material object
      return response.data.map(transaction => ({
        ...transaction,
        material: transaction.material || {}  // Provide default empty object if material is null
      }));
    } catch (error) {
      console.error('Error fetching transactions:', error);
      throw error;
    }
  },

  // Get a specific transaction by ID
  getById: async (id) => {
    const response = await api.get(`/api/transactions/${id}`);
    return response.data;
  },

  // Update transaction status
  updateStatus: async (id, status) => {
    try {
      const response = await api.patch(`/api/transactions/${id}/status`, { status });
      return response.data;
    } catch (error) {
      console.error('Error updating transaction status:', error);
      throw error;
    }
  },

  // Get incoming transaction requests (for providers)
  getIncoming: async () => {
    const response = await api.get('/api/transactions/incoming');
    return response.data;
  },

  // Get outgoing transaction requests (for requesters)
  getOutgoing: async () => {
    const response = await api.get('/api/transactions/outgoing');
    return response.data;
  },

  // Get transaction history
  getHistory: async (id) => {
    const response = await api.get(`/api/transactions/${id}/history`);
    return response.data;
  },

  // Complete a transaction
  complete: async (id) => {
    const response = await api.post(`/api/transactions/${id}/complete`);
    return response.data;
  },

  // Cancel a transaction
  cancel: async (id) => {
    const response = await api.patch(`/api/transactions/${id}/status`, { status: 'cancelled' });
    return response.data;
  },

  getStats: async () => {
    console.log('Making stats request...');
    const response = await api.get('/api/transactions/stats');
    console.log('Stats response:', response.data);
    return response.data;
  }
};