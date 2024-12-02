import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
  state(){
    return {
      customers: [],
      depositAccount: [],
      card: [],
      transations: [],
    }
  },

  mutations: {
    setCustomers(state, customers) {
      state.customers = customers
    },
    setDepositAccount(state, depositAccount) {
      state.depositAccount = depositAccount
    },
    setCard(state, card) {
      state.card = card
    },
    setTransations(state, transations) {
      state.transations = transations
    }

  },

  actions: {
    async fetchCustomers({commit}) {
      try {
        const response = await axios.get('/api/customers');

        commit('setCustomers', response.data);        
      } catch(error) {
        console.error('fetch customers fail: ', error);
      }
    },

    async fetchDepositAccount({commit}) {
      try {
        const response = await axios.get('/api/depositAccount');

        commit('setDepositAccount', response.data);        
      } catch(error) {
        console.error('fetch depositAccount fail: ', error);
      }
    },

    async fetchCard({commit}) {
      try {
        const response = await axios.get('/api/Card');

        commit('setCard', response.data);        
      } catch(error) {
        console.error('fetch card fail: ', error);
      }
    },
    
    async fetchTransations({commit}) {
      try {
        const response = await axios.get('/api/Transations');

        commit('setTransations', response.data);        
      } catch(error) {
        console.error('fetch transations fail: ', error);
      }
    }
  },

  getters: {
    allCustomers(state) {
      return state.customers;
    },
    allDepositAccount(state) {
      return state.depositAccount;
    },
    allCard(state) {
      return state.card;
    },
    allTransations(state) {
      return state.transations;
    },
  }
})

export default store