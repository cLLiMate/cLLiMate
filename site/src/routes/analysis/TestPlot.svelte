<script>
  import Plot from "$lib/Plot.svelte";
  export let agreement;
  let currentDataset = Object.keys(agreement)[0];
  let logOr = false;
  $: data = [
    {
      x: agreement[currentDataset].x,
      y: agreement[currentDataset].y,

      mode: "lines+markers",
      type: "scatter"
    }
  ];
  $: layout = {
    height: 400,
    title: currentDataset,
    xaxis: {
      title: "Time",
      autorange: true
    },
    yaxis: {
      autorange: true,
      title: "No. Articles Published or Percent of Reviews",
      type: logOr ? "log" : "linear"
    }
  };
</script>

<Plot {data} {layout} />

<label for="pet-select">Choose the graph to look at: </label>
<select bind:value={currentDataset}>
  {#each Object.entries(agreement) as [name, x]}
    <option value={name}>{name}</option>
  {/each}
</select>
<label>
  <input type="checkbox" bind:checked={logOr} />
  Logarithmic Scale
</label>
