<template>
<section>
<div>
<div v-for="value in query" :key="value.index" class="card">
  <div class="card-content">
    <p class="title">
        <a>{{ value[0] }}</a>
    </p>
    <p class="subtitle">
      With score of <strong>{{ value[1] }}</strong>
    </p>
  </div>
</div>
</div>
</section>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
    name: 'Results',
    computed: {
        ...mapGetters({ query: 'getSearchResults' })
    }
}
</script>
