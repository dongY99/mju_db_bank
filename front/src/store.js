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
    addCustomer(state, customer) {
      state.customers.push(customer); // 새 고객 추가
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
        const response = await axios.get('/api/deposit_account');

        commit('setDepositAccount', response.data);        
      } catch(error) {
        console.error('fetch depositAccount fail: ', error);
      }
    },

    async fetchCard({commit}) {
      try {
        const response = await axios.get('/api/card');

        commit('setCard', response.data);        
      } catch(error) {
        console.error('fetch card fail: ', error);
      }
    },

    async fetchTransations({commit}) {
      try {
        const response = await axios.get('/api/transations');

        commit('setTransations', response.data);        
      } catch(error) {
        console.error('fetch transations fail: ', error);
      }
    },

    async postCustomer({ commit }, customer) {
      try {
        const response = await axios.post('/add_customer', customer);
        commit('addCustomer', response.data.customer); // Store에 새 고객 추가
      } catch (error) {
        console.error('Error posting customer:', error);
        throw error; // Vue 컴포넌트에서 에러를 처리하도록 전달
      }
    },
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