<template>
    <section class="section">
        <div class="columns">
            <div class="column is-half is-offset-one-quarter">
                <div class="field is-grouped">
                    <div class="control is-expanded">
                        <input v-model="searchTerm" class="input is-primary is-medium is-rounded" type="email" placeholder="Enter Search Term...">
                    </div>
                    <div class="control">
                        <button @click="invokeSearch" class="button is-medium is-primary is-capitalized is-rounded"><i class="fas fa-search"></i>Search</button>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    name: 'Search',
    data: function() {
        return {
            searchTerm: ''
        }
    },
    methods: {
        ...mapActions({ search: 'search' }),
        invokeSearch() {
            if (!this.searchTerm.length > 4) {
                return;
            }
            this.search(this.searchTerm);
        }
    }
}
</script>