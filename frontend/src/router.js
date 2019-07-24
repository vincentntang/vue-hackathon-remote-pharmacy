import Vue from 'vue';
import Router from 'vue-router';
// import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Patients from './views/Patients.vue';
import PatientProfile from './components/PatientProfile.vue';
import PatientPrescription from './components/PatientPrescription.vue';
import PatientHistory from './components/PatientHistory.vue';
import Radiation from './views/Radiation.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login,
    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () =>
    //     import(/* webpackChunkName: "about" */ './views/About.vue'),
    // },
    {
      path: '/patients',
      name: 'patients',
      component: Patients,
      props: true, // accept props from login routes
    },
    {
      path: '/patients/:id',
      name: 'patient-id',
      component: PatientProfile,
      props: true,
    },
    {
      path: '/patients/prescription/:id',
      name: 'prescription',
      component: PatientPrescription,
      props: true,
    },
    {
      path: '/patients/history/:id',
      name: 'history',
      component: PatientHistory,
      props: true,
    },
    {
      path: '/radiation',
      name: 'radiation',
      component: Radiation,
      props: true,
    },
  ],
});
