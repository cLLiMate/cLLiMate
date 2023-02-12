<script>
  import Plot from "$lib/Plot.svelte";
  export let agreement;
  let currentDataset = "Test3d";
  $: data = agreement;
  $: layout = {
    title: currentDataset,
    scene: {
      xaxis: { title: "x" },
      yaxis: { title: "y" },
      zaxis: { title: "z" }
    }
  };
</script>

<Plot {data} {layout} />
