<template>
  <div class="example">
    <apexchart width="500" height="350" type="line" :options="chartOptions" :series="series"></apexchart>
    <div>
       <button @click="updateChart">Update!</button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    name: 'LineExample',
    data: function() {
      return {
        chartOptions: {
          xaxis: {
            categories: ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
            title: {
              text: 'Minutes',
            },
          },
          yaxis: {
            title: {
              text: 'Rads',
            },
          },
        },
        series: [
          {
            name: 'Series A',
            data: [30, 40, 45, 50, 49, 60, 70, 91],
          },
        ],
      };
    },
    methods: {
      generateDayWiseTimeSeries(baseval, count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
          var x = baseval;
          var y =
            Math.floor(Math.random() * (yrange.max - yrange.min + 1)) +
            yrange.min;

          series.push([x, y]);
          baseval += 86400000;
          i++;
        }
        return series;
      },
      updateChart() {
        const url = 'https://853f7148.ngrok.io/getradslive';
        console.log('url', url);
        axios
          .get(url)
          .then(response => {
            console.log('response', response);
            // let result = response.data.data;
            let result = response.data;
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