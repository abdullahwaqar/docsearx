<template>
    <section class="section">
        <div v-if="error" class="notification is-danger">
        <button @click="error = ''" class="delete"></button>
        {{ error }}
        </div>
        <div class="columns">
            <div class="column is-half is-offset-one-quarter">
            <div class="control">
                <input v-model="searchTerm" class="input is-medium is-rounded" type="email" placeholder="Enter Search Term...">
            </div>
            </div>
        </div>
        <br>
        <button @click="search" class="button is-medium is-primary is-capitalized">Search</button>
    </section>
</template>

<script>
export default {
    name: 'Search'
}
</script>