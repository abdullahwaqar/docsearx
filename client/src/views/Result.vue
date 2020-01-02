<template>
<section>
    <section class="hero is-small">
    <!-- Hero content: will be in the middle -->
    <div class="hero-body">
        <div class="container has-text-centered">
        <a href="/" class="title logo-font"><i class="fab fa-searchengin"></i> docsearx</a>
        <search-bar></search-bar>
        <div v-if="query != null">
            <results></results>
            <br>
        </div>
        </div>
    </div>
    </section>
</section>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

import Search from '@/components/Search.vue';
import Results from '@/components/Results.vue';

export default {
    name: 'result',
    components: {
        'search-bar': Search,
        'results': Results
    },
    computed: {
        ...mapGetters({ query: 'getSearchResults' })
    }
}
</script>

<style scoped>
.logo-font {
    font-family: 'Finger Paint', cursive;
}
</style>
