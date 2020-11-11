<template>
  <h1>Hello World!</h1>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      products: [],
      search: '',
    };
  },
  methods: {
    ...mapActions(['getAllProducts']),
    renderProducts() {
      this.getAllProducts()
        .then((res) => {
          this.products = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addToCart(product) {
      this.$store.commit('addOrderItem', product);
    },
  },
  created() {
    this.renderProducts();
  },
};
</script>
