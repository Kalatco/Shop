import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import axios from "axios";

export default createStore({
  /***********************************************
   *                  STATE                      *
   ***********************************************/
  state: {
    shoppingCart: [],
    serverName: `${window.location.protocol}//${window.location.hostname}:8000`,
    stripePublishableKey: "pk_test_51H6Q2LHxVqe5J3VbRnN0TFtd8e6v09aA5UfloeoQBETwRqv9g2pT90Y0ihlwn2be2SVKzOZ1wgW32gnWOihKQCGI00Oe4EURlY",

  },
  /***********************************************
   *            SESSION STORAGE                  *
   ***********************************************/
  // sessionStorage is for develop mode only
  plugins: [createPersistedState({
    storage: window.sessionStorage
  })],
  /***********************************************
   *                MUTATIONS                    *
   ***********************************************/
  mutations: {
    addOrderItem: function (state, item) {
      state.shoppingCart.push(item);
    },
    removeOrderItem: function (state, item) {
      state.forEach((cartItem, index, object) => {
        if(cartItem.id == item.id)
          object.splice(index, 1);
      });
    },
    clearOrderList: function (state) {
      state.shoppingCart = [];
    },
  },
  /***********************************************
   *                 ACTIONS                     *
   ***********************************************/
  actions: {
    getAllCategories: function({ state }) {
      return axios.get(`${state.serverName}/api/categories`);
    },
    getCategoryProducts: function({ state }, id) {
      return axios.get(`${state.serverName}/api/categories/${id}`)
    },
    getAllProducts: function({ state }) {
      return axios.get(`${state.serverName}/api/products`);
    },
    getSingleProduct: function({ state }, id) {
      return axios.get(`${state.serverName}/api/products/${id}`)
    },
  },
  /***********************************************
   *                 MODULES                     *
   ***********************************************/
  modules: {}
});
