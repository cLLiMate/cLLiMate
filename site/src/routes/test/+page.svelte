<script>
  import ThreeDPlot from "./ThreeDPlot.svelte";
  import TestPlot from "./TestPlot.svelte";
  export let data;
  console.log(data.agreement.GroupOne);
</script>

<h1>Component Test</h1>

<TestPlot agreement={data.agreement.GroupZero} />
<TestPlot agreement={data.agreement.GroupOne} />
<TestPlot agreement={data.agreement.GroupTwo} />
<ThreeDPlot agreement={data.agreement.umapClimate} />
