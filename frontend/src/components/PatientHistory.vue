<template>
<div class="example example-history">
  <apexchart width="500" height="200" type="heatmap" :options="chartOptions" :series="series"></apexchart>
</div>
</template>

<script>
  export default {
    name: 'HeatmapExample',
    data: function() {
      return {
        chartOptions: {
          dataLabels: {
            enabled: false,
          },
          colors: ['#008FFB'],
          xaxis: {
            type: 'category',
          },
          title: {
            text: 'Prescription History',
          },
        },
        series: [
          {
            name: 'Saturday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Friday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Thursday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Wednesday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Tuesday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Monday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
          {
            name: 'Sunday',
            data: this.generateData(2, {
              min: 0,
              max: 1,
            }),
          },
        ],
      };
    },
    methods: {
      generateData(count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
          var x = (i + 1).toString();
          var y =
            Math.floor(Math.random() * (yrange.max - yrange.min + 1)) +
            yrange.min;
          series.push({
            x: x,
            y: y,
          });
          i++;
        }
        return series;
      },
    },
  };
</script>

<style lang="scss">
  .example-history {
    transform: scale(1.5);
    margin-top: 100px;
    position: relative;
    &:after {
      position: absolute;
      content: 'AM';
      background-color: white;
      z-index: 5;
      left: 35%;
      bottom: 10%;
    }
    &:before {
      position: absolute;
      content: 'PM';
      background-color: white;
      z-index: 5;
      right: 20%;
      bottom: 10%;
    }
  }
</style>