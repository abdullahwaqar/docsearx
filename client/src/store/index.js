import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

const BASE_URL = `http://127.0.0.1:5000/api`;

export default new Vuex.Store({
    state: {
        numberOfIndexedDocumnets: 0,
        searcResults: null,
        currentQuery: ''
    },
    mutations: {
        setNumberOfIndexedDocumnets(state, number) {
            state.numberOfIndexedDocumnets = number;
        },
        setSearchResults(state, results) {
            state.searcResults = results;
        }
    },
    getters: {
        getNumberOfIndexedDocumnets(state) {
            return state.numberOfIndexedDocumnets;
        },
        getSearchResults(state) {
            return state.searcResults;
        }
    },
    actions: {
        async pingServer({ commit }) {
            try {
                const response = await axios.get(`${BASE_URL}/ping`);
                commit('setNumberOfIndexedDocumnets', response.data.number_of_files);
            } catch (error) {
                console.error(error);
            }
        },
        async search({ commit }, query) {
            try {
                const SEARCH_URL = `/search?q=`;
                const response = await axios.get(`${BASE_URL}${SEARCH_URL}${query}`);
                commit('setSearchResults', response.data);
            } catch (error) {
                console.error(error);
            }
        },
    }
});
