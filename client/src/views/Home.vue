<template>
<section>
    <section class="hero is-fullheight">
    <!-- Hero content: will be in the middle -->
    <div class="hero-body">
        <div class="container has-text-centered">
        <h1 class="title logo-font"><i class="fab fa-searchengin"></i> docsearx</h1>
        <h2 class="subtitle">
            A minimal document search engine.
        </h2>
        <search-bar></search-bar>
        <p><a>{{ numberOfDoc }}</a> documents indexed.</p>
        </div>
    </div>
    </section>
</section>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

import Search from '@/components/Search.vue';

export default {
    name: 'home',
    components: {
        'search-bar': Search
    },
    computed: {
        ...mapGetters({ numberOfDoc: 'getNumberOfIndexedDocumnets' })
    },
    mounted: function() {
        this.ping();
    },
    methods: {
        ...mapActions({ ping: 'pingServer' })
    }
}
</script>

<style scoped>
.logo-font {
    font-family: 'Finger Paint', cursive;
}
</style>
