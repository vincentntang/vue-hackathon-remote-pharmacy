<template>
  <div>
    <form v-on:submit.prevent class="patient-form">
      <div>
        <label class="typo__label">Prescription</label>
        <multiselect v-model="prescriptionValue" :options="prescriptionOptions" :searchable="false" :close-on-select="false" :show-labels="false" placeholder="Pick a Medication"></multiselect>
      </div>
      <div class="form-group">
        <label for="exampleFormControlInput1">Dosage</label>
        <input v-model="dosage" type="text" class="form-control" id="exampleFormControlInput1" placeholder="e.g. 4">
      </div>
      <!-- <div>
        <label class="typo__label">Frequency</label>
        <multiselect v-model="frequencyValue" :options="frequencyOptions" :searchable="false" :close-on-select="false" :show-labels="false" placeholder="Choose a frequency"></multiselect>
      </div> -->
      <div class="radio-btns">
        <label class="typo__label">Frequency</label>
        <br/>
        <input type="radio" id="one" value="AM" v-model="frequencyValue">
        <label for="one">AM</label>
        <input type="radio" id="two" value="PM" v-model="frequencyValue">
        <label for="two">PM</label>
        <input type="radio" id="two" value="Daily" v-model="frequencyValue">
        <label for="two">Daily</label>
      </div>
      <div class="radio-btns">
        <label class="typo__label">Refill</label>
        <br/>
        <input type="radio" id="one" value="Yes" v-model="picked">
        <label for="one">Yes</label>
        <br>
        <input type="radio" id="two" value="No" v-model="picked">
        <label for="two">No</label>
      </div>
      <div class="form-group">
        <label for="exampleFormControlTextarea1">Additional Text Notes</label>
        <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" v-modal="textzone"></textarea>
      </div>
      <button @click="_handleSubmitPrescription" class="btn btn-primary">Submit Prescription</button>
    </form>
  </div>
</template>

<script>
  // import AppDropdown from './AppDropdown.vue';
  // import dropdown from 'vue-dropdowns';
  // import AppDropdown from './AppDropdown.vue';
  import Multiselect from 'vue-multiselect';
  export default {
    components: {
      Multiselect,
    },
    data() {
      return {
        id: parseInt(this.$route.params.id), // let id be the unique patient id
        prescriptionValue: '',
        frequencyValue: '',
        picked: '',
        textzone: '',
        dosage: '',
        prescriptionOptions: [
          'Levothyroxine',
          'Lisinopril',
          'Atorvastatin',
          'Metformin Hydrochloride',
          'Amlodipine Besylate',
          'Metoprolol',
          'Omeprazole',
          'Simvastatin',
          'Losartan Potassium',
          'Albuterol',
          'Gabapentin',
          'Hydrochlorothiazide',
        ],
        frequencyOptions: ['AM', 'PM', 'Daily'],
      };
    },
    methods: {
      _handleSubmitPrescription() {
        Swal.fire({
          title: 'Are you sure?',
          text: '',
          type: 'warning',
          showCancelButton: true,
          confirmButtonColor: '#3085d6',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes',
        }).then(result => {
          if (result.value) {
            Swal.fire('Success!', 'Your file has been saved', 'success');
          }
        });
        this._handlePostRequest();
        // router.push({ name: 'patient-id', params: { userId: id } });
      },
      _handlePostRequest() {
        var request = require('request');

        var options = {
          method: 'POST',
          url: 'http://853f7148.ngrok.io/prescribe',
          headers: {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json',
          },
          // body: {
          // prescriptionID: '23',
          // patientID: '1',
          // medicationName: 'Vicodin',
          // dosage: 'B',
          // refillable: '0',
          // },
          body: {
            // prescriptionID: '23',
            patientID: this.id + '',
            medicationName: this.prescriptionValue,
            dosage: this.dosage,
            refillable: this.picked,
          },
          json: true,
        };
        console.log('options', options);

        request(options, function(error, response, body) {
          if (error) throw new Error(error);

          console.log(body);
        });
      },
    },
    // methods: {
    //   methodToRunOnSelect(payload) {
    //     console.log('I ran');
    //   },
    // },
  };
</script>

<style lang="scss">
  .patient-form {
    margin-top: 30px;
    width: 300px;
    text-align: left;
  }
  .form-group {
    margin-top: 20px;
  }
  li.dropdown-toggle:after {
    content: '';
    border: 0px !important;
    border-color: transparent;
    border-bottom-color: transparent !important;
    display: none;
  }
  .radio-btns {
    margin-top: 10px;
    input {
      margin-right: 10px;
    }
    label {
      margin-right: 10px;
    }
  }
</style>