import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
  state() {
    return {
      customers: [],
      depositAccount: [],
      card: [],
      transactions: [],
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
    addDepositAccount(state, depositAccount) {
      state.depositAccount.push(depositAccount);
    },

    setCard(state, card) {
      state.card = card
    },
    addCard(state, card) {
      state.card.push(card);
    },

    setTransactions(state, transaction) {
      state.transactions = transaction
    },
    addTransactions(state, transaction) {
      state.transactions.push(transaction);
    }

  },

  actions: {
    async fetchCustomers({ commit }) {
      try {
        const response = await axios.get('/api/customers');

        commit('setCustomers', response.data);
      } catch (error) {
        console.error('fetch customers fail: ', error);
      }
    },

    async fetchDepositAccount({ commit }) {
      try {
        const response = await axios.get('/api/deposit_account');

        commit('setDepositAccount', response.data);
      } catch (error) {
        console.error('fetch depositAccount fail: ', error);
      }
    },

    async fetchCard({ commit }) {
      try {
        const response = await axios.get('/api/card');

        commit('setCard', response.data);
      } catch (error) {
        console.error('fetch card fail: ', error);
      }
    },

    async fetchTransaction({ commit }) {
      try {
        const response = await axios.get('/api/transactions');

        commit('setTransactions', response.data);
      } catch (error) {
        console.error('fetch transaction fail: ', error);
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

    async postDepositAccount({ commit }, depositAccount) {
      try {
        const response = await axios.post("/add_deposit_account", depositAccount);
        commit("addDepositAccount", response.data.deposit_account); // Vuex 상태 업데이트
      } catch (error) {
        console.error("Error posting deposit account:", error);
        throw error;
      }
    },

    async postCard({ commit }, card) {
      try {
        const response = await axios.post("/add_card", card);
        commit("addCard", response.data.card); // Vuex 상태 업데이트
      } catch (error) {
        console.error("Error posting card:", error);
        throw error;
      }
    },

    async postTransactions({ commit }, transactions) {
      try {
        const response = await axios.post("/add_transaction", transactions);
        commit("addTransactions", response.data.transaction); // Vuex 상태 업데이트
      } catch (error) {
        console.error("Error posting transaction:", error);
        throw error;
      }
    },

    async searchCustomer({ commit }, resident_registration_number) {
      const response = await axios.get('/query/customer/pk', {
        params: { resident_registration_number: resident_registration_number } // 쿼리 파라미터
      });
      console.log(response.data.customer)

      commit("setCustomers", response.data.customer)
    },

    async searchDepositAccount({ commit }, deposit_account_id) {
      const response = await axios.get('/query/deposit_account/pk', {
        params: { deposit_account_id: deposit_account_id } // 쿼리 파라미터
      });

      commit("setDepositAccount", response.data.deposit_account)
    },

    async searchCard({ commit }, card_id) {
      const response = await axios.get('/query/card/pk', {
        params: { card_id: card_id } // 쿼리 파라미터
      });

      commit("setCard", response.data.card)
    },

    async searchTransaction({ commit }, deposit_account_id) {
      const response = await axios.get('/query/transaction', {
        params: { deposit_account_id: deposit_account_id } // 쿼리 파라미터
      });

      commit("setTransactions", response.data.transactions)
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
    alltransaction(state) {
      return state.transactions;
    },
  }
})

export default store