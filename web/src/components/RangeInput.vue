<template>
  <input type='range' :value='value' :max='max' :min='min' @change.prevent='onValueChange'/>
</template>

<script>
export default {
  name: 'RangeInput',
  props: {
    value: {
      default: 0
    },
    change: {
      type: Function,
      required: false
    },
    max: {
      type: Number,
      default: 10
    },
    min: {
      type: Number,
      default: 0
    },
    step: {
      type: Number,
      default: 1
    }
  },
  methods: {
    onValueChange(event) {
      this.$emit('change', event.target.value)
    }
  }
}
</script>

<style scoped>
/*
 Generate here
 http://www.cssportal.com/style-input-range/
 */
input[type="range"] {
  height: 28px;
  -webkit-appearance: none;
  margin: 0;
  width: 100%;
}
input[type="range"]:focus {
  outline: none;
}
input[type="range"]::-webkit-slider-runnable-track {
  width: 100%;
  height: 5px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 0px 0px 0px #8f8f8f;
  background: #ebebeb;
  border-radius: 1px;
  border: 0px solid #ffffff;
}
input[type="range"]::-webkit-slider-thumb {
  box-shadow: 1px 1px 1px #313131;
  border: 1px solid #1e1c1c;
  height: 20px;
  width: 20px;
  border-radius: 50px;
  background: #ffffff;
  cursor: pointer;
  -webkit-appearance: none;
  margin-top: -8px;
}
input[type="range"]:focus::-webkit-slider-runnable-track {
  background: #ebebeb;
}
input[type="range"]::-moz-range-track {
  width: 100%;
  height: 5px;
  cursor: pointer;
  animate: 0.2s;
  box-shadow: 0px 0px 0px #8f8f8f;
  background: #ebebeb;
  border-radius: 1px;
  border: 0px solid #ffffff;
}
input[type="range"]::-moz-range-thumb {
  box-shadow: 1px 1px 1px #313131;
  border: 1px solid #1e1c1c;
  height: 20px;
  width: 20px;
  border-radius: 50px;
  background: #ffffff;
  cursor: pointer;
}
input[type="range"]::-ms-track {
  width: 100%;
  height: 5px;
  cursor: pointer;
  animate: 0.2s;
  background: transparent;
  border-color: transparent;
  color: transparent;
}
input[type="range"]::-ms-fill-lower {
  background: #ebebeb;
  border: 0px solid #ffffff;
  border-radius: 2px;
  box-shadow: 0px 0px 0px #8f8f8f;
}
input[type="range"]::-ms-fill-upper {
  background: #ebebeb;
  border: 0px solid #ffffff;
  border-radius: 2px;
  box-shadow: 0px 0px 0px #8f8f8f;
}
input[type="range"]::-ms-thumb {
  margin-top: 1px;
  box-shadow: 1px 1px 1px #313131;
  border: 1px solid #1e1c1c;
  height: 20px;
  width: 20px;
  border-radius: 50px;
  background: #ffffff;
  cursor: pointer;
}
input[type="range"]:focus::-ms-fill-lower {
  background: #ebebeb;
}
input[type="range"]:focus::-ms-fill-upper {
  background: #ebebeb;
}
</style>
