<script>
  import Plot from "$lib/Plot.svelte";
  export let agreement;
  let currentDataset = "K Means Clustering for Climate News";
  $: data = agreement;
  $: layout = {
    height: 600,
    title: currentDataset,
    scene: {
      xaxis: { title: "x" },
      yaxis: { title: "y" },
      zaxis: { title: "z" }
    }
  };
</script>

<Plot {data} {layout} />
