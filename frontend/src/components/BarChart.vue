<template>
<div class="example-barchart">
  <apexchart width="500" height="350" type="bar" :options="chartOptions" :series="series"></apexchart>
   <div>
       <button @click="updateChart">Update!</button>
    </div>
</div>
</template>

<script>
  import axios from 'axios';
  export default {
    name: 'ColumnExample',
    data: function() {
      return {
        chartOptions: {
          plotOptions: {
            bar: {
              horizontal: false,
              endingShape: 'rounded',
              columnWidth: '55%',
            },
          },
          dataLabels: {
            enabled: false,
          },
          stroke: {
            show: true,
            width: 2,
            colors: ['transparent'],
          },
          xaxis: {
            categories: [
              '0',
              '5',
              '10',
              '15',
              '20',
              '25',
              '30',
              '35',
              '40',
              '45',
              '50',
              '55',
              '60',
            ],
            title: {
              text: 'Days',
            },
          },
          yaxis: {
            title: {
              text: 'Rads',
            },
          },
          fill: {
            opacity: 1,
          },
          tooltip: {
            y: {
              formatter: function(val) {
                return '$ ' + val + ' thousands';
              },
            },
          },
        },
        series: [
          {
            name: 'Days Historgram',
            data: [55, 41, 36, 26, 45, 48, 52, 53, 41],
          },
        ],
      };
    },
    methods: {
      updateChart() {
        const url = 'https://853f7148.ngrok.io/getrads';
        console.log('url'), url;
        axios
          .get(url)
          .then(response => {
            let result = response.data.data;
            this.series[0].data = result;
          })
          .catch(error => {
            console.log('error', error);
          });
      },
    },
    mounted() {
      this.updateChart();
    },
  };
</script>
<style lang="scss">
  .example-barchart {
    margin-top: 50px;
  }
</style>
