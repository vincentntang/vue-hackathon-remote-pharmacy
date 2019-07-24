<template>
  <div class="wrapper">
    <div>
      <div class="big-fat-card card" style="width: 30rem;">
        <img class="card-img-top" :src="profile.image" alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">{{profile.name}}</h5>
        </div>
        <div class="wrapper-buttons">
          <router-link :to="`/patients/prescription/${id}`" exact class="btn btn-primary">Prescription</router-link>
          <router-link :to="`/patients/history/${id}`" exact class="btn btn-primary">History</router-link>
        </div>        
      </div>
    </div>
    <!-- Some text boxes -->
  </div>
</template>

<script>
  import pictureData from '../data.js';
  // import { db } from './firebase';

  export default {
    data() {
      return {
        id: parseInt(this.$route.params.id), // let id be the unique patient id
        profile: '',
      };
    },
    methods: {
      _handlePrescription() {},
      _handleHistory() {},
    },
    mounted() {
      this.profile = pictureData.profiles.find(x => x.id === this.id);
    },
  };
</script>

<style lang="scss" scoped>
  .card {
    width: 300px !important;
  }
  .big-fat-card {
    margin-bottom: 60px;
  }
  .wrapper-buttons {
    display: flex;
    justify-content: space-evenly;
  }
</style>